#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests import Response
from uuid import getnode
from ..const import *
from ..model.colors import BColors


class API:
    @staticmethod
    def find_instance():
        with open(ALLO_INFO_PATH, 'rb') as payload:
            r = requests.post("{}/referees/{}".format(API_PATH, getnode()), verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.json()

    @staticmethod
    def get_secret():
        r = requests.get("{}/referees/{}/secret".format(API_PATH, getnode()), verify=False)
        if API.has_error(r):
            return False
        return r.text

    @staticmethod
    def ask_install():
        with open(ALLO_INFO_PATH, 'rb') as payload:
            r = requests.post("{}/referees/{}/install".format(API_PATH, getnode()), verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.text

    @staticmethod
    def get_versions():
        r = requests.get("{}/referees/{}/versions".format(API_PATH, getnode()), verify=False)
        if API.has_error(r):
            return False
        return r.json()

    @staticmethod
    def update_to_version(versionid):
        with open(ALLO_INFO_PATH, 'rb') as payload:
            r = requests.post("{}/referees/{}/update/{}".format(API_PATH, getnode(), versionid), verify=False, data=payload)
            if API.has_error(r):
                return False
            return r.text

    @staticmethod
    def has_error(r: Response):
        if r.status_code is 502:
            BColors.error("Erreur lors de la communication avec Allo Server : Erreur {}".format(r.status_code))
            return True
        return False
