#!/usr/bin/env python

import os


def check_path(path):
    if not os.path.exists(path):
        print(f"{path} not exist")
        os.makedirs(path)
        print(f"Create {path} success")
