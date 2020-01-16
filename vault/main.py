#!/usr/bin/env python3

import ruamel.yaml

import os
import getpass
import glob
import sys
import platform
import subprocess

from client import Vault
from parser import parse_args


check_call = subprocess.check_call

if sys.version_info[:2] < (3, 7):
    raise Exception("Python 3.7 or a more recent version is required.")


class Envs:
    def __init__(self, args):
        self.args = args

    def get_env(self, env_name, default=None):
        if env_name in os.environ:
            value = os.environ[env_name]
            if self.args.verbose is True:
                print(f'The environment {env_name} is: {value}')
        elif vars(self.args).get(env_name.lower()):
            value = vars(self.args).get(env_name.lower())
            if self.args.verbose is True:
                print(f'The {env_name} is: {value}')
        elif default:
            value = default
            if self.args.verbose is True:
                print(f'The default {env_name} is: {value}')
        else:
            value = None

        return value

    def get_envs(self):
        # Get environment variables or ask for input
        mount_point = self.get_env('MOUNTPOINT', default='secret/data')
        vault_path = self.get_env('VAULTPATH', default='secret/helm')
        secret_delim = self.get_env('DELIMINATOR', default='changeme')
        kvversion = self.get_env('KVVERSION', default='v2')

        editor_default = 'vi'
        if platform.system() is "Windows":
            editor_default = 'notepad'

        editor = self.get_env('EDITOR', default=editor_default)

        return mount_point, vault_path, secret_delim, editor, kvversion


def load_yaml(yaml_file):
    # Load the YAML file
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    with open(yaml_file) as filepath:
        data = yaml.load(filepath)
        return data


def cleanup(args):
    # Cleanup decrypted files
    yaml_file = args.yaml_file
    try:
        os.remove(f"{yaml_file}.dec")
        if args.verbose is True:
            print(f"Deleted {yaml_file}.dec")
            sys.exit()
    except AttributeError:
        for fl in glob.glob("*.dec"):
            os.remove(fl)
            if args.verbose is True:
                print(f"Deleted {fl}")
                sys.exit()
    except Exception as ex:
        print(f"Error: {ex}")
    else:
        sys.exit()


def dict_walker(pattern, data, args, envs, path=None):
    # Walk through the loaded dicts looking for the values we want
    path = path if path is not None else ""
    action = args.action
    if isinstance(data, dict):
        for key, value in data.items():
            if value == pattern:
                if action == "enc":
                    data[key] = getpass.getpass(f"Input a value for {path}/{key}: ")
                    vault = Vault(args, envs)
                    vault.vault_write(data[key], path, key)
                elif (action == "dec") or (action == "view") or (action == "edit")\
                        or (action == "install") or (action == "template") or (action == "upgrade")\
                        or (action == "lint") or (action == "diff"):
                    vault = Vault(args, envs)
                    vault = vault.vault_read(value, path, key)
                    value = vault
                    data[key] = value
            for res in dict_walker(pattern, value, args, envs, path=f"{path}/{key}"):
                yield res
    elif isinstance(data, list):
        for item in data:
            for res in dict_walker(pattern, item, args, envs, path=f"{path}"):
                yield res


def main(argv=None):
    # Parse arguments from argparse
    # This is outside of the parse_arg function because of issues returning
    # multiple named values from a function
    parsed = parse_args(argv)
    args, leftovers = parsed.parse_known_args(argv)

    yaml_file = args.yaml_file
    data = load_yaml(yaml_file)
    action = args.action

    if action == "clean":
        cleanup(args)

    envs = Envs(args)
    envs = envs.get_envs()
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True

    for path, key, value in dict_walker(envs[2], data, args, envs):
        print("Done")

    if action == "dec":
        yaml.dump(data, open(f"{yaml_file}.dec", "w"))
        print("Done Decrypting")
    elif action == "view":
        yaml.dump(data, sys.stdout)
    elif action == "edit":
        yaml.dump(data, open(f"{yaml_file}.dec", "w"))
        os.system(envs[3] + ' ' + f"{yaml_file}.dec")
    # These Helm commands are only different due to passed variables
    elif (action == "install") or (action == "template") or (action == "upgrade")\
            or (action == "lint") or (action == "diff"):
        yaml.dump(data, open(f"{yaml_file}.dec", "w"))
        leftovers = ' '.join(leftovers)

        if args.verbose is True:
            print(f'LeftOvers: {leftovers}')

        try:
            print(f"helm {args.action} {leftovers} -f {yaml_file}.dec")
            subprocess.run(f"helm {args.action} {leftovers} -f {yaml_file}.dec", shell=True)
        except Exception as ex:
            print(f"Error: {ex}")

        cleanup(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"ERROR: {ex}")
    except SystemExit:
        pass
