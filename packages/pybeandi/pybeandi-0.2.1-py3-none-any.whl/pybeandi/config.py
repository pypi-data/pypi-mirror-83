from dataclasses import dataclass
from typing import List, Optional, Dict

from mashumaro import DataClassDictMixin

from pybeandi.model import BeanId, BeanInstance


@dataclass
class Configuration(DataClassDictMixin):
    """
    Generic configuration class
    """
    profiles: Optional[List[str]] = None
    beans: Optional[Dict[BeanId, BeanInstance]] = None
