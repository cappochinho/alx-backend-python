#!/usr/bin/env python3

"""
This module contains task 0 - Basic async syntax
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Takes an int input, waits for a random delay
    and returns it
    """

    rnd: float = random.uniform(0, max_delay)
    await asyncio.sleep(rnd)
    return rnd
