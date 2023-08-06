import os
import io
import tarfile
import time
from abc import ABC, abstractmethod
from typing import List, Iterable, IO, Sequence, Union
from pathlib import Path
from contextlib import contextmanager
from itertools import filterfalse

from .error import UserError
from .filesystem import delete_files

tarfile.DEFAULT_FORMAT = tarfile.PAX_FORMAT

METADATA_FILE = "metadata.json"
METADATA_FILE_SIG = "metadata.json.sig"
CHECKSUM_FILE = "checksum.sha256"
DATA_ARCHIVE = "data.tar.gz"
DATA_FILE_ENCRYPTED = DATA_ARCHIVE + ".gpg"
PACKAGE_CONTENT = {METADATA_FILE, METADATA_FILE_SIG, DATA_FILE_ENCRYPTED}
CONTENT_FOLDER = "content"


def check_tar(tar: str):
    if not tar.endswith(".tar"):
        raise UserError(
            "Input file '{}' does not have .tar extension.\n"
            "Only .tar files can be used as input of the data decryption command.".format(tar))
    check_tar_contents(os.path.realpath(tar))


def check_tar_contents(path: str):
    """Checks for exactly one .json file and exactly one .tar.gz.gpg"""
    with tarfile.open(path, format=tarfile.PAX_FORMAT) as tar:
        content = set(tar.getnames())
        content.add(METADATA_FILE_SIG)  # NOTE: Backward compatibility to v0.9
        if content != PACKAGE_CONTENT:
            raise UserError(
                f"Input file '{path}' has non-compliant content:\n" +
                "\n".join(content) + "\n\n"
                "BiomedIT input tar files must contain exactly the following files:\n"
                f"\t- {METADATA_FILE} file with metadata\n"
                f"\t- {DATA_FILE_ENCRYPTED} file with the encrypted data"
            )


class ArchiveFileBase(ABC):
    def __init__(self, archive_path: str, content_container):
        self.archive_path = archive_path
        self.content_container = content_container

    @abstractmethod
    def add_to_tar(self, tar: tarfile.TarFile):
        pass


class ArchiveInMemoryFile(ArchiveFileBase):
    """An ArchiveFileBase whose content_container is a bytes instance"""

    def add_to_tar(self, tar: tarfile.TarFile):
        t = tarfile.TarInfo(self.archive_path)
        t.size = len(self.content_container)
        t.mtime = int(time.time())
        tar.addfile(t, io.BytesIO(self.content_container))


class ArchiveFile(ArchiveFileBase):
    """An ArchiveFileBase whose content_container is a file like object"""

    def add_to_tar(self, tar: tarfile.TarFile):
        t = tar.gettarinfo(name=self.content_container.name,
                           arcname=self.archive_path,
                           fileobj=None)
        with self.content_container as f_opened:
            tar.addfile(t, f_opened)


def write_tar(content: Sequence[ArchiveFileBase],
              output: Union[str, IO[bytes]],
              mode="w:gz") -> None:
    """Create a tar.gz archive with files of input file_list.

    :param content: Files / In-memory-files that will be added to the tar archive.
    :param output: path (or file object) or stream for the output tarball.
    :param mode: Mode to be passed to tarfile, i.e. `'w:gz'`
    :raises UserError:
    """

    arch_names = set(f.archive_path for f in content)
    assert_relative(arch_names)

    if isinstance(output, str):
        open_tar = tarfile.open(name=output, mode=mode)
    else:
        open_tar = tarfile.open(fileobj=output, mode=mode)
    # Compress input files into tarball.
    with open_tar as tar:
        for archive_file in content:
            archive_file.add_to_tar(tar)

    if isinstance(output, str):
        # Verify the tarball file was created correctly. If it's not the case,
        # delete it.
        if not Path(output).is_file():
            raise UserError(f'compression failed for [{output}]: '
                            f'tarball not created.')
        with tarfile.open(output, 'r') as tar:
            missing_files = {Path(p) for p in arch_names} - \
                            {Path(p) for p in tar.getnames()}
        if missing_files:
            delete_files(output)
            raise UserError(f'compression failed for [{output}]: '
                            f'one or more files are missing in tarball.')


def is_relative(path: str):
    return not (
        os.path.isabs(path) or
        os.path.normpath(path).startswith("..")
    )


def assert_relative(files: Iterable[str]):
    """Asserts that each path in the list is relative"""
    non_relative = [f for f in files if not is_relative(f)]
    if non_relative:
        raise UserError(
            "The archive contains files with absolute path or paths ending "
            "in a parent directory:\n" +
            "\n".join(non_relative))


def check_extracted(paths: Iterable[str]):
    """Tests if all paths in :paths: exist now on the file system"""
    failed = tuple(filterfalse(os.path.exists, paths))
    if failed:
        raise UserError("Failed to extract to following files: \n" +
                        "\n".join(failed))


@contextmanager
def extract(archive: IO[bytes], *files):
    with archive as a:
        with tarfile.open(fileobj=a) as tar:
            try:
                if len(files) == 1:
                    yield tar.extractfile(files[0])
                else:
                    yield (tar.extractfile(file_name) for file_name in files)

            except KeyError as e:
                raise UserError(f"In archive {archive.name}: {e.args[0]}") from e


def unpack_from_stream(archive: IO[bytes], dest: str, content: List[str],
                       mode: str = 'r|*'):
    """Extract all files in the tarball from a stream.

    After unpacking the function checks that all files have been properly
    extracted by comparing the new files on disk to the list of files present
    in the tarball.

    :param archive: tarball stream
    :param dest: destination directory for the unpacked data
    :param content: a list container to store the file names compressed in the tarball
    :param mode: Mode to be passed to tarfile, i.e. `'r|*'`
    """
    if not os.path.isdir(dest):
        os.makedirs(dest)
    with tarfile.open(mode=mode, fileobj=archive) as tar:
        for f in tar:
            assert_relative((f.name,))
            content.append(f.name)
            tar.extract(f, dest)
    check_extracted((os.path.join(dest, f) for f in content))
