import hvac
import os


class Vault:
    def __init__(self, args, envs):
        self.args = args
        self.envs = envs
        self.kvversion = envs[4]

        # Setup Vault client (hvac)
        try:
            self.client = hvac.Client(url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
        except KeyError:
            print("Vault not configured correctly, check VAULT_ADDR and VAULT_TOKEN env variables.")
        except Exception as ex:
            print(f"ERROR: {ex}")

    def vault_write(self, value, path, key):
        # Write to vault, using the correct Vault KV version
        try:
            path = os.path.join(self.envs[1], path, key)

            if self.kvversion == "v1":
                if self.args.verbose is True:
                    print(f"Using KV Version: {self.kvversion}")

                self.client.write(mount_point=self.args.mountpoint, path=path, value=value)

            elif self.kvversion == "v2":
                if self.args.verbose is True:
                    print(f"Using KV Version: {self.kvversion}")

                self.client.secrets.kv.v2.create_or_update_secret(mount_point=self.args.mountpoint,
                                                                  path=path, secret=dict(value=value))
            else:
                print("Wrong KV Version specified, either v1 or v2")

#             if self.args.verbose is True:
#                     print(f"Wrote {value} to: {self.args.mountpoint}/{path}/")

        except AttributeError:
            print("Vault not configured correctly, check VAULT_ADDR and VAULT_TOKEN env variables.")
        except Exception as ex:
            print(f"Error: {ex}")

    def vault_read(self, value, path, key):
        # Read from Vault, using the correct Vault KV version
        if self.args.verbose is True:
            print(f"Using KV Version: {self.kvversion}")
        try:
            path = os.path.join(self.envs[1], path, key)

            if self.kvversion == "v1":
                if self.args.verbose is True:
                    print(f"Using KV Version: {self.kvversion}")

                value = self.client.read(mount_point=self.args.mountpoint,
                                         path=path)
                value = value.get("data", {}).get("value")
            elif self.kvversion == "v2":
                if self.args.verbose is True:
                    print(f"Using KV Version: {self.kvversion}")

                value = self.client.secrets.kv.v2.read_secret_version(
                    mount_point=self.args.mountpoint,
                    path=path,
                )
                value = value.get("data", {}).get("data", {}).get("value")
            else:
                print("Wrong KV Version specified, either v1 or v2")

#             if self.args.verbose is True:
#                     print(f"Got {value} from: {self.args.mountpoint}/{path}/")

            return value

        except AttributeError:
            print("Vault not configured correctly, check VAULT_ADDR and VAULT_TOKEN env variables.")
        except Exception as ex:
            print(f"Error: {ex}")
