#
# Copyright (c) nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from functools import partial
import os
from os import path
import gzip
import tarfile
import zipfile

from commoncode import fileutils
from commoncode.system import on_linux
from commoncode.system import on_windows
from commoncode.system import py2

"""
Mimimal tar and zip file handling, primarily for testing.
"""


def _extract_tar_raw(test_path, target_dir, to_bytes, *args, **kwargs):
    """
    Raw simplified extract for certain really weird paths and file
    names.
    """
    if to_bytes and py2:
        # use bytes for paths on ALL OSes (though this may fail on macOS)
        target_dir = fileutils.fsencode(target_dir)
        test_path = fileutils.fsencode(test_path)
    tar = None
    try:
        tar = tarfile.open(test_path)
        tar.extractall(path=target_dir)
    finally:
        if tar:
            tar.close()


extract_tar_raw = partial(_extract_tar_raw, to_bytes=True)

extract_tar_uni = partial(_extract_tar_raw, to_bytes=False)


def extract_tar(location, target_dir, verbatim=False, *args, **kwargs):
    """
    Extract a tar archive at location in the target_dir directory.
    If `verbatim` is True preserve the permissions.
    """
    # always for using bytes for paths on all OSses... tar seems to use bytes internally
    # and get confused otherwise
    location = fileutils.fsencode(location)
    if on_linux and py2:
        target_dir = fileutils.fsencode(target_dir)

    with open(location, 'rb') as input_tar:
        tar = None
        try:
            tar = tarfile.open(fileobj=input_tar)
            tarinfos = tar.getmembers()
            to_extract = []
            for tarinfo in tarinfos:
                if tar_can_extract(tarinfo, verbatim):
                    if not verbatim:
                        tarinfo.mode = 0o755
                    to_extract.append(tarinfo)
            tar.extractall(target_dir, members=to_extract)
        finally:
            if tar:
                tar.close()


def extract_zip(location, target_dir, *args, **kwargs):
    """
    Extract a zip archive file at location in the target_dir directory.
    """
    if not path.isfile(location) and zipfile.is_zipfile(location):
        raise Exception('Incorrect zip file %(location)r' % locals())

    if on_linux and py2:
        location = fileutils.fsencode(location)
        target_dir = fileutils.fsencode(target_dir)

    with zipfile.ZipFile(location) as zipf:
        for info in zipf.infolist():
            name = info.filename
            content = zipf.read(name)
            target = path.join(target_dir, name)
            if not path.exists(path.dirname(target)):
                os.makedirs(path.dirname(target))
            if not content and target.endswith(path.sep):
                if not path.exists(target):
                    os.makedirs(target)
            if not path.exists(target):
                with open(target, 'wb') as f:
                    f.write(content)


def extract_zip_raw(location, target_dir, *args, **kwargs):
    """
    Extract a zip archive file at location in the target_dir directory.
    Use the builtin extractall function
    """
    if not path.isfile(location) and zipfile.is_zipfile(location):
        raise Exception('Incorrect zip file %(location)r' % locals())

    if on_linux and py2:
        location = fileutils.fsencode(location)
        target_dir = fileutils.fsencode(target_dir)

    with zipfile.ZipFile(location) as zipf:
        zipf.extractall(path=target_dir)


def tar_can_extract(tarinfo, verbatim):
    """
    Return True if a tar member can be extracted to handle OS specifics.
    If verbatim is True, always return True.
    """
    if tarinfo.ischr():
        # never extract char devices
        return False

    if verbatim:
        # extract all on all OSse
        return True

    # FIXME: not sure hard links are working OK on Windows
    include = tarinfo.type in tarfile.SUPPORTED_TYPES
    exclude = tarinfo.isdev() or (on_windows and tarinfo.issym())

    if include and not exclude:
        return True


def get_gz_compressed_file_content(location):
    """
    Uncompress a compressed file at `location` and return its content as a byte
    string. Raise Exceptions on errors.
    """
    with gzip.GzipFile(location, 'rb') as compressed:
        content = compressed.read()
    return content
