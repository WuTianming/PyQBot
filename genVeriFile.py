#!/usr/bin/env python3

import json
from urllib import request, parse
from qqrobot import QQClient, QQHandler

a = QQClient()
a.QR_veri()
a.login()
a.save_veri()
