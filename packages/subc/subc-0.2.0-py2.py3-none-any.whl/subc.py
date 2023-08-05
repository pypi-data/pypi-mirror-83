#!/usr/bin/env python3
"""
A simple sub-command library for writing rich CLIs
"""
import argparse
import collections
from abc import ABC
from abc import abstractproperty
from abc import abstractmethod


class Command(ABC):
    """
    A simple class for implementing sub-commands in your command line
    application. Create a subclass for your app as follows:

        class MyCmd(subc.Command):
            pass

    Then, each command in your app can subclass this, implementing the three
    required fields:

        class HelloWorld(MyCmd):
            name = 'hello-world'
            description = 'say hello'
            def run(self):
                print('hello world')

    Finally, use your app-level subclass for creating an argument parser:

        def main():
            parser = argparse.ArgumentParser(description='a cool tool')
            MyCmd.add_commands(parser)
            args = parser.parse_args()
            args.func(args)
    """

    @abstractproperty
    def name(self):
        # type: () -> str
        pass

    @abstractproperty
    def description(self):
        # type: () -> str
        pass

    def add_args(self, parser):
        # type: (argparse.ArgumentParser) -> None
        pass  # default is no arguments

    @abstractmethod
    def run(self):
        # type: () -> None
        pass

    def base_run(self, args):
        # type: (argparse.Namespace) -> None
        self.args = args
        return self.run()

    @classmethod
    def add_commands(cls, parser):
        # type: (argparse.ArgumentParser) -> None
        subparsers = parser.add_subparsers(title='sub-command')
        subclasses = collections.deque(cls.__subclasses__())
        while subclasses:
            subcls = subclasses.popleft()
            this_node_subclasses = subcls.__subclasses__()
            if this_node_subclasses:
                # Assume that any class with children is not executable. Add
                # its children to the queue (BFS) but do not instantiate it.
                subclasses.extend(this_node_subclasses)
            else:
                cmd = subcls()
                cmd_parser = subparsers.add_parser(
                    cmd.name, description=cmd.description
                )
                cmd.add_args(cmd_parser)
                cmd_parser.set_defaults(func=cmd.base_run)

        def default(*args, **kwargs):
            raise Exception('you must select a sub-command')
        parser.set_defaults(func=default)
        return parser

    @classmethod
    def main(cls, description):
        # type: (str) -> None
        parser = argparse.ArgumentParser(description=description)
        cls.add_commands(parser)
        args = parser.parse_args()
        args.func(args)
