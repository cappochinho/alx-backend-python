#!/usr/bin/env python3
"""
Module for task 1
"""

import asyncio
import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Return the list of all delays
    """
    d_list: List = []

    for _ in range(n):
        delay = asyncio.create_task(wait_random(max_delay))
        d_list.append(delay)

    r_list: List = []
    for work in asyncio.as_completed(d_list):
        res: float = await work
        r_list.append(res)
    return r_list
