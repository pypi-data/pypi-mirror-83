
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import letsformatError
from .controllers.base import Base
from .controllers.convert import Convert

# configuration defaults
CONFIG = init_defaults('letsformat')
CONFIG['letsformat']['foo'] = 'bar'


class letsformat(App):
    """letsformat primary application."""

    class Meta:
        label = 'letsformat'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Convert
        ]


class letsformatTest(TestApp,letsformat):
    """A sub-class of letsformat that is better suited for testing."""

    class Meta:
        label = 'letsformat'


def main():
    with letsformat() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except letsformatError as e:
            print('letsformatError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
