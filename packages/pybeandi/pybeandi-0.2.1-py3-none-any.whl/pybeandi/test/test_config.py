from pathlib import Path

import pytest

from pybeandi.config import Configuration
from pybeandi.context import BeanContextBuilder
from pybeandi.errors import ContextInitError

CONFIG_1 = Configuration(['profile1'], {'message': 'Message from profile1'})
CONFIG_2 = Configuration(['profile2'], {'message': 'Message from profile2'})


def test_ctx_config_without_profile(ctx_builder: BeanContextBuilder):
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with ctx_builder.init() as ctx:
        assert 'message' not in ctx.beans


def test_ctx_config_with_profile1(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with ctx_builder.init() as ctx:
        assert 'message' in ctx.beans
        assert ctx.beans['message'] == 'Message from profile1'


def test_ctx_config_with_both_profiles(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    ctx_builder.profiles.add('profile2')
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with pytest.raises(ContextInitError):
        with ctx_builder.init():
            pass


def test_ctx_config_yaml(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    ctx_builder.load_yaml(Path('pybeandi', 'test', 'test_config.yaml'))
    with ctx_builder.init() as ctx:
        assert 'message' in ctx.beans
        assert ctx.beans['message'] == 'Message from yaml file config'


def test_ctx_config_yaml_not_exists(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    with pytest.raises(FileNotFoundError):
        ctx_builder.load_yaml(Path('pybeandi', 'test', 'test_config1.yaml'))
