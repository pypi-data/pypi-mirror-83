"""
Library to take care of all passphrase encryption used by AutoNode.
"""

import base64
import os
import subprocess

import pexpect
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pyhmy import (
    cli,
    Typgpy
)

from .common import (
    validator_config,
    node_config,
    log
)
from .exceptions import (
    InvalidWalletPassphrase
)


def _get_harmony_pid():
    try:
        return subprocess.check_output(["pgrep", "harmony"], env=os.environ).strip()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        return b'0'


def _get_process_info(pid):
    assert isinstance(pid, bytes)
    pid = pid.strip()
    try:
        if int(pid) <= 0:
            return b'0'
        proc_start = subprocess.check_output(["ps", "-p", pid.decode(), "-o", "lstart="], env=os.environ).strip()
        proc_command = subprocess.check_output(["ps", "-p", pid.decode(), "-o", "command="], env=os.environ).strip()
        return proc_start + b' ' + proc_command
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError):
        return b'0'


def _get_node_based_salt():
    key = ''.join([str(x) for x in node_config["public-bls-keys"]]
                  + [str(validator_config["validator-addr"]), str(validator_config["identity"])]).encode()
    return hmac.HMAC(key, hashes.SHA256(), backend=default_backend()).finalize()


def _derive_wallet_encryption_key():
    """
    Create the wallet encryption key based on:
        PBKDF2HMAC(PID(harmony) + ProcessInfo(harmony), salt=HMAC(node_bls_public_keys, Validator_Addr, Validator_ID))

    This means that the encryption key is only valid for when AutoNode has a harmony node process running.
    """
    pid = _get_harmony_pid().strip()
    proc_info = _get_process_info(pid).strip()
    salt = _get_node_based_salt().strip()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    data = pid + b' ' + proc_info
    return base64.urlsafe_b64encode(kdf.derive(data))


def encrypt_wallet_passphrase(passphrase):
    """
    Encrypt the given passphrase.

    Returned string can be stored on disk, will be invalidated once harmony process is stopped.
    """
    assert isinstance(passphrase, str)
    return Fernet(_derive_wallet_encryption_key()).encrypt(passphrase.encode())


def decrypt_wallet_passphrase(encrypted_wallet_passphrase):
    """
    Decrypt the given encrypted passphrase.
    """
    assert isinstance(encrypted_wallet_passphrase, bytes)
    try:
        return Fernet(_derive_wallet_encryption_key()).decrypt(encrypted_wallet_passphrase).decode()
    except InvalidToken:
        raise InvalidWalletPassphrase()


def is_valid_passphrase(passphrase, validator_address):
    """
    Validate the given passphrase, can be an expensive call.
    """
    cmd = ["hmy", "keys", "check-passphrase", validator_address]
    try:
        proc = cli.expect_call(cmd)
        proc.expect("Enter wallet keystore passphrase:\r\n")
        proc.sendline(passphrase)
        proc.expect("Valid passphrase\r\n")
        proc.expect(pexpect.EOF)
        return True
    except RuntimeError as e:
        log(f"{Typgpy.FAIL}Failed to verify passphrase due to: {e}{Typgpy.ENDC}")
        return False
    except pexpect.ExceptionPexpect as e:
        log(f"{Typgpy.FAIL}Failed to verify passphrase due to:\n{e.get_trace()}{Typgpy.ENDC}")
        return False
