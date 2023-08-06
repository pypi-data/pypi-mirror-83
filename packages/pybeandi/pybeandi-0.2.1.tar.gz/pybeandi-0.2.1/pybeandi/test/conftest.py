import sys

import pytest

from pybeandi.context import BeanContextBuilder
from pybeandi.decorators import bean


@bean(bean_id='class_based_bean')
class ClassBasedBean:

    def __init__(self):
        pass


@bean(bean_id='func_based_bean')
def func_bean():
    return 'func'


@pytest.fixture()
def ctx_builder():
    ctx_builder = BeanContextBuilder()
    ctx_builder.add_as_bean('1', 1)
    ctx_builder.add_as_bean('2', 2)
    ctx_builder.add_as_bean('3', 3)
    ctx_builder.import_module(sys.modules[__name__])
    return ctx_builder
