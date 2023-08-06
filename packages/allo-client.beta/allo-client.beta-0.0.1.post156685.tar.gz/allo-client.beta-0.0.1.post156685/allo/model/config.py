# -*- coding: utf-8 -*-
import pickle
import os

from allo.model.version import Version
from allo.const import CONFIG_PATH


class AlloConfig:
    id: int
    id_client: str
    code_produit: str
    teleport_token: str
    env: str
    repo_path: str
    version: Version
    internal: bool = False

    @staticmethod
    def load():
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'rb') as config_dictionary_file:
                return pickle.load(config_dictionary_file)
        else:
            return AlloConfig()

    def save(self):
        with open(CONFIG_PATH, 'wb') as config_dictionary_file:
            pickle.dump(self, config_dictionary_file)
