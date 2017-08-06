# -*- coding: utf-8 -*-
# lsys tests init
from pkg_resources import resource_filename

import pytest

import lsys

from . import *

def test(*args): # pragma: no cover
    options = [resource_filename('lsys', 'tests')]
    options.extend(list(args))
    return pytest.main(options)
