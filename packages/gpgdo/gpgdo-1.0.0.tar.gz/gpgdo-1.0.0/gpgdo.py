# gpgdo - decrease effort of using gpg encrypted files
#
# Copyright 2020 Heikki Orsila
#
# SPDX-License-Identifier: BSD-2-Clause
#
# TODO: Automatic armor detection for encrypted files.
# TODO: Handle Command --argument=foo.gpg.

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
import traceback
from typing import List

# Return codes for errors
ARGUMENT_ERROR = 20
CLEANUP_ERROR = 21
DECRYPT_ERROR = 22
ENCRYPT_ERROR = 23
# Could not run the Command, e.g. it does not exist
RUN_ERROR = 24
TEMPFILE_ERROR = 25
UNEXPECTED_ERROR = 26

DESCRIPTION = """
In brief, gpgdo decreases effort of using gpg encrypted files.
Example use-case:

$ gpgdo edit my-text-file.gpg

It is equivalent to doing:

$ gpg -d -o /dev/shm/plain-text my-text-file.gpg
$ edit /dev/shm/plain-text
$ gpg -e -r USER-ID -o my-text-file.gpg /dev/shm/plain-text
$ rm -f /dev/shm/plain-text

gpgdo automates manual decryption and encryption when executing a specific
Command that operates on content that is located in encrypted files.

Security of gpgdo relies on at least 3 factors:
* security of /dev/shm (which is the security of virtual memory)
* file permissions (uses mkstemp() to create a file under /dev/shm)
* deleting the plain text file after use

Terminology: Command (with capital C) refers to the executable that gpgdo
executes.

gpgdo takes a Command with arguments to run, decrypts its gpg file arguments
under /dev/shm, executes the Command for plain text files,
and finally re-encrypts modified files. If the Command fails, plain text files
are not re-encrypted. The plain text files are removed always.

Argument processing for gpgdo specific option arguments ends at "--".
Giving "--" is only necessary if option arguments are given for gpgdo.

gpgdo finds the recipients from decrypted files by the information provided
by gpg and automatically uses the same recipients when re-encrypting files.

The given gpg name on command line does not need to exist.
In this case, the recipient must be provided with
-r USER-ID and "--" must be used to terminate gpgdo argument list:

$ gpgdo -r USER-ID -- edit non-existing-file.gpg


A plain text file is encrypted to replace the original gpg file
only if two conditions hold:
1. The sha256sum of its content changes
2. Command returns success

CAVEATS

Only filenames that end with ".gpg" are decrypted.

BUGS

Option arguments with a gpg filename directly attached are not recognized.
This does not work:

$ gpgdo Command --argument=foo.gpg

Command will read the encrypted file and most probably fail or do the wrong
thing. But this works:

$ gpgdo Command --argument foo.gpg
"""

VERBOSE_MODE = False


def log_debug(*args, **kwargs):
    if VERBOSE_MODE:
        print(*args, **kwargs)


def log_error(*args, **kwargs):
    print('ERROR:', *args, **kwargs)


def log_warning(*args, **kwargs):
    print('WARNING:', *args, **kwargs)


def is_encrypted_path(path):
    return path.endswith('.gpg')


class FileArg:
    def __init__(self, arg_pos: int, gpg_name: str, gpg_exists: bool,
                 plain_text_name: str, is_dup: bool):
        self.arg_pos = arg_pos
        self.gpg_name = gpg_name
        self.gpg_exists = gpg_exists
        self.plain_text_name = plain_text_name
        self.is_dup = is_dup
        self.recipients = None
        self.sha256 = bytes()

    def add_recipient(self, key: str):
        if self.recipients is None:
            self.recipients = []
        self.recipients.append(key)
        log_debug('Add recipient:', key)

    def get_sha256(self) -> bytes:
        h = hashlib.sha256()
        with open(self.plain_text_name, 'rb') as f:
            h.update(f.read())
        return h.digest()

    def set_sha256(self, sha256: bytes):
        assert isinstance(sha256, bytes)
        self.sha256 = sha256


