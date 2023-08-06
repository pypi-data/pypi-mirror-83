from os import path
from cliff.lister import Lister

try:
    import openstack.config.loader as client_config
except ImportError as error:
    raise ImportError("ERROR: Looks like dependencies are not satisfied. Import error: %s" % error)


loader = client_config.OpenStackConfig(app_name='cloudsyaml')


def get_one_cloud(cloud):
    return loader.get_one_cloud(cloud=cloud)


def get_clouds():
    return loader.get_all_clouds()


def list_files():
    return list(filter(path.exists, client_config.CONFIG_FILES))


class Files(Lister):
    """Get list of used files"""
    def get_parser(self, prog_name):
        parser = super(Files, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        files = list_files()

        return (('name', 'path'), ((path.basename(file),
                                    file) for file in files))
