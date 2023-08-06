#!/usr/bin/env python3
#
# TODO: Convert markdown automatically from README.md that is intended for
# gitlab.

from distutils.core import setup

version = '1.0.0'

long_description = """
# Introduction

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

## CAVEATS

Only filenames that end with ".gpg" are decrypted.

## BUGS

Option arguments with a gpg filename directly attached are not recognized.
This does not work:

    $ gpgdo Command --argument=foo.gpg

Command will read the encrypted file and most probably fail or do the wrong
thing. But this works:

    $ gpgdo Command --argument foo.gpg
"""

setup(
    name='gpgdo',
    version=version,
    description='gpgdo decreases effort of using gpg encrypted files',
    author='Heikki Orsila',
    author_email='heikki.orsila@iki.fi',
    url='https://gitlab.com/heikkiorsila/gpgdo',
    py_modules=['gpgdo'],
    scripts=['gpgdo'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    )
