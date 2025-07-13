# calculator/async_calc.py
import asyncio

class AsyncCalculator:
    async def async_add(self, a: float, b: float) -> float:
        """Asynchronously add two numbers (simulating async operation)."""
        await asyncio.sleep(0.1)  # Simulate async operation
        return a + b
