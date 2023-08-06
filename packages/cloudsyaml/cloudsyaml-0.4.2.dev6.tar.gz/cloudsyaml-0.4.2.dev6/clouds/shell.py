import sys

from clouds import __version__

from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff import complete


class CloudsShell(App):

    def __init__(self):
        super(CloudsShell, self).__init__(
            description='Library and CLI for manage the clouds.yaml',
            version=__version__,
            command_manager=CommandManager('clouds.yaml'),
            deferred_help=True,
        )

    def build_option_parser(self, description, version):
        parser = super(CloudsShell, self).build_option_parser(description, version)

        return parser

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        self.command_manager.add_command('complete', complete.CompleteCommand)

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__)


def main(argv=sys.argv[1:]):
    app = CloudsShell()
    try:
        result = app.run(argv)
    except KeyboardInterrupt:
        print("\nUser request to exit")
    else:
        return result


if __name__ == '__main__':
    exit_code = main(sys.argv[1:])

    sys.exit(exit_code)
