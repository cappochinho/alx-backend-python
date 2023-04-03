#!/usr/bin/env python3

"""
Task 4
"""

import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int = 10) -> List[float]:
    """
    Calling task wait random function
    """

    d: List = []
    for i in range(n):
        delay = task_wait_random(max_delay)
        d.append(delay)
    r: List = []
    for task in asyncio.as_completed(d):
        res: float = await task
        r.append(res)
    return r