def create_secure_tempfiles(arg_pos, gpg_name, args):
    # Strip .gpg suffix
    assert is_encrypted_path(gpg_name)
    stripped_name = gpg_name[:-4]
    unused, suffix = os.path.splitext(stripped_name)
    # suffix contains the dot, e.g. '.pdf'
    if len(suffix) == 0:
        suffix = None

    if args.same_dir:
        tdir = os.path.dirname(gpg_name)
    else:
        tdir = '/dev/shm'

    try:
        fd, plain_text_name = tempfile.mkstemp(dir=tdir, suffix=suffix)
    except OSError as e:
        log_error('Can not create tempfile: {}'.format(e))
        return None

    os.close(fd)
    fd = None

    # gpg file need not exist. We just don't decrypt it.
    gpg_exists = os.path.isfile(gpg_name)

    # We record arg_pos into file_args so that we can later easily replace
    # encrypted filenames with plain text filenames when we run the actual
    # Command.
    return FileArg(arg_pos, gpg_name, gpg_exists, plain_text_name, False)


def remove_tempfiles(file_args):
    ret = True
    removed = []
    for fa in file_args:
        if fa.is_dup:
            continue
        try:
            os.remove(fa.plain_text_name)
            removed.append(fa.plain_text_name)
        except OSError as e:
            print()
            log_error('Unable to remove plain text file {}: {}'.format(
                fa.plain_text_name, e))
            print()
            ret = False

    log_debug('Removed plain text files: {}'.format(', '.join(removed)))
    return ret


def decrypt_files(file_args, args):
    decrypt_cmd = ['gpg', '-d', '--yes'] + args.decrypt_arg
    for fa in file_args:
        if fa.gpg_exists and not fa.is_dup:
            cmd = decrypt_cmd + ['-o', fa.plain_text_name, fa.gpg_name]
            log_debug('Decrypting:', cmd)
            try:
                cp = subprocess.run(
                    decrypt_cmd + ['-o', fa.plain_text_name, fa.gpg_name],
                    stderr=subprocess.PIPE)
            except OSError as e:
                log_error('Could not run gpg: {}'.format(e))
                return False

            if cp.returncode != 0:
                log_error('Decrypting {} failed.'.format(fa.gpg_name))
                return False

            fa.set_sha256(fa.get_sha256())

            if fa.recipients is not None:
                # The key was given with -r
                continue

            # Decryption was successful. Find the USER-ID for the gpg key.
            try:
                keyinfo = cp.stderr.decode()
            except UnicodeDecodeError as e:
                log_error('Unable to detect USER-ID (gpg key) '
                          'for {}: {}'.format(fa.gpg_name, e))
                return False
            for line in keyinfo.splitlines():
                if len(line) == 0:
                    continue
                fields = line.split()
                if len(fields) < 2:
                    continue
                if fields[0] != 'gpg:' or fields[1] != 'encrypted':
                    continue
                try:
                    i = fields.index('ID')
                except ValueError:
                    break
                i += 1
                if i >= len(fields):
                    break
                if fields[i][-1] != ',':
                    break
                key = fields[i][:-1]
                try:
                    int(key, base=16)
                except ValueError:
                    break
                fa.add_recipient(key)

            if fa.recipients is None:
                log_error('Unable to detect USER-ID (gpg key) for {}'.format(
                    fa.gpg_name))
                return False

    return True


def encrypt_files(file_args, args):
    encrypt_cmd = ['gpg', '-e', '--yes']

    if not VERBOSE_MODE:
        encrypt_cmd.append('-q')

    if args.armor:
        encrypt_cmd.append('-a')

    encrypt_cmd.extend(args.encrypt_arg)

    for fa in file_args:
        if not fa.is_dup:
            sha256 = fa.get_sha256()
            if sha256 == fa.sha256:
                log_debug('Not re-encrypting {} because the content did not '
                          'change.'.format(fa.gpg_name))
                continue

            cmd = list(encrypt_cmd)
            for r in fa.recipients:
                cmd.extend(('-r', r))
            cmd.extend(['-o', fa.gpg_name, fa.plain_text_name])
            log_debug('Encrypting:', cmd)
            cp = subprocess.run(cmd)
            if cp.returncode != 0:
                log_error('Decrypting {} failed.'.format(fa.gpg_name))
                return False

    return True


def run(cmd_args: List[str], file_args: List):
    if len(cmd_args) == 0:
        return 0

    cmd_args = list(cmd_args)
    for fa in file_args:
        cmd_args[fa.arg_pos] = fa.plain_text_name

    log_debug('Executing: {}'.format(cmd_args))

    try:
        cp = subprocess.run(cmd_args)
    except OSError as e:
        log_error('Could not run the Command: {}'.format(e))
        return RUN_ERROR

    return cp.returncode


