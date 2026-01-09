"""
Comprehensive test file demonstrating every possible scenario of unused imports in Python.
This file is intentionally filled with unused imports for testing purposes.
"""

# ==============================================================================
# SECTION 1: Basic Unused Imports
# ==============================================================================

# 1.1 Simple unused module import
import os

# 1.2 Simple unused module import (another example)
import sys

# 1.3 Unused import with alias
import numpy as np

# 1.4 Unused import with long alias
import pandas as pd

# 1.5 Multiple unused imports on single line
import json, pickle, shelve

# 1.6 Unused nested/submodule import
import os.path

# 1.7 Unused deeply nested import
import xml.etree.ElementTree

# 1.8 Unused import of package __init__
import collections.abc


# ==============================================================================
# SECTION 2: From Imports (Unused)
# ==============================================================================

# 2.1 Simple from import
from pathlib import Path

# 2.2 From import with alias
from datetime import datetime as dt

# 2.3 Multiple from imports on single line
from typing import List, Dict, Tuple, Set

# 2.4 From import of submodule
from os import path

# 2.5 From import of specific function
from functools import reduce

# 2.6 From import of class
from collections import OrderedDict

# 2.7 From import of constant
from string import ascii_letters

# 2.8 Multiple aliased from imports
from itertools import chain as ch, cycle as cy, repeat as rp

# 2.9 Star import (wildcard) - unused
from enum import *


# ==============================================================================
# SECTION 3: Relative Imports (Unused)
# ==============================================================================

# NOTE: These would cause ImportError if run directly, but represent valid syntax
# Uncomment to test in a package context:

# 3.1 Relative import from current package
# from . import sibling_module

# 3.2 Relative import from parent package
# from .. import parent_module

# 3.3 Relative import specific item
# from .utils import helper_function

# 3.4 Relative import with alias
# from ..config import settings as cfg


# ==============================================================================
# SECTION 4: Conditional/Contextual Unused Imports
# ==============================================================================

# 4.1 Import inside if block (condition always False)
if False:
    import never_imported_module

# 4.2 Import inside try block - unused
try:
    import optional_dependency
except ImportError:
    optional_dependency = None

# 4.3 Import inside try block with fallback - both unused
try:
    import preferred_json as json_lib
except ImportError:
    import json as json_lib

# 4.4 Platform-specific import - unused
import platform
if platform.system() == "Windows":
    import winreg
elif platform.system() == "Linux":
    import fcntl  # type: ignore

# 4.5 Version-specific import - unused
import sys as sys_version_check
if sys_version_check.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated  # type: ignore


# ==============================================================================
# SECTION 5: Type Checking Imports (Often Unused at Runtime)
# ==============================================================================

from typing import TYPE_CHECKING

# 5.1 Import only for type checking - unused even for types
if TYPE_CHECKING:
    from typing import Protocol
    from collections.abc import Callable, Iterator, Generator
    import threading
    from concurrent.futures import Future


# ==============================================================================
# SECTION 6: Shadowed Imports (Import becomes unused due to shadowing)
# ==============================================================================

# 6.1 Import shadowed by local variable assignment
import re
re = "this shadows the import"

# 6.2 Import shadowed by function definition
import math

def math():
    """This function shadows the math import."""
    return 42

# 6.3 Import shadowed by class definition
import abc

class abc:
    """This class shadows the abc import."""
    pass

# 6.4 Import shadowed by for loop variable
import copy
for copy in range(10):
    pass

# 6.5 Import shadowed by with statement
import io
with open(__file__) as io:
    pass

# 6.6 Import shadowed by except clause
import traceback
try:
    raise ValueError()
except ValueError as traceback:
    pass

# 6.7 Import shadowed by comprehension variable (in same scope for walrus)
import itertools
result = [itertools := x for x in range(5)]

# 6.8 Import shadowed in function parameter
from operator import add

def process(add=None):
    """The add parameter shadows the imported add."""
    return add


# ==============================================================================
# SECTION 7: Imports Used Only in Strings/Comments (Still Unused)
# ==============================================================================

# 7.1 Import mentioned only in comment
import hashlib  # hashlib is used for hashing

# 7.2 Import mentioned only in docstring
import hmac
"""
This module uses hmac for message authentication.
hmac.new() is called somewhere.
"""

# 7.3 Import used only in string literal
import base64
some_string = "base64.b64encode() encodes data"

# 7.4 Import used only in f-string
import binascii
description = f"We use binascii for {binascii.__name__} operations... just kidding"
# Note: This one IS actually used due to the f-string evaluation


# ==============================================================================
# SECTION 8: Imports in __all__ (May or may not be considered used)
# ==============================================================================

# 8.1 Import only exported via __all__
import uuid
import secrets

__all__ = ["uuid", "secrets", "main"]


# ==============================================================================
# SECTION 9: Future Imports (Special case - may be unnecessary)
# ==============================================================================

# 9.1 Future imports that might be redundant in Python 3.10+
from __future__ import annotations
from __future__ import division  # Redundant in Python 3
from __future__ import print_function  # Redundant in Python 3
from __future__ import absolute_import  # Redundant in Python 3


# ==============================================================================
# SECTION 10: Imports Used Only in Dead/Unreachable Code
# ==============================================================================

