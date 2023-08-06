import inspect
from pathlib import Path
from types import ModuleType
from typing import Dict, Any, Callable, Type, Set, List

import yaml

from pybeandi.beans_list import BeansList
from pybeandi.config import Configuration
from pybeandi.decorators import BeanMeta, AfterInitMeta
from pybeandi.errors import ContextInitError
from pybeandi.model import (
    BeanDef, id_ref, UserGeneralBeanRef, BeanId, BeanInstance
)
from pybeandi.util import setup_yaml_env_vars, all_callable_of_object


class BeanContext:
    """
    Main class of pybeandi.
    Links all beans to each other and controls theirs lifecycle
    """
    bean_defs: Dict[BeanId, BeanDef]
    beans: BeansList
    profiles: Set[str]

    closed: bool = False

    def __init__(self, bean_defs: Dict[BeanId, BeanDef], profiles: Set[str]):
        self._bean_defs: Dict[BeanId, BeanDef] = bean_defs
        self._beans: BeansList = BeansList()
        self._profiles = profiles

    @property
    def beans(self):
        return self._beans

    @property
    def profiles(self):
        return self._profiles

    def init(self) -> None:
        """
        Initialize context using bean definitions provided earlier

        @raise ContextInitError: is context incorrect
        """
        self._bean_defs = {bean_id: bean_def for (bean_id, bean_def) in
                           self._bean_defs.items()
                           if bean_def.profile_func(self.profiles)}
        all_beans_ids = set(self._bean_defs.keys())

        while any(bean_id not in self.beans for bean_id in self._bean_defs):
            # Get all uninitialized beans
            to_init: List[BeanDef] = [bean_def for (bean_id, bean_def) in
                                      self._bean_defs.items()
                                      if bean_id not in self.beans]
            # Filter all beans with unsatisfied dependencies
            to_init = [
                bean_def for bean_def in to_init
                if all(
                    dep_ref.all_dependencies_satisfied(
                        self.beans.ids(), all_beans_ids
                    ) for dep_ref in bean_def.dependencies.values()
                )
            ]

            if len(to_init) == 0:
                raise ContextInitError(
                    'Circular or missing dependency was founded'
                )

            for bean_def in to_init:
                beans_to_insert = {arg_name: self.beans[arg_bean_ref]
                                   for (arg_name, arg_bean_ref)
                                   in bean_def.dependencies.items()
                                   if
                                   arg_bean_ref.need_to_inject(all_beans_ids)}
                bean = bean_def.factory_func(**beans_to_insert)
                self.beans._add_as_bean(bean_def.bean_id, bean)

        self._process_after_init()

    # with ctx_builder.init() as ctx:
    # Syntax support, features later
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _process_after_init(self):
        bean_ids = set(self._bean_defs.keys())

        for bean in self.beans.values():
            for after_init_func in filter(
                    lambda func: '_bean_meta' in dir(func),
                    all_callable_of_object(bean)):
                after_init_meta: AfterInitMeta = after_init_func._bean_meta

                beans_to_insert = {arg_name: self.beans[arg_bean_ref]
                                   for (arg_name, arg_bean_ref)
                                   in after_init_meta.depends_on.items()
                                   if arg_bean_ref.need_to_inject(bean_ids)}
                after_init_func(**beans_to_insert)


class BeanContextBuilder:
    """
    Builder for BeanContext
    """
    def __init__(self):
        self._scanned: Set = set()
        self.bean_defs: List[BeanDef] = []
        self.profiles = set()

    def init(self) -> BeanContext:
        """
        Create BeanContext from defined settings

        @raise ContextInitError: context configuration error
        @return: BeanContext
        """
        # Check id duplication
        bean_defs = [bean_def for bean_def in self.bean_defs
                     if bean_def.profile_func(self.profiles)]

        bean_ids = [bean_def.bean_id for bean_def in bean_defs]
        duplicate_ids = set([x for x in bean_ids if bean_ids.count(x) > 1])
        if len(duplicate_ids) > 0:
            raise ContextInitError(
                f'Multiple beans with same id exist: '
                f'{", ".join(duplicate_ids)}')

        bean_defs = {bean_def.bean_id: bean_def for bean_def in bean_defs}

        ctx = BeanContext(bean_defs, self.profiles)
        ctx.init()
        return ctx

    def load_config(self, config: Configuration):
        """
        Loads config to builder. Usually it's used inside lib

        @param config: Configuration object
        """
        if config.profiles is not None:
            if not all(profile in self.profiles
                       for profile in config.profiles):
                return
        if config.beans is not None:
            for bean_id, bean_instance in config.beans.items():
                self.add_as_bean(bean_id, bean_instance)

    def load_yaml(self, path: Path) -> None:
        """
        Load configuration from specified file

        @param path: YAML config file
        """

        loader = setup_yaml_env_vars(yaml.SafeLoader)

        with open(path, 'r', encoding='utf-8') as file:
            for yaml_raw in yaml.load_all(file, loader):
                if 'pybeandi' not in yaml_raw:
                    return
                config_raw = yaml_raw['pybeandi']

                config = Configuration.from_dict(config_raw)
                self.load_config(config)

    def import_module(self, module: ModuleType):
        """
        Imports all declared beans from module.
        (usually module is 'import <module_name>' object
        or sys.modules[__name__])

        @param module: module with beans
        """
        for name, member in inspect.getmembers(
                module,
                lambda m: (inspect.isclass(m) or callable(
                    m)) and '_bean_meta' in dir(m)):
            if member in self._scanned:
                continue
            else:
                self._scanned.add(member)
            self.register_bean_by_class(member)

    def register_bean(self,
                      bean_id: BeanId,
                      factory_func: Callable[..., Any],
                      dependencies: Dict[str, UserGeneralBeanRef],
                      profile_func: Callable[[Set[str]], bool]
                      = lambda profs: True) -> None:
        """
        Register bean to be created at init phase

        @param bean_id: id of registered bean
        @param factory_func: function or class that returns object of bean
        @param dependencies: dictionary of names of factory_func arg to
        reference to bean
        @param profile_func: function that returns do context need to create
        bean
        """
        dependencies = {
            arg_name: (
                id_ref(arg_ref)
                if isinstance(arg_ref, BeanId)
                else arg_ref
            )
            for (arg_name, arg_ref) in dependencies.items()}

        self.bean_defs.append(
            BeanDef(bean_id, factory_func, dependencies, profile_func))

    def register_bean_by_class(self, cls: Type) -> None:
        """
        Register bean to be created at init phase by class.
        Class must be decorated by @bean first!

        @param cls: class of bean
        """
        bean_meta: BeanMeta = cls._bean_meta

        self.register_bean(
            bean_meta.bean_id,
            bean_meta.cls,
            bean_meta.depends_on,
            bean_meta.profile_func
        )

    def add_as_bean(self, bean_id: BeanId, bean_instance: BeanInstance):
        """
        Add object as a simple bean (without dependencies). Useful for configs

        @param bean_id: bean id
        @param bean_instance: object
        """
        self.register_bean(bean_id, lambda: bean_instance, {})
