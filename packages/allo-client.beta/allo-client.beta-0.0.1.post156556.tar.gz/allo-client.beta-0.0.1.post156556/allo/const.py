#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import platform
from uuid import getnode as get_mac

from allo.model.config import AlloConfig

TELEPORT_SHA = "786e399511525889778d2a3e64bc5d18f7ecddf6eaac684c224249657f404b76" \
    if os.getenv("ALLOENV") == "TEST" \
    else "fa04922fca037e9f2f6ff0c770ab10c746843c91b4aad8008df24d8b79b6b206"

ALLO_INFO_PATH = '/tmp/allo-infos.yml'

CONFIG_PATH = "/etc/allo-config.dict"

ALLO_URL = "10.81.41.1:3025" \
    if os.getenv("ALLOENV") == "TEST" \
    else "teleport.libriciel.fr:443"

API_PATH = "https://{}/v1/webapi".format("10.81.41.1:3080") \
    if os.getenv("ALLOENV") == "TEST" \
    else "https://{}/v1/webapi".format(ALLO_URL)

CODEPRODUIT = {
    "i-Parapheur": "IP",
    "Pastell": "PA"
}


def getnode():
    config = AlloConfig.load()
    if hasattr(config, "id_client"):
        return config.id_client
    else:
        random.seed(platform.node() + get_mac())
        return str(random.randint(1, 9999999)).zfill(7)
