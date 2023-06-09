#!/usr/bin/env python3

"""
Module for task 1
"""

from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Comprehension over async_generator"""

    return [i async for i in async_generator()]
