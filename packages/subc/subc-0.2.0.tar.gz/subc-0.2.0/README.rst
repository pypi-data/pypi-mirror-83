subc
====

This is a tiny library to help you write CLI applications with many
sub-commands.

Installation
------------

``pip install subc``

Use
---

Create your own command subclass for your application:


.. code:: python

    class MyCmd(subc.Command):
        pass

Then, write commands in your application which sub-class this:

.. code:: python

    class HelloWorld(MyCmd):
        name = 'hello-world'
        description = 'say hello'
        def run(self):
            print('hello world')

Finally, use your application-level subclass for creating the argument parser
and running your application:

.. code:: python

    if __name__ == '__main__':
        MyCmd.main()

Advanced Use
------------

You may find yourself wanting to create intermediate subclasses for your
application, in order to share common functionality. For example, you might
create a class for all commands which handle a single file as an argument:

.. code:: python

    class FileCmd(MyCmd):
        def add_args(self, parser):
            parser.add_args('file', help='the single file')

You can do that, so long as your intermediate subclasses are not executable. For
example, given the following class hierarchy:

.. code::

    MyCmd*
    |- FileCmd*
    |  |- AppendLineCmd
    |  |- RemoveLineCmd
    |- DoSomethingElseCmd

The non-leaf commands (marked with an asterisk) will not be included as
executable commands. Only leaf classes will be executable.

``subc`` is a very simple library. If you have other advanced uses, read the
code.

License
-------

This project is released under the Revised BSD license.  See ``LICENSE.txt`` for
details.
