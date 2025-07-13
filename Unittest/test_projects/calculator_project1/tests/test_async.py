# tests/test_async.py
import unittest
import asyncio
from calculator.async_calc import AsyncCalculator

class AsyncTests(unittest.TestCase):
    def setUp(self):
        self.async_calc = AsyncCalculator()

    async def async_test_add(self):
        result = await self.async_calc.async_add(3, 4)
        self.assertEqual(result, 7)

    def test_async_operation(self):
        asyncio.run(self.async_test_add())