#!/usr/bin/env python3

"""
Module for task 0
"""

import asyncio
from typing import Generator
import random


async def async_generator() -> Generator[float, None, None]:
    """
    Yields a random number in range(0 - 10)
    """

    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
