import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
import logging

# Налаштування логування
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Вказати вихідну та цільову папки вручну
source_folder = AsyncPath("input/")
target_folder = AsyncPath("output/")


async def read_folder(folder_path: AsyncPath):
    async for item in folder_path.glob("**/*"):
        if await item.is_file():
            yield item


async def copy_file(file: AsyncPath, target_folder: AsyncPath):
    try:
        extension = file.suffix[1:] if file.suffix else "no_extension"
        target_subfolder = target_folder / extension
        await target_subfolder.mkdir(parents=True, exist_ok=True)
        target_file = target_subfolder / file.name
        await copyfile(file, target_file)
    except Exception as e:
        logging.error(f"Помилка під час копіювання файлу {file}: {e}")


async def main():
    if not await source_folder.exists():
        print(f"Вихідна папка {source_folder} не існує.")
        return

    if not await target_folder.exists():
        await target_folder.mkdir(parents=True, exist_ok=True)

    async for file in read_folder(source_folder):
        await copy_file(file, target_folder)


if __name__ == "__main__":
    asyncio.run(main())
