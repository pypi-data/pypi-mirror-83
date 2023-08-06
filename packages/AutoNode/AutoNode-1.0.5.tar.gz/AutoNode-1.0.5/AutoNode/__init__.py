import json
import logging
import os
import pickle
import sys
import warnings

import requests
from pyhmy import (
    cli,
    Typgpy
)

from .common import (
    log,
    msg_tag,
    harmony_dir,
    node_dir,
    node_sh_log_dir,
    bls_key_dir,
    saved_validator_path,
    imported_wallet_pass_file_dir,
    cli_bin_path,
    saved_node_config_path,
    validator_config,
    node_config,
    load_validator_config,
    load_node_config
)

if sys.version_info.major < 3:
    warnings.simplefilter("always", DeprecationWarning)
    warnings.warn(
        DeprecationWarning(
            "`AutoNode` does not support Python 2. Please use Python 3."
        )
    )
    warnings.resetwarnings()
    exit(-1)

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    warnings.simplefilter("always", ImportWarning)
    warnings.warn(
        ImportWarning(
            "`AutoNode` does not work on Windows or Cygwin. Try using WSL."
        )
    )
    warnings.resetwarnings()
    exit(-1)

if sys.platform.startswith('darwin'):
    warnings.simplefilter("always", ImportWarning)
    warnings.warn(
        ImportWarning(
            "`AutoNode.node` does not work on MacOS."
        )
    )
    warnings.resetwarnings()


def _init():
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(f'{msg_tag} %(message)s')
    log_handler.setFormatter(formatter)
    logging.getLogger('AutoNode').handlers = []
    logging.getLogger('AutoNode').addHandler(log_handler)
    logging.getLogger('AutoNode').setLevel(logging.DEBUG)

    try:
        # TODO: implement logic to check for latest version of CLI and download if out of date.
        cli.environment.update(cli.download(cli_bin_path, replace=False, verbose=False))
        cli.set_binary(cli_bin_path)
    except requests.exceptions.RequestException as e:
        print(f"{Typgpy.FAIL}Request error: {e}. Exiting.{Typgpy.ENDC}", file=sys.stderr)
        raise SystemExit(e)

    try:  # Config file that should exist on setup
        load_validator_config()
    except (json.decoder.JSONDecodeError, IOError, PermissionError):
        warnings.simplefilter("once", ImportWarning)
        warnings.warn(ImportWarning("Could not import validator config, using defaults."))

    if os.path.isfile(saved_node_config_path):  # Internal file that could not exist.
        try:
            load_node_config()
        except (pickle.PickleError, IOError, PermissionError) as e:
            raise SystemExit(f"Could not import saved node config from {saved_node_config_path}, error: {e}")


_init()
