"""Atomic replacement tolerant of brief Windows sync/antivirus file locks."""
import os
import time


def atomic_replace(source,target):
    for delay in (.01,.03,.08,.15,None):
        try:
            os.replace(source,target)
            return
        except PermissionError:
            if delay is None:raise
            time.sleep(delay)
