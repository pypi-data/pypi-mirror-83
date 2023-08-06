# PYTHON_ARGCOMPLETE_OK

import sys
from arghandler import subcmd, ArgumentHandler

from . import __version__
from .pb import pasteboard_read
from .api_cmd import APICommand
from .mock_cmd import MockCommand
from .json_cmd import JSONCommand
from .test_cmd import UnitTestCommand
from .bind_cmd import BindViewModelCommand
from .template_cmd import TemplateCommand


@subcmd('template', help='create template files for a scene')
def cmd_template(parser, context, args):
    parser.description = 'Create template files for a scene.'

    parser.add_argument(
        'type',
        nargs=1,
        choices=[
            'base'
        ],
        help="template type"
    )

    parser.add_argument(
        'name',
        nargs=1,
        help='scene name'
    )

    args = parser.parse_args(args)
    template_name = args.type[0]
    scene_name = args.name[0]

    options = {}

    TemplateCommand(template_name, scene_name, options).create_files()


@subcmd('mock', help='create a mock class for a protocol/function')
def cmd_mock(parser, context, args):
    parser.usage = '''copy the protocol/function to the pasteboard then run: ptfgen mock [-h] [-p]'''
    parser.description = 'Create a mock class for a protocol/function.'
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    protocol_text = pasteboard_read()
    MockCommand(protocol_text).create_mock(args.print)


@subcmd('test', help='create unit tests for a view model')
def cmd_test(parser, context, args):
    parser.usage = '''copy the view model to the pasteboard then run: ptfgen test [-h] [-p]'''
    parser.description = 'Create unit tests for a view model.'
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    vm_text = pasteboard_read()
    UnitTestCommand(vm_text).create_tests(args.print)


@subcmd('bind', help='create a bindViewModel method for a UIViewController')
def cmd_bind(parser, context, args):
    parser.usage = '''copy the view model to the pasteboard then run: ptfgen bind [-h] [-p]'''
    parser.description = '''Create a bindViewModel method for a UIViewController.'''
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    vm_text = pasteboard_read()
    BindViewModelCommand(vm_text).create_bind_view_model(args.print)


@subcmd('json', help='create a model from JSON')
def cmd_json(parser, context, args):
    parser.usage = '''copy the JSON to the pasteboard then run: ptfgen json [-h] [-p] name'''
    parser.description = 'Create a model from JSON.'
    parser.add_argument(
        'name',
        nargs=1,
        help='model name'
    )
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    json = pasteboard_read()
    JSONCommand(args.name[0], json).create_models(args.print)


@subcmd('api', help='create input and output files for an API')
def cmd_api(parser, context, args):
    parser.description = 'Create input and output files for an API.'
    parser.add_argument(
        'name',
        nargs=1,
        help='api name'
    )
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    APICommand(args.name[0]).create_api(args.print)


def main():
    handler = ArgumentHandler(
        use_subcommand_help=True,
        enable_autocompletion=True,
        epilog='Get help on a subcommand: ptfgen subcommand -h'
    )

    handler.add_argument(
        '-v', '--version',
        action='version',
        version=__version__,
        help='show the version number'
    )

    # if no parameters are provided, show help
    if len(sys.argv) == 1:
        handler.run(['-h'])
    else:
        handler.run()


if __name__ == '__main__':
    main()
