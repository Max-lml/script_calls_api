import aiohttp
import asyncio
import json


async def fetch_data(url):
    """Асинхронное получение данных из API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                return await response.json()
            else:
                print("Не удалось получить данные с API.")
                return []


def filter_calls(data):
    """Фильтрация звонков по заданным условиям."""
    filtered = [
        call for call in data
        if len(call['body']) > 100 and "success" in call['body'].lower()
    ]
    return filtered


async def main():
    """Основная функция."""
    url = "https://jsonplaceholder.typicode.com/comments"

    # Загружаем данные с API
    data = await fetch_data(url)

    # Сохраняем необработанные данные в файл calls_raw.json
    with open("calls_raw.json", "w", encoding="utf-8") as raw_file:
        json.dump(data, raw_file, ensure_ascii=False, indent=4)

    # Фильтрация данных
    filtered_calls = filter_calls(data)

    # Сохраняем отфильтрованные данные в файл filtered_calls.json
    with open("filtered_calls.json", "w", encoding="utf-8") as filtered_file:
        json.dump(filtered_calls, filtered_file, ensure_ascii=False, indent=4)

    # Выводим результаты на консоль
    print(f"Общее количество звонков: {len(data)}")
    print(f"Количество отфильтрованных звонков: {len(filtered_calls)}")
    if filtered_calls:
        print(f"Пример текста: \"{filtered_calls[0]['body']}\"")


# Запуск асинхронной программы
if __name__ == "__main__":
    asyncio.run(main())
