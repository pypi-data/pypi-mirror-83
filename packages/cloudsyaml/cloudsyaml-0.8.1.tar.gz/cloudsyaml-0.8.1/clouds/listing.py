from re import search
from cliff.lister import Lister
from cliff.show import ShowOne
from clouds import arguments
from clouds.sdk import get_clouds
from clouds.sdk import get_one_cloud
from clouds.utils import to_list


def list_clouds(args):
    clouds = get_clouds()

    if args.grep:
        filtered_clouds = clouds
        for grep in args.grep:
            filtered_clouds = list(filter(lambda cloud: search(grep, cloud.name), filtered_clouds))

        return filtered_clouds
    else:
        return clouds


def get_cloud(cloud):
    return get_one_cloud(cloud)


class List(Lister):
    """List clouds from files"""
    formatter_default = 'value'

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)

        parser = arguments.arg_list(parser)
        return parser

    def take_action(self, parsed_args):
        clouds = list_clouds(parsed_args)

        if parsed_args.eval:
            return ('eval',), (("export OS_CLOUD={}".format(cloud.name),) for cloud in clouds)
        else:
            return ('name',), ((cloud.name,) for cloud in clouds)


class Show(ShowOne):
    """Show cloud from files"""
    formatter_default = 'yaml'

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)

        return arguments.arg_show(parser)

    def take_action(self, parsed_args):
        cloud = get_cloud(parsed_args.cloud)

        data = to_list(cloud, parsed_args.detail)

        return ('clouds', ), data