# 10.1 Import used only after return
import decimal

def unreachable_usage():
    return True
    x = decimal.Decimal("1.5")  # Unreachable

# 10.2 Import used only after raise
import fractions

def unreachable_after_raise():
    raise RuntimeError("Always fails")
    f = fractions.Fraction(1, 2)  # Unreachable

# 10.3 Import used only in never-called function
import statistics

def never_called():
    return statistics.mean([1, 2, 3])


# ==============================================================================
# SECTION 11: Partial Usage (Some imports used, others not)
# ==============================================================================

# 11.1 Multiple imports where only some are used
from html import escape, unescape  # Only escape used below

# 11.2 Multiple aliased imports where only some are used
from urllib.parse import quote as q, unquote as uq  # Neither used

# 11.3 Import module but only use submodule
import logging.handlers  # handlers used, logging unused as standalone


# ==============================================================================
# SECTION 12: Imports with Side Effects (Might be intentionally "unused")
# ==============================================================================

# 12.1 Import that registers something (common pattern)
import codecs  # Often imported for side effect of registering codecs

# 12.2 Import that modifies global state
import locale  # Often imported to set locale

# 12.3 Import of test fixtures (common in pytest)
# from conftest import some_fixture  # Would be unused but needed by pytest


# ==============================================================================
# SECTION 13: Metaclass and Decorator Imports
# ==============================================================================

# 13.1 Unused decorator import
from functools import wraps, lru_cache

# 13.2 Unused metaclass import
from abc import ABCMeta, abstractmethod

# 13.3 Unused context manager import
from contextlib import contextmanager, suppress


# ==============================================================================
# SECTION 14: Protocol and Abstract Base Class Imports
# ==============================================================================

# 14.1 Unused Protocol for structural typing
from typing import Protocol as TypingProtocol

# 14.2 Unused ABC imports
from collections.abc import MutableMapping, Sequence, Mapping


# ==============================================================================
# SECTION 15: Third-party Library Patterns (Common unused imports)
# ==============================================================================

# 15.1 Django-style unused imports (would work in Django project)
# from django.db import models
# from django.contrib.auth.models import User

# 15.2 Flask-style unused imports
# from flask import Flask, request, jsonify

# 15.3 Type stub imports
# from numpy.typing import NDArray
# from pandas._typing import DataFrame


# ==============================================================================
# SECTION 16: Import Variations and Edge Cases
# ==============================================================================

# 16.1 Import and immediate delete
import tempfile
del tempfile

# 16.2 Import inside a function (unused within function)
def function_with_unused_import():
    import random
    return 42

# 16.3 Import inside a class (unused within class)
class ClassWithUnusedImport:
    import struct

    def __init__(self):
        pass

# 16.4 Import inside a nested function
def outer():
    def inner():
        import array
        pass
    return inner

# 16.5 Import in lambda (syntax not supported, but demonstrating intent)
# unused_lambda = lambda: __import__('csv')

# 16.6 Multiple imports with some having same base module
import urllib
import urllib.request
import urllib.parse
import urllib.error

# 16.7 Import of the same module multiple times (last one wins)
import warnings
import warnings as warn
import warnings as warning_module

# 16.8 Import with parentheses for multi-line
from dataclasses import (
    dataclass,
    field,
    asdict,
    astuple,
    make_dataclass,
    replace,
    fields,
    is_dataclass,
)

# 16.9 Conditional import with walrus operator (Python 3.8+)
# if (mod := __import__('getpass')):
#     pass  # mod is unused


# ==============================================================================
# SECTION 17: Async/Await Related Imports
# ==============================================================================

# 17.1 Unused asyncio imports
import asyncio
from asyncio import gather, create_task, sleep as async_sleep

# 17.2 Unused async context manager imports
from contextlib import asynccontextmanager

# 17.3 Unused async iterator imports
from collections.abc import AsyncIterator, AsyncGenerator


# ==============================================================================
# SECTION 18: Testing Framework Imports
# ==============================================================================

# 18.1 Unused pytest imports
# import pytest
# from pytest import fixture, mark, raises

# 18.2 Unused unittest imports
import unittest
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch, Mock


# ==============================================================================
# SECTION 19: Namespace Manipulation
# ==============================================================================

# 19.1 Import added to globals but unused
import pprint
globals()['pretty_print'] = pprint.pprint

# 19.2 Import added to locals (doesn't actually work at module level)
import textwrap
# locals()['tw'] = textwrap  # This doesn't persist at module level


# ==============================================================================
# SECTION 20: Type Annotation Only Usage
# ==============================================================================

# 20.1 Import used only in type annotation (string form)
import queue

def get_queue() -> "queue.Queue":
    pass

# 20.2 Import used only in type annotation (direct form)
import multiprocessing

def get_process() -> multiprocessing.Process:
    pass

# 20.3 Import used only in variable annotation
import socket
my_socket: socket.socket


# ==============================================================================
# USED IMPORT (for contrast - this one IS used)
# ==============================================================================

# This import IS used to demonstrate the difference
from html import escape as html_escape

def main():
    """Main function that actually uses one import."""
    dangerous = "<script>alert('xss')</script>"
    safe = html_escape(dangerous)
    print(f"Escaped: {safe}")
    return safe


if __name__ == "__main__":
    main()
