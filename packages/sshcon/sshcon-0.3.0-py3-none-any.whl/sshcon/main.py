"""Python SSH connector/wrapper for linux systems based on super fast SSH2
protocol library -> ssh2-python
"""

import errno
import os
import socket
import stat
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

from ssh2.exceptions import SFTPProtocolError
from ssh2.session import Session
from ssh2.sftp import (
    LIBSSH2_FXF_APPEND,
    LIBSSH2_FXF_CREAT,
    LIBSSH2_FXF_READ,
    LIBSSH2_FXF_WRITE,
    LIBSSH2_SFTP_S_IRGRP,
    LIBSSH2_SFTP_S_IROTH,
    LIBSSH2_SFTP_S_IRUSR,
    LIBSSH2_SFTP_S_IWUSR,
)

from sshcon.exceptions import SshConError, SshConSftpError


class SshCon:
    """A class to represent ssh connection."""

    def __init__(
        self, host: str, user: str, key: Union[Path, str], port: int = 22
    ) -> None:
        """Constructs all the necessary attributes for the SshCon object.

        Args:
            host (str): Hostname or IP adress of remote machine.
            user (str): SSH user to use for the connection.
            key (Union[Path, str]): File with SSH RSA private key.
            port (int, optional): Port number for ssh connection. Defaults to 22.
        """
        self.user = user
        self.key = str(key)
        self.host = host
        self.port = port
        self.sftp = None
        self.session = self._make_session()

    def _make_session(self) -> Session:
        """Makes SSH connection and handshake.

        Returns:
            Session: Succesfully connected Session object.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        session = Session()
        session.handshake(sock)
        session.userauth_publickey_fromfile(self.user, self.key)
        return session

    def _sftp_session(self):
        """Makes SFTP session.

        Returns:
            PySFTP: Object with SFTP session.
        """
        if self.sftp is None:
            self.sftp = self.session.sftp_init()
        return self.sftp

    def _lstat(self, path: Union[Path, str]):
        """Get file lstat

        Args:
            path (Union[Path, str]): File for which to get lstat.

        Raises:
            SshConSftpError: Raise when lstat command fails.

        Returns:
            attrs: File lstat.
        """
        sftp = self._sftp_session()

        try:
            fstat = sftp.lstat(str(path).encode("utf-8"))
        except SFTPProtocolError as msgerr:
            err_code = sftp.last_error()
            if err_code == 2:
                raise FileNotFoundError(f"File {path} not found.") from msgerr
            raise SshConSftpError("lsstat", err_code) from msgerr
        else:
            return fstat.permissions

    def run(
        self,
        cmd: Union[List, str],
        capture_output: bool = False,
        check: bool = True,
        user: Optional[str] = None,
        encoding: Optional[str] = "utf-8",
    ) -> Optional[NamedTuple]:
        """Run command on the remote machine.

        Raises:
            OSError: Raises error if command returns non-zero error code.

        Returns:
            CompletedCommand: Object CompletedCommand with rcode, stdout and stderr.
        """
        if isinstance(cmd, list):
            cmd = [str(item) for item in cmd]
            cmd = " ".join(cmd)
        if user is not None:
            cmd = f"su - {user} -c '{cmd}'"
        channel = self.session.open_session()
        channel.execute(cmd)
        channel.wait_eof()
        channel.close()
        channel.wait_closed()
        rcode = channel.get_exit_status()
        _buffsize, stderr = channel.read_stderr()
        if check:
            if rcode:
                raise OSError(rcode, stderr.decode("utf-8").strip(), cmd)
        if capture_output:
            size, data = channel.read()
            stdout = b""
            while size > 0:
                stdout += data
                size, data = channel.read()
            if encoding:
                stderr = stderr.decode(encoding)
                stdout = stdout.decode(encoding).rstrip()
            return CompletedCommand(rcode, stdout, stderr)
        return None

    def mkdir(
        self,
        path: Union[Path, str],
        mode: int = 511,
        exist_ok: bool = True,
        parents: bool = False,
    ) -> None:
        """Make dir in a remote machine.

        Args:
            path (Union[Path, str]): Path of directory to create.
            mode (int, optional): Permissions mode of new directory. Defaults to 511.
            exist_ok (bool, optional): No error if existing. Defaults to True.
            parents (bool, optional): Make parent directories as needed. Defaults to False.
        """
        mkdir_cmd = ["mkdir", "-m", mode, path]
        if parents or exist_ok:
            mkdir_cmd.insert(1, "-p")
        self.run(mkdir_cmd, check=True)

    def remove(
        self,
        path: Union[Path, str],
        force: bool = False,
        recursive: bool = False,
    ) -> None:
        """Remove files or directories.

        Args:
            path (Union[Path, str]): File or folder to remove.
            force (bool, optional): Ignore nonexistent files, never prompt. Defaults to False.
            recursive (bool, optional): Remove directories and their contents recursively.
                                        Defaults to False.
        """
        rm_cmd = ["rm", path]
        if force:
            rm_cmd.insert(1, "-f")
        if recursive:
            rm_cmd.insert(1, "-r")
        self.run(rm_cmd, check=True)

    def rmdir(self, path: Union[Path, str]) -> None:
        """Remove empty directories.

        Args:
            path (Union[Path, str]): Empty directory to remove.
        """
        self._sftp_session().rmdir(str(path))

    def isdir(self, path: Union[str, Path]) -> bool:
        """Check if path is directory.

        Args:
            path (Union[str, Path]): Target path.

        Returns:
            bool: True if directory else False.
        """
        return stat.S_ISDIR(self._lstat(path))

    def isfile(self, path: Union[str, Path]) -> bool:
        """Check if path is file.

        Args:
            path (Union[str, Path]): Target path.

        Returns:
            bool: True if file else False.
        """
        return stat.S_ISREG(self._lstat(path))

    def ismounted(self, mount) -> bool:
        """Check if path is mountpoint.

        Args:
            path (Union[str, Path]): Target path.

        Returns:
            bool: True if mountpoint else False.
        """
        try:
            self.run(["mountpoint", mount])
        except OSError:
            return False
        else:
            return True

    def get_filemode(self, path: Union[Path, str]):
        """Get file status.

        Args:
            path (Union[Path, str]): Target path.

        """
        fstat = self._sftp_session().lstat(path)
        return stat.filemode(fstat.permissions)

    def mount(
        self,
        source: str,
        target: Union[Path, str],
        force: bool = False,
        mkdir: bool = False,
    ) -> None:
        """Mounts a filesystem in remote machine.

        Args:
            source (str): Source filesystem.
            target (Union[Path, str]): Target filesystem.
            force (bool, optional): Umount current filesystem and mount new
                                    filesystem. Defaults to False.
            mkdir (bool, optional): Make directory if not exist. Defaults to False.

        Raises:
            SshConError: Raises error if target is already a mountpoint and option
                         force is not used.
        """
        if self.ismounted(target):
            if force:
                self.umount(target)
            else:
                raise SshConError("mount", f"Folder {target} is already mountpoint.")
        if mkdir:
            self.mkdir(target, exist_ok=True)
        self.run(["mount", source, target], check=True)

    def umount(self, target: Union[Path, str], rmdir: bool = False) -> None:
        """Unmount filesystems.

        Args:
            target (Union[Path, str]): Path to a filesystem to unmount.
            rmdir (bool, optional): Remove directory after unmount. Defaults to False.
        """
        self.run(["umount", target], check=True)
        if rmdir:
            self.rmdir(target)

    def read_text(
        self, file: Union[Path, str], encoding: str = "utf-8"
    ) -> Optional[str]:
        """Gets text from the remote file.

        Args:
            file (Union[Path, str]): Path to a file.
            encoding (str, optional): Which encoding to use. Defaults to "utf-8".

        Raises:
            FileNotFoundError: Raises when file is not found.

        Returns:
            Optional[str]: File content as string.
        """
        text = None
        if self.isfile(file) is False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(file))
        with self._sftp_session().open(
            str(file), LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR
        ) as text_file:
            for _size, text_bytes in text_file:
                text = text_bytes.decode(encoding)
        return text

    def write_text(
        self,
        data: str,
        file: Union[Path, str],
        append: bool = False,
        encoding: str = "utf-8",
        force: bool = False,
    ) -> None:
        """Write text to a remote file.

        Args:
            data (str): Content to write to a file.
            file (Union[Path, str]): Path to a file.
            append (bool, optional): If append text to a file instead of
                                     rewrite a content. Defaults to False.
            encoding (str, optional): Which encoding to use. Defaults to "utf-8".

        Raises:
            IsADirectoryError: If target file is a directory.
            FileExistsError: If target file exists already.
        """
        file = str(file)
        try:
            if self.isdir(file):
                raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), file)
        except FileNotFoundError:
            pass

        mode = (
            LIBSSH2_SFTP_S_IRUSR
            | LIBSSH2_SFTP_S_IWUSR
            | LIBSSH2_SFTP_S_IRGRP
            | LIBSSH2_SFTP_S_IROTH
        )
        f_flags = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
        try:
            if append:
                f_flags = f_flags | LIBSSH2_FXF_APPEND
            elif self.isfile(file) and not force:
                raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), file)
        except FileNotFoundError:
            pass

        with self._sftp_session().open(file, f_flags, mode) as text_file:
            text_file.write(data.encode(encoding))

    def chmod(self, path: Union[Path, str], mode: int, recursive: bool = False) -> None:
        """Change file mode bits in remote machine.

        Args:
            path (Union[Path, str]): Path to a target.
            mode (int): File mode bits.
            recursive (bool, optional): Change file mod recursively. Defaults to False.
        """
        chmod_cmd = ["chmod", mode, path]
        if recursive:
            chmod_cmd.insert(1, "-R")
        self.run(chmod_cmd, check=True)

    def chown(
        self,
        path: Union[Path, str],
        owner: str,
        group: str,
        recursive: bool = False,
    ) -> None:
        """Change file owner and group in remote machine.

        Args:
            path (Union[Path, str]): Path to a target.
            owner (str): Username of an owner.
            group (str): Group to use.
            recursive (bool, optional): Change owner/group mod recursively. Defaults to False.
        """
        chown_cmd = ["chown", f"{owner}:{group}", path]
        if recursive:
            chown_cmd.insert(1, "-R")
        self.run(chown_cmd, check=True)

    def send_file(
        self,
        file: Union[Path, str],
        destination: Union[Path, str],
        force: bool = False,
    ) -> None:
        """Send local file to a remote location.

        Args:
            file (Union[Path, str]): File to send.
            destination (Union[Path, str]): Target filename in remote machine.
            force (bool, optional): Replace file if already exists. Defaults to False.

        Raises:
            IsADirectoryError: Raises if target destination is a directory.
            FileExistsError: Raises if target destination exists.
        """
        try:
            if self.isdir(destination):
                raise IsADirectoryError(
                    errno.EISDIR, os.strerror(errno.EISDIR), str(file)
                )
        except FileNotFoundError:
            pass

        if not force:
            try:
                if self.isfile(destination):
                    raise FileExistsError(
                        errno.EEXIST, os.strerror(errno.EEXIST), str(file)
                    )
            except FileNotFoundError:
                pass
        fileinfo = os.stat(file)

        chan = self.session.scp_send64(
            str(destination),
            fileinfo.st_mode & 0o777,
            fileinfo.st_size,
            fileinfo.st_mtime,
            fileinfo.st_atime,
        )

        with open(file, "rb") as local_fh:
            for data in local_fh:
                chan.write(data)

    def get_file(
        self, file: Union[Path, str], destination: Union[Path, str], force: bool = False
    ) -> None:
        """Get remote file from a remote location.

        Args:
            file (Union[Path, str]): File to get from a remote.
            destination (Union[Path, str]): Local destination.
            force (bool): Rewrite the file, if exists. Defaults to False

        Raises:
            IsADirectoryError: Raises if file is a directory.
            FileNotFoundError:: Raises if remote file not found.
        """
        if self.isdir(file):
            raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), str(file))

        chan = self.session.scp_recv2(
            str(file),
        )

        mode = "wb+" if force else "xb+"
        with open(destination, mode) as local_fh:
            size = 0
            while True:
                siz, buf = chan[0].read()

                if siz < 0:
                    print("error code:", siz)
                    chan[0].close()
                    break
                size += siz

                if size > chan[1].st_size:
                    local_fh.write(buf[: (chan[1].st_size - size)])
                else:
                    local_fh.write(buf)

                if size >= chan[1].st_size:
                    chan[0].close()
                    break


class CompletedCommand(NamedTuple):
    """Class to represent ssh connection.

    Args:
        NamedTuple (rcode, stdout, stderr): Constructs all the necessary
                                            attributes for the CompletedCommand
                                            object.
    """

    rcode: int
    stdout: Union[str, bytes]
    stderr: str
