# -*- coding: utf-8 -*-

from _thread import LockType
from _thread import allocate_lock as allocate
from _thread import start_new_thread as start

__all__ = ("LockType", "allocate", "mutex", "start")

mutex: LockType = allocate()
