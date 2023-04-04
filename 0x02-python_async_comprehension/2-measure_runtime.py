#!/usr/bin/env python3

"""
Module for task 2
"""

import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measure the total runtime of four couroutines
    """

    start: float = time.time()
    await asyncio.gather(*[async_comprehension() for _ in range(4)])
    end: float = time.time()

    return end - start
