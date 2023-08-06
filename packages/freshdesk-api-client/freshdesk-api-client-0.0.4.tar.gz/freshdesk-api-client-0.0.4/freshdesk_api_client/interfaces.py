# -*- coding: utf-8 -*-

import abc


class GettableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_item(self, code_or_item):
        pass

class SearchableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def search(self, query):
        pass    

class ListableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def fetch_list(self, args=None):
        pass

class CreatableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def create_item(self, item):
        pass

class UpdatableResourceInterface(abc.ABC):
    # @abc.abstractmethod
    def update_create_item(self, item_values, code=None):
        pass

class DeletableResourceInterface(abc.ABC):
    @abc.abstractmethod
    def delete_item(self, code_or_item):
        pass
