import os

import pytest
from sshcon.main import SshCon

host = os.environ["SSHHOST"]
user = os.environ["SSHUSER"]
key = os.environ["SSHKEY"]

remote = SshCon(host, user, key)

TEMP_DIR = "/tmp/sshcon_test_dir"
MADEUP_DIR = "/I/DO/NOT/EXIST/PYTHON/EGGS/BACON"


def test_mkdir_exception():
    with pytest.raises(PermissionError):
        remote.mkdir(MADEUP_DIR)


def test_is_dir():
    assert remote.isdir("/tmp")


def test_mkdir():
    remote.mkdir(TEMP_DIR)
    assert remote.isdir(TEMP_DIR)


def test_rmdir():
    remote.rmdir(TEMP_DIR)
    with pytest.raises(FileNotFoundError):
        assert remote.isdir(TEMP_DIR)


def test_run():
    string = "test one two three"
    echo = remote.run(["echo", string], capture_output=True, check=True)
    assert echo.stdout == string
    assert echo.rcode == 0
    assert echo.stderr == ""


def test_run_exception():
    with pytest.raises(OSError):
        remote.run([MADEUP_DIR])


def test_lstat():
    with pytest.raises(FileNotFoundError):
        remote._lstat(MADEUP_DIR)


def test_umount_exception():
    with pytest.raises(PermissionError):
        remote.umount(MADEUP_DIR)
