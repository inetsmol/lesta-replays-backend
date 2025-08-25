import time
import sys
import asyncio


# Тест памяти
def memory_test():
    # Список - вся память сразу
    list_data = [x ** 2 for x in range(1_000_000)]
    print(f"Список: {sys.getsizeof(list_data):,} байт")

    # Генератор - минимум памяти
    gen_data = (x ** 2 for x in range(1_000_000))
    print(f"Генератор: {sys.getsizeof(gen_data):,} байт")


memory_test()


# Тест скорости
def speed_test():
    # Синхронная обработка
    def sync_process(urls):
        results = []
        for url in urls:
            time.sleep(0.1)  # Имитация I/O
            results.append(f"Processed {url}")
        return results

    # Асинхронная обработка
    async def async_process(urls):
        async def process_one(url):
            await asyncio.sleep(0.1)  # Имитация I/O
            return f"Processed {url}"

        tasks = [process_one(url) for url in urls]
        return await asyncio.gather(*tasks)

    urls = [f"url{i}" for i in range(10)]

    # Синхронно: ~1 секунда
    start = time.time()
    sync_process(urls)
    print(f"Синхронно: {time.time() - start:.2f} сек")

    # Асинхронно: ~0.1 секунды
    start = time.time()
    asyncio.run(async_process(urls))
    print(f"Асинхронно: {time.time() - start:.2f} сек")

speed_test()