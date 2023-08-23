import random
import time
import threading
import multiprocessing
import asyncio

arr = [random.randint(1, 100) for _ in range(1000000)]


def sequential_sum():
    start_time = time.time()

    total_sum = sum(arr)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Последовательное вычисление, сумма: {total_sum}. Время выполнения: {total_time} сек')


def multithreading_sum():
    start_time = time.time()

    num_threads = 4
    chunk_size = len(arr) // num_threads

    partial_sums = []

    def sum_chunk(chunk):
        partial_sums.append(sum(chunk))

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(arr)
        thread = threading.Thread(target=sum_chunk, args=(arr[start:end],))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total_sum = sum(partial_sums)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Многопоточное вычисление, сумма: {total_sum}. Время выполнения: {total_time} сек')
def sum_chunk(chunk):
    return sum(chunk)


def multiprocessing_sum():
    start_time = time.time()

    num_processes = 4
    chunk_size = len(arr) // num_processes

    pool = multiprocessing.Pool(processes=num_processes)
    partial_sums = pool.map(sum_chunk, [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)])
    pool.close()
    pool.join()

    total_sum = sum(partial_sums)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Многопроцессорное вычисление, сумма: {total_sum}. Время выполнения: {total_time} сек')


async def async_sum():
    start_time = time.time()

    chunk_size = len(arr) // 4

    async def sum_chunk(chunk):
        return sum(chunk)

    tasks = []
    for i in range(4):
        start = i * chunk_size
        end = start + chunk_size if i < 3 else len(arr)
        task = asyncio.create_task(sum_chunk(arr[start:end]))
        tasks.append(task)

    partial_sums = await asyncio.gather(*tasks)
    total_sum = sum(partial_sums)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Асинхронность вычисление, сумма: {total_sum}. Время выполнения: {total_time} сек')


if __name__ == '__main__':
    sequential_sum()
    multithreading_sum()
    multiprocessing_sum()
    asyncio.run(async_sum())
