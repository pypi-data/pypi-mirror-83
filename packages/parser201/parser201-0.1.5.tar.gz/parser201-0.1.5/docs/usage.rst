=====
Usage
=====

To use parser201 in a project::

    from parser201 import LogParser

The most common use-case will be importing individual lines from an Apache log file and building `LogParser` objects, like this:

.. code-block:: python

   from parser201 import LogParser

   f = open('apache.log','r')
   for line in f:
      lp = LogParser(line)
      # Use lp as desired: add to List, Dictionary, etc.
      ...