def exception_error(e):
    print('Exception raised:', traceback.format_exc(e))
    print('\nContinuing to clean up any plain text files.')


def gpgdo():
    filtered_args = []
    i = 0
    cmd_args = None
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--':
            cmd_args = sys.argv[(i + 1):]
            break
        filtered_args.append(arg)
        i += 1

    if cmd_args is None:
        if len(sys.argv) == 1:
            # Nothing to do
            return 0
        if len(sys.argv[1]) > 0 and sys.argv[1][0] != '-':
            cmd_args = sys.argv[1:]
            filtered_args = []  # Do not parse gpgdo args
        else:
            cmd_args = []

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--armor', '-a', action='store_true',
        help=('Encrypt files with ASCII armored output. This is equivalent to '
              '--encrypt-arg=-a.'))
    parser.add_argument(
        '--decrypt-arg', action='append', default=[],
        help='Add a given argument for gpg decryption.')
    parser.add_argument(
        '--encrypt-arg', action='append', default=[],
        help='Add a given argument for gpg encryption.')
    parser.add_argument(
        '--recipient', '-r', dest='recipients', action='append', default=[],
        help=('Encrypt files for given recipients. '
              'This can be given many times. This is given as -r argument '
              'for gpg.'))
    parser.add_argument(
        '--same-dir', '-s', action='store_true',
        help=('Decrypt files in the same directory. By default files are '
              'decrypted under /dev/shm for security. This argument is '
              'useful when a Command refuses to use files under /dev/shm. '
              'This option should only be used with encrypted filesystems.'))
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose mode.')
    args = parser.parse_args(filtered_args[1:])

    global VERBOSE_MODE
    VERBOSE_MODE = args.verbose

    # The process works as follows:
    # 0. Create temp files for plain text content
    # 1. Decrypt cipher text into temp files
    # 2. Run the Command on temp files
    # 3. Re-encrypt temp files
    # 4. Remove temp files

    # Map gpg file's real path to plain text file
    realpaths = {}
    # Collected information about replaced gpg file arguments into file_args
    file_args = []
    for arg_pos, arg in enumerate(cmd_args):
        if arg_pos == 0:
            # The arg is the executed command, not a gpg file
            continue
        bname = os.path.basename(arg)
        if len(bname) == 0 or bname[0] == '-' or not is_encrypted_path(arg):
            continue
        if os.path.exists(arg) and not os.path.isfile(arg):
            log_warning('{} exists, but is not a regular file. '
                        'Ignoring it.'.format(arg))
            continue

        # Resolve real path of the file to detect duplicate gpg files
        realpath = os.path.realpath(arg)
        if realpath in realpaths:
            # Duplicate exists
            gpg_exists = os.path.isfile(arg)
            fa = FileArg(arg_pos, arg, gpg_exists, realpaths[realpath], True)
        else:
            fa = create_secure_tempfiles(arg_pos, arg, args)
            if fa is None:
                remove_tempfiles(file_args)
                return TEMPFILE_ERROR
            realpaths[realpath] = fa.plain_text_name

        if len(args.recipients) > 0:
            for recipient in args.recipients:
                fa.add_recipient(recipient)

        file_args.append(fa)

    ret = 0
    try:
        for fa in file_args:
            if not fa.gpg_exists and len(args.recipients) == 0:
                log_error(
                    'GPG file {} does not exist. If this is intended, please '
                    'provide a recipient with -r USER-ID. E.g. '
                    'gpgdo -r USER-ID -- Command non-existing.gpg'.format(
                        fa.gpg_name))
                ret = ARGUMENT_ERROR
    except Exception as e:
        exception_error(e)
        ret = UNEXPECTED_ERROR

    if ret == 0:
        try:
            if not decrypt_files(file_args, args):
                ret = DECRYPT_ERROR
        except Exception as e:
            exception_error(e)
            ret = UNEXPECTED_ERROR

    if ret == 0:
        try:
            ret = run(cmd_args, file_args)
        except Exception as e:
            exception_error(e)
            ret = UNEXPECTED_ERROR

    if ret == 0:
        # If Command execution worked, re-encrypt files
        try:
            if not encrypt_files(file_args, args):
                log_error('Unable to encrypt files.')
                ret = ENCRYPT_ERROR
        except Exception as e:
            exception_error(e)
            ret = UNEXPECTED_ERROR

    if not remove_tempfiles(file_args):
        ret = CLEANUP_ERROR

    return ret
