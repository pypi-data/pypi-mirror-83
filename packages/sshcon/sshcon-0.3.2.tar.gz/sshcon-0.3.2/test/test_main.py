import os
from pathlib import Path

import pytest
from sshcon.main import SshCon

host = os.environ["SSHHOST"]
user = os.environ["SSHUSER"]
key = os.environ["SSHKEY"]

remote = SshCon(host, user, key)

TEMP_DIR = "/tmp/sshcon_test_dir"
MADEUP_DIR = "/I/DO/NOT/EXIST/PYTHON/EGGS/BACON"
REMOTE_FILENAME = "/tmp/sshcon_write.tst"
DATA = "Hello, this is test file to check if writing is working in sshcon."
APPEND_DATA = "PS: PYTHON IS BEST"
LOCAL_FILE = Path("/tmp/sshcon_get_file.tst")


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


def test_send_file():
    local_filename = Path("/tmp/scp_sshcon.tst_local")
    remote_filename = Path("/tmp/scp_sshcon.tst_remote")
    with open(local_filename, "w") as file:
        file.write("This is test file for sshcon!")
    try:
        remote.send_file(local_filename, remote_filename)
    except FileExistsError:
        remote.remove(remote_filename)
        remote.send_file(local_filename, remote_filename)
    remote.remove(remote_filename)
    local_filename.unlink()


def test_write_file():
    try:
        remote.write_text(DATA, REMOTE_FILENAME)
    except FileExistsError:
        remote.remove(REMOTE_FILENAME)
        remote.write_text(DATA, REMOTE_FILENAME)


def test_overwrite_data():
    remote.write_text(DATA, REMOTE_FILENAME, force=True)


def test_overwrite_data_exception():
    with pytest.raises(FileExistsError):
        remote.write_text(DATA, REMOTE_FILENAME, force=False)
    remote.write_text(DATA, REMOTE_FILENAME, force=True)


def test_append_data():
    remote.write_text(APPEND_DATA, REMOTE_FILENAME, append=True)


def test_read_text():
    text = remote.read_text(REMOTE_FILENAME)
    assert text == DATA + APPEND_DATA


def test_get_file():
    try:
        remote.get_file(REMOTE_FILENAME, LOCAL_FILE)
    except FileExistsError:
        LOCAL_FILE.unlink()
        remote.get_file(REMOTE_FILENAME, LOCAL_FILE)
    with open(LOCAL_FILE, "r") as file:
        text = file.read()
    assert text == DATA + APPEND_DATA


def test_get_file_nonforce():
    with pytest.raises(FileExistsError):
        remote.get_file(REMOTE_FILENAME, LOCAL_FILE, force=False)


def test_get_file_force():
    remote.get_file(REMOTE_FILENAME, LOCAL_FILE, force=True)
    LOCAL_FILE.unlink()


def test_remove():
    remote.remove(REMOTE_FILENAME)
