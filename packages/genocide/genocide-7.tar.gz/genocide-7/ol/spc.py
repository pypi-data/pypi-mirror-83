# OLIB - object library
#
#

"""
specification

classes
=======

.. autoclass:: ol.bus.Bus
    :noindex:

..autoclass:: ol.Default
    :noindex:

.. autoclass:: ol.csl.Console
    :noindex:

.. autoclass:: ol.evt.Event
    :noindex:

.. autoclass:: ol.hdl.Handler
    :noindex:

.. autoclass:: ol.krn.Kernel
    :noindex:

.. autoclass:: ol.ldr.Loader
    :noindex:

.. autoclass:: ol.Object
    :noindex:

.. autoclass:: ol.Ol
    :noindex:

functions
=========

.. automethod:: ol.krn.boot
    :noindex:

.. automethod:: ol.bus.bus
    :noindex:

.. automethod:: ol.krn.cmd
    :noindex:

.. automethod:: ol.trm.execute
    :noindex:

.. automethod:: ol.krn.get_kernel
    :noindex:

.. automethod:: ol.tsk.launch
    :noindex:

.. automethod:: ol.prs.parse_cli
    :noindex:

.. automethod:: ol.utl.privileges
    :noindex:

.. automethod:: ol.utl.root
    :noindex:

.. automethod:: ol.krn.scandir
    :noindex:

"""

def __dir__():
    return ("Bus", "Console", "Default", "Event", "Handler", "Kernel", "Loader", "Object", "Ol", "boot", "bus", "cmd", "execute", "get_kernel", "launch", "parse_cli", "privileges", "root", "scandir")

import ol
import os
import pwd
import sys
import time

from ol.bus import Bus, bus
from ol.csl import Console
from ol.evt import Event
from ol.hdl import Handler
from ol.krn import Kernel, boot, cmd, get_kernel, scandir
from ol.ldr import Loader
from ol.prs import parse, parse_cli
from ol.tsk import launch
from ol.trm import execute
from ol.utl import privileges, root
