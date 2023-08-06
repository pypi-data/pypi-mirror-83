# coding=utf-8

import re
from jinja2 import Environment, PackageLoader
from .pb import pasteboard_write
from .command import Command
from .constants import DART_TYPES_DEFAULT_VALUES, DART_TYPES
from .str_helpers import upper_first_letter


class MockCommand(Command):
    def __init__(self, abstract_text):
        super(MockCommand, self).__init__()
        self.abstract_text = abstract_text

    def create_mock(self, print_result):
        output = Mock(self.abstract_text).create_mock()
        if print_result:
            print()
            print(output)
            print()
        pasteboard_write(output)
        print('The result has been copied to the pasteboard.')


class Mock(object):

    class Function(object):
        def __init__(self, origin, name, params, return_type):
            super(Mock.Function, self).__init__()
            self.origin = origin
            self.name = name
            self.params = list(filter(None, params.split(',')))
            self.return_type = return_type
            self.is_overloaded = False

        def __str__(self):
            return self.origin

        @property
        def return_value(self):
            if self.return_type is None:
                return_value = '()'
            if self.return_type == 'void':
                return_value = '()'
            elif self.return_type.endswith('?'):
                return_value = 'nil'
            elif self.return_type.startswith('Stream'):
                regex = re.compile('Stream<(.+)>')
                mo = regex.search(self.return_type)
                stream_type = mo.group(1)
                return_value = 'Stream<{}>.value(null)'.format(
                    stream_type
                )
            elif self.return_type in DART_TYPES:
                return_value = DART_TYPES_DEFAULT_VALUES[self.return_type]
            else:
                return_value = '{}()'.format(self.return_type)
            return return_value

        @property
        def return_void(self):
            return self.return_type is None or self.return_type == 'void'

        @property
        def return_nil(self):
            return self.return_value == 'nil'

        @property
        def first_param(self):
            if self.params:
                param = self.params[0]
                param_name = param.split(':')[0].split(' ')
                return param_name[0] \
                    + "".join(x.title() for x in param_name[1:])
            return None

        @property
        def first_param_title(self):
            if self.first_param is not None:
                return upper_first_letter(self.first_param)
            return None

        @property
        def overloaded_name(self):
            if self.is_overloaded and (self.first_param_title is not None):
                return self.name + self.first_param_title
            return self.name

    def __init__(self, abstract_text):
        super(Mock, self).__init__()
        self.abstract_text = abstract_text

    def _get_abstract_name(self, str):
        regex = re.compile(r'abstract class (\w+)')
        mo = regex.search(str)
        abstract_name = mo.group(1)
        if abstract_name.endswith('Type'):
            class_name = abstract_name[:-4]
        else:
            class_name = abstract_name
        return (abstract_name, class_name)

    def create_mock(self):
        str = self.abstract_text
        is_abstract = False
        abstract_name = ''
        class_name = ''
        # get abstract name
        try:
            (abstract_name, class_name) = self._get_abstract_name(str)
            is_abstract = True
        except Exception:
            pass
        # get functions
        func_regex = re.compile(r'  (.*) (.*)\((.*)\)')
        funcs = [Mock.Function(f.group(), f.group(2), f.group(3), f.group(1))
                 for f in func_regex.finditer(str)]

        if not funcs:
            print('The abstract or functions in the pasteboard is invalid.')
            exit(1)

        # check if overloaded
        func_dict = {}
        for f in funcs:
            if f.name in func_dict:
                func_dict[f.name] = func_dict[f.name] + 1
            else:
                func_dict[f.name] = 1
        for f in funcs:
            f.is_overloaded = func_dict[f.name] > 1

        env = Environment(
            loader=PackageLoader('ptfgen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template("mock.dart")
        content = template.render(
            class_name=class_name,
            abstract_name=abstract_name,
            functions=funcs,
            is_abstract=is_abstract
        )
        return content
