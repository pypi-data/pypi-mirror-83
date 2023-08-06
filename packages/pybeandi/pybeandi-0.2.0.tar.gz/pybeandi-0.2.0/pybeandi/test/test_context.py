import pytest

from pybeandi.context import BeanContextBuilder
from pybeandi.errors import NoSuchBeanError, ContextInitError
from pybeandi.model import id_ref, wildcard_ref, regex_ref, BeanId
from pybeandi.test import beans_with_inject
from pybeandi.test.beans_with_inject import ClassInjectBean
from pybeandi.test.conftest import ClassBasedBean
from pybeandi.util import all_active, is_active, is_not_active


def test_init(ctx_builder: BeanContextBuilder):
    with ctx_builder.init() as ctx:
        assert set(ctx.beans.ids()) == {'1', '2', '3', 'class_based_bean',
                                        'func_based_bean'}


def test_init_with_duplicates(ctx_builder: BeanContextBuilder):
    ctx_builder.add_as_bean('1', -1)
    with pytest.raises(ContextInitError):
        with ctx_builder.init():
            pass


def test_init_inject_class(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)
    with ctx_builder.init() as ctx:
        assert isinstance(
            ctx.beans[id_ref('bean_with_inject')], ClassInjectBean
        )


def test_init_inject_func(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('func_based')
    ctx_builder.import_module(beans_with_inject)
    with ctx_builder.init() as ctx:
        assert isinstance(ctx.beans[id_ref('bean_with_inject')], BeanId)


def test_init_inject_manual(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('manual')
    ctx_builder.register_bean(
        'manual_inject',
        lambda id_num_1, wildcard_nums, regex_nums, default_none=None:
        (id_num_1, wildcard_nums, regex_nums, default_none),
        {
            'id_num_1': '1',
            'wildcard_nums': wildcard_ref('[123]'),
            'regex_nums': regex_ref(r'^[1-3]$'),
        },
        lambda profs: 'manual' in profs
    )
    with ctx_builder.init() as ctx:
        assert ctx.beans[id_ref('manual_inject')] == (
            1, {1, 2, 3}, {1, 2, 3}, None
        )


def test_multiple_module_import(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)
    ctx_builder.import_module(beans_with_inject)
    with ctx_builder.init():
        pass


def test_id_ref(ctx_builder: BeanContextBuilder):
    with ctx_builder.init() as ctx:
        assert ctx.beans[id_ref('1')] == ctx.beans['1'] == 1
        assert ctx.beans[id_ref('2')] == ctx.beans['2'] == 2
        assert ctx.beans[id_ref('3')] == ctx.beans['3'] == 3
        assert isinstance(
            ctx.beans[id_ref('class_based_bean')], ClassBasedBean
        )
        assert isinstance(
            ctx.beans[id_ref('func_based_bean')], BeanId
        )

        with pytest.raises(NoSuchBeanError):
            empty = ctx.beans['empty']  # noqa F841

        assert '1' in ctx.beans and id_ref('1') in ctx.beans
        assert '2' in ctx.beans and id_ref('2') in ctx.beans
        assert '3' in ctx.beans and id_ref('3') in ctx.beans
        assert 'class_based_bean' in ctx.beans and id_ref(
            'class_based_bean') in ctx.beans
        assert 'func_based_bean' in ctx.beans and id_ref(
            'func_based_bean') in ctx.beans
        assert 'empty' not in ctx.beans and id_ref('empty') not in ctx.beans


def test_wildcard_ref(ctx_builder: BeanContextBuilder):
    with ctx_builder.init() as ctx:
        assert ctx.beans[wildcard_ref('[123]')] == {1, 2, 3}
        assert ctx.beans[wildcard_ref('[13]')] == {1, 3}
        assert ctx.beans[wildcard_ref('empty')] == set()
        for bean in ctx.beans[wildcard_ref('class_based_*')]:
            assert isinstance(bean, ClassBasedBean)
        for bean in ctx.beans[wildcard_ref('func_based_*')]:
            assert isinstance(bean, BeanId)


def test_regex_ref(ctx_builder: BeanContextBuilder):
    with ctx_builder.init() as ctx:
        assert ctx.beans[regex_ref(r'^[1-3]$')] == {1, 2, 3}
        assert ctx.beans[regex_ref(r'^[13]$')] == {1, 3}
        assert ctx.beans[regex_ref(r'empty')] == set()
        for bean in ctx.beans[regex_ref(r'class_based_.+')]:
            assert isinstance(bean, ClassBasedBean)
        for bean in ctx.beans[regex_ref(r'func_based_.+')]:
            assert isinstance(bean, BeanId)


def test_optional_without_bean(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)

    with ctx_builder.init() as ctx:
        assert 'optional_id' not in ctx.beans
        assert ctx.beans['bean_with_inject'].optional_arg is None


def test_optional_with_bean(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)

    ctx_builder.add_as_bean('optional_id', True)
    with ctx_builder.init() as ctx:
        assert ctx.beans['optional_id'] is True
        assert ctx.beans['bean_with_inject'].optional_arg is True


def test_optional_after_init_without_bean(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)

    with ctx_builder.init() as ctx:
        assert 'optional_id' not in ctx.beans
        assert ctx.beans['bean_with_inject'].optional_setted is False


def test_optional_after_init_with_bean(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('class_based')
    ctx_builder.import_module(beans_with_inject)

    ctx_builder.add_as_bean('optional_id', True)
    with ctx_builder.init() as ctx:
        assert ctx.beans['optional_id'] is True
        assert ctx.beans['bean_with_inject'].optional_setted is True


def test_profile_func_all_active():
    ctx_builder = BeanContextBuilder()
    ctx_builder.register_bean(
        bean_id='bean_profile1',
        factory_func=lambda: None,
        dependencies={},
        profile_func=all_active({'profile1'}),
    )
    ctx_builder.register_bean(
        bean_id='bean_profile1_2',
        factory_func=lambda: None,
        dependencies={},
        profile_func=all_active({'profile1', 'profile2'}),
    )

    with ctx_builder.init() as ctx:
        assert 'bean_profile1' not in ctx.beans
        assert 'bean_profile1_2' not in ctx.beans

    ctx_builder.profiles.add('profile1')
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' in ctx.beans
        assert 'bean_profile1_2' not in ctx.beans

    ctx_builder.profiles.add('profile2')
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' in ctx.beans
        assert 'bean_profile1_2' in ctx.beans


def test_profile_func_is_active():
    ctx_builder = BeanContextBuilder()
    ctx_builder.register_bean(
        bean_id='bean_profile1',
        factory_func=lambda: None,
        dependencies={},
        profile_func=is_active('profile1'),
    )
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' not in ctx.beans

    ctx_builder.profiles.add('profile1')
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' in ctx.beans


def test_profile_func_is_not_active():
    ctx_builder = BeanContextBuilder()
    ctx_builder.register_bean(
        bean_id='bean_profile1',
        factory_func=lambda: None,
        dependencies={},
        profile_func=is_not_active('profile1'),
    )
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' in ctx.beans

    ctx_builder.profiles.add('profile1')
    with ctx_builder.init() as ctx:
        assert 'bean_profile1' not in ctx.beans
