from typing import List

from abc import ABC, abstractmethod


class BaseVariable(ABC):
    name: str

    @abstractmethod
    def replace(self, value):
        pass


class BaseDocument(ABC):
    @abstractmethod
    def __init__(self, file_or_path):
        pass

    @abstractmethod
    def find_variables(self) -> List[BaseVariable]:
        pass

    @abstractmethod
    def save(self, target):
        pass