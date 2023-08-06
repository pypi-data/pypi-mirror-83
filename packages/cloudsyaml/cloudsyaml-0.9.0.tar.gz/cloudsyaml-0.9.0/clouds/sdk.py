from os import path
from cliff.lister import Lister

from clouds import arguments

try:
    import openstack.config.loader as client_config
except ImportError as error:
    raise ImportError("ERROR: Looks like dependencies are not satisfied. Import error: %s" % error)


loader = client_config.OpenStackConfig(app_name='cloudsyaml')


def get_one_cloud(cloud):
    return loader.get_one_cloud(cloud=cloud)


def get_clouds():
    return loader.get_all_clouds()


def list_files(all_files):
    files = list()
    if all_files:
        files += list(filter(path.exists, client_config.CONFIG_FILES))
        files += list(filter(path.exists, client_config.SECURE_FILES))
        files += list(filter(path.exists, client_config.VENDOR_FILES))
    else:
        # The first file found wins
        config_files = list(filter(path.exists, client_config.CONFIG_FILES))
        if config_files:
            files.append(config_files[0])

        secure_files = list(filter(path.exists, client_config.SECURE_FILES))
        if secure_files:
            files.append(secure_files[0])

        vendor_files = list(filter(path.exists, client_config.VENDOR_FILES))
        if vendor_files:
            files.append(vendor_files[0])

    return files


class Files(Lister):
    """Get list of used files"""
    def get_parser(self, prog_name):
        parser = super(Files, self).get_parser(prog_name)

        return arguments.arg_files(parser)

    def take_action(self, parsed_args):
        files = list_files(parsed_args.all)

        return (('name', 'path'), ((path.basename(file),
                                    file) for file in files))
