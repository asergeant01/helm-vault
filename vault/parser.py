import argparse

RawTextHelpFormatter = argparse.RawTextHelpFormatter


def parse_args(args):
    # Help text
    parser = argparse.ArgumentParser(description="""Store secrets from Helm in Vault
    \n
    Requirements:
    \n
    Environment Variables:
    \n
    VAULT_ADDR:     (The HTTP address of Vault, for example, http://localhost:8200)
    VAULT_TOKEN:    (The token used to authenticate with Vault)
    """, formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="action")

    # Encrypt help
    encrypt = subparsers.add_parser("enc", help="Parse a YAML file and store user entered data in Vault")
    encrypt.add_argument("yaml_file", type=str, help="The YAML file to be worked on")
    encrypt.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    encrypt.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    encrypt.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault) Default: \"secret/helm\"")
    encrypt.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    encrypt.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Decrypt help
    decrypt = subparsers.add_parser("dec", help="Parse a YAML file and retrieve values from Vault")
    decrypt.add_argument("yaml_file", type=str, help="The YAML file to be worked on")
    decrypt.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    decrypt.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    decrypt.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    decrypt.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    decrypt.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Clean help
    clean = subparsers.add_parser("clean", help="Remove decrypted files (in the current directory)")
    clean.add_argument("-f", "--file", type=str, help="The specific YAML file to be deleted, without .dec", dest="yaml_file")
    clean.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # View Help
    view = subparsers.add_parser("view", help="View decrypted YAML file")
    view.add_argument("yaml_file", type=str, help="The YAML file to be worked on")
    view.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    view.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    view.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    view.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    view.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Edit Help
    edit = subparsers.add_parser("edit", help="Edit decrypted YAML file. DOES NOT CLEAN UP AUTOMATICALLY.")
    edit.add_argument("yaml_file", type=str, help="The YAML file to be worked on")
    edit.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    edit.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    edit.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    edit.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    edit.add_argument("-e", "--editor", help="Editor name. Default: (Linux/MacOS) \"vi\" (Windows) \"notepad\"", const=True, nargs="?")
    edit.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Install Help
    install = subparsers.add_parser("install", help="Wrapper that decrypts YAML files before running helm install")
    install.add_argument("-f", "--values", type=str, dest="yaml_file", help="The encrypted YAML file to decrypt on the fly")
    install.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    install.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    install.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    install.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    install.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Template Help
    template = subparsers.add_parser("template", help="Wrapper that decrypts YAML files before running helm install")
    template.add_argument("-f", "--values", type=str, dest="yaml_file", help="The encrypted YAML file to decrypt on the fly")
    template.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    template.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    template.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    template.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    template.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Upgrade Help
    upgrade = subparsers.add_parser("upgrade", help="Wrapper that decrypts YAML files before running helm install")
    upgrade.add_argument("-f", "--values", type=str, dest="yaml_file", help="The encrypted YAML file to decrypt on the fly")
    upgrade.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    upgrade.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    upgrade.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    upgrade.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    upgrade.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Lint Help
    lint = subparsers.add_parser("lint", help="Wrapper that decrypts YAML files before running helm install")
    lint.add_argument("-f", "--values", type=str, dest="yaml_file", help="The encrypted YAML file to decrypt on the fly")
    lint.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    lint.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    lint.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    lint.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    lint.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    # Diff Help
    diff = subparsers.add_parser("diff", help="Wrapper that decrypts YAML files before running helm diff")
    diff.add_argument("-f", "--values", type=str, dest="yaml_file", help="The encrypted YAML file to decrypt on the fly")
    diff.add_argument("-d", "--deliminator", type=str, help="The secret deliminator used when parsing. Default: \"changeme\"")
    diff.add_argument("-mp", "--mountpoint", type=str, help="The Vault Mount Point Default: \"secret/data\"")
    diff.add_argument("-vp", "--vaultpath", type=str, help="The Vault Path (secret mount location in Vault). Default: \"secret/helm\"")
    diff.add_argument("-kv", "--kvversion", choices=['v1', 'v2'], default='v2', type=str, help="The KV Version (v1, v2) Default: \"v1\"")
    diff.add_argument("-v", "--verbose", help="Verbose logs", const=True, nargs="?")

    return parser
