#! /usr/bin/env python3
# coding: utf-8

import subprocess
from typing import List


def run_command(command: List, shell: bool = False, encoding: str = "utf-8"):
    try:
        return subprocess.run(
            command,
            shell=shell,
            encoding=encoding,
            stdout=subprocess.PIPE
        ).stdout
    except subprocess.CalledProcessError as e:
        raise Exception("command has been executed with some errors: " + e)
    except FileNotFoundError as e:
        raise Exception("command was not found: "+e)
