import abc
import fnmatch
import re
from dataclasses import dataclass
from typing import Dict, Callable, Any, Set, Union

# Alias for docs hinting
BeanId = str
BeanInstance = Any
ProfileFunction = Callable[[Set[str]], bool]


class BeanRef(abc.ABC):
    """
    Base class for all bean definitions
    """

    @abc.abstractmethod
    def all_dependencies_satisfied(
            self, ready_beans_ids: Set[BeanId],
            all_beans_ids: Set[BeanId]
    ) -> bool:
        """
        Indicates all dependencies of definition satisfied.
        Children must override this

        @param ready_beans_ids: set of ids of ready beans
        @param all_beans_ids: set of ids of all beans to be initialized
        @return: all dependencies of definition satisfied
        """
        pass

    def need_to_inject(self, all_beans_ids: Set[BeanId]) -> bool:
        """
        Indicates this bean must or not be initialized and used

        @param all_beans_ids: set of ids of all beans to be initialized
        @return: must or not be initialized and used
        """
        return True


class IdBeanRef(BeanRef):
    """
    Bean definition based on it's id
    """

    def __init__(self, bean_id: BeanId, optional=False):
        self.optional = optional
        self.bean_id = bean_id

    def all_dependencies_satisfied(
            self, ready_beans_ids: Set[BeanId],
            all_beans_ids: Set[BeanId]
    ) -> bool:
        if self.bean_id not in all_beans_ids:
            return self.optional
        else:
            return self.bean_id in ready_beans_ids

    def need_to_inject(self, all_beans_ids: Set[BeanId]) -> bool:
        if self.optional:
            return self.bean_id in all_beans_ids
        else:
            return True


class WildcardBeanRef(BeanRef):
    """
    Bean definition based on wildcards
    (see https://en.wikipedia.org/wiki/Glob_(programming)).
    Resulted bean is a set of suitable beans or empty set
    """

    def __init__(self, wildcard: str):
        self.wildcard = wildcard

    def all_dependencies_satisfied(
            self, ready_beans_ids: Set[BeanId],
            all_beans_ids: Set[BeanId]
    ) -> bool:
        required_beans = set(fnmatch.filter(all_beans_ids, self.wildcard))
        return ready_beans_ids >= required_beans


class RegexBeanRef(BeanRef):
    """
    Bean definition based on regex.
    Resulted bean is a set of suitable beans or empty set
    """

    def __init__(self, regex: str):
        self.regex = regex

    def all_dependencies_satisfied(
            self, ready_beans_ids: Set[BeanId],
            all_beans_ids: Set[BeanId]
    ) -> bool:
        required_beans = {bean_id for bean_id in all_beans_ids
                          if re.match(self.regex, bean_id)}
        return ready_beans_ids >= required_beans


# Aliases
id_ref = IdBeanRef
wildcard_ref = WildcardBeanRef
regex_ref = RegexBeanRef

UserGeneralBeanRef = Union[BeanId, BeanRef]


@dataclass
class BeanDef:
    """
    Bean definition class
    """
    bean_id: BeanId
    factory_func: Callable[..., BeanInstance]
    dependencies: Dict[BeanId, BeanRef]
    profile_func: ProfileFunction
