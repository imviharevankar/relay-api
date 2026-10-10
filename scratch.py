import asyncio
import time


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def main() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(fetch("a", 1), fetch("b", 1))
    print(results, f"{time.perf_counter() - start:.1f}s")


asyncio.run(main())
