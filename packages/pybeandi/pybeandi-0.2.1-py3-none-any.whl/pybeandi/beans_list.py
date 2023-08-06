import fnmatch
import re
from typing import Set, Mapping, Any, Sized, Iterable, Tuple, Union, Iterator

from pybeandi.errors import (
    NoSuchBeanError, MultipleBeanInstancesError,
    BeanIdAlreadyExistsError
)
from pybeandi.model import (
    WildcardBeanRef, IdBeanRef, UserGeneralBeanRef,
    RegexBeanRef, BeanId, BeanInstance
)


class BeansList(
    Mapping[UserGeneralBeanRef, BeanInstance],
    Sized,
    Iterable[Tuple[BeanId, BeanInstance]],
):
    """
    Readonly dictionary-like object to access beans
    """

    def __init__(self, beans=None):
        if beans is None:
            beans = {}
        self._beans = beans

    def get_bean_by_id(self, bean_id: BeanId) -> BeanInstance:
        """
        Return bean from context by its id

        @param bean_id: id of bean
        @return: bean
        @raise NoSuchBeanError: if such bean does not exist
        """
        if bean_id not in self._beans:
            raise NoSuchBeanError(f'Bean with id \'{bean_id}\' does not exist')
        return self._beans[bean_id]

    def get_beans_by_wildcard(self, wildcard: str) -> Set[BeanInstance]:
        needed_ids = fnmatch.filter(self.ids(), wildcard)
        return {self[bean_id] for bean_id in needed_ids}

    def get_beans_by_regex(self, regex: str) -> Set[BeanInstance]:
        needed_ids = (bean_id for bean_id in self.ids()
                      if re.match(regex, bean_id))
        return {self[bean_id] for bean_id in needed_ids}

    def _add_as_bean(
            self, bean_id: BeanId, bean_instance: BeanInstance
    ) -> None:
        """
        Register obj as bean

        @param bean_id: id of new bean
        @param bean_instance: object to register as a bean
        """
        if bean_id in self._beans:
            raise BeanIdAlreadyExistsError(
                f'Bean with id \'{bean_id}\' already exists')
        self._beans[bean_id] = bean_instance

    def values(self):
        return self._beans.values()

    def ids(self):
        return self._beans.keys()

    def items(self):
        return self._beans.items()

    def __contains__(self, bean_ref: Any) -> bool:
        """
        Checks do bean exists by its reference

        @param bean_ref: reference
        @return: do bean exists
        """

        try:
            self[bean_ref]
        except NoSuchBeanError:
            return False
        except MultipleBeanInstancesError:
            return True
        return True

    def __getitem__(
            self, bean_ref: UserGeneralBeanRef
    ) -> Union[BeanInstance, Set[BeanInstance]]:
        """
        General method that returns beans by any type of reference
        (id, BeanRef instance)

        @param bean_ref: id or BeanRef instance
        @return: bean or set of beans, depends on :bean_ref: type
        """
        if isinstance(bean_ref, BeanId):
            return self.get_bean_by_id(bean_ref)
        if isinstance(bean_ref, IdBeanRef):
            return self.get_bean_by_id(bean_ref.bean_id)
        if isinstance(bean_ref, WildcardBeanRef):
            return self.get_beans_by_wildcard(bean_ref.wildcard)
        if isinstance(bean_ref, RegexBeanRef):
            return self.get_beans_by_regex(bean_ref.regex)
        raise ValueError(f'Invalid bean reference {bean_ref}')

    def __len__(self) -> int:
        return len(self._beans)

    def __iter__(self) -> Iterator[Tuple[BeanId, BeanInstance]]:
        return iter(self._beans)
