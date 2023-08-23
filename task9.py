import os
import sys
import time
import requests
import threading
import multiprocessing
import asyncio
import aiohttp


def download_image(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f'Файл  {file_name} загружен. Адрес источника: {url}')


def download_images_multithreading(urls):
    start_time = time.time()

    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время скачивания при использовании многопоточности: {total_time} сек')


def download_images_multiprocessing(urls):
    start_time = time.time()

    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время скачивания при использовании мультипроцессорности: {total_time} сек')


async def download_image_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            file_name = url.split('/')[-1]
            with open(file_name, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
            print(f'Файл {file_name} загружен. Адрес источника: {url}')


async def download_images_async(urls):
    start_time = time.time()

    tasks = []
    for url in urls:
        tasks.append(download_image_async(url))

    await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'Время скачивания при использовании асинхронности: {total_time} сек')


if __name__ == '__main__':
    urls = sys.argv[1:]

    if not urls:
        print('Укажите список URL-адресов в качестве аргументов командной строки.')
        sys.exit(1)

    download_images_multithreading(urls)

    download_images_multiprocessing(urls)

    asyncio.run(download_images_async(urls))

#python task9.py https://www.gstatic.com/webp/gallery3/1.png https://www.gstatic.com/webp/gallery3/2.png https://www.gstatic.com/webp/gallery3/3.png