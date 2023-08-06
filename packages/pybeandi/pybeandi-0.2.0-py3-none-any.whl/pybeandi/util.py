import inspect
import os
import re
from typing import Any, Callable, Generator, Set

from pybeandi.model import ProfileFunction


def camel_case_to_snake_case(camel_case: str) -> str:
    """
    Convert ClassLikeCase to variable_like_case
    Source: https://stackoverflow.com/a/1176023/8312205
    @param camel_case: ClassLikeCase
    @return: variable_like_case
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case).lower()


def setup_yaml_env_vars(base_loader, tag='!ENV'):
    """
    Environment variables processing from
    https://medium.com/swlh/python-yaml-configuration-with-environment-variables-parsing-77930f4273ac
    """

    # pattern for global vars: look for ${word}
    pattern = re.compile(r'.*?\${(\w+)}.*?')

    # the tag will be used to mark where to start searching for the pattern
    # e.g. somekey: !ENV somestring${MYENVVAR}blah blah blah
    base_loader.add_implicit_resolver(tag, pattern, None)

    def constructor_env_variables(loader, node):
        """
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

    base_loader.add_constructor(tag, constructor_env_variables)
    return base_loader


def all_callable_of_object(obj: Any) -> Generator[Callable, None, None]:
    """
    Yields all methods of object
    @param obj:
    @return:
    """
    for name, func in inspect.getmembers(obj, inspect.ismethod):
        yield func


def all_active(required_profiles: Set[str]) -> ProfileFunction:
    """
    Checks all required profiles are active

    @param required_profiles: required profiles
    @return: function for profile_func
    """
    return lambda active_profiles: active_profiles >= required_profiles


def is_active(required_profile: str) -> ProfileFunction:
    """
    Check this profile is active

    @param required_profile: profile that must be active
    @return: function for profile_func
    """
    return lambda active_profiles: required_profile in active_profiles


def is_not_active(required_profile: str) -> ProfileFunction:
    """
    Check this profile is not active

    @param required_profile: profile that must be not active
    @return: function for profile_func
    """
    return lambda active_profiles: required_profile not in active_profiles
