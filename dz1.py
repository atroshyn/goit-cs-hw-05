import os
import shutil
import asyncio
from pathlib import Path
import argparse
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Асинхронна функція для читання папки
async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(asyncio.create_task(copy_file(file_path, output_folder)))
    await asyncio.gather(*tasks)

# Асинхронна функція для копіювання файлу у відповідну підпапку на основі розширення
async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix[1:] if file_path.suffix else 'no_extension'
        target_folder = Path(output_folder) / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file_path.name
        shutil.copy(file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logger.error(f"Failed to copy {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Sort files by extension.')
    parser.add_argument('source_folder', type=str, help='Source folder to read files from')
    parser.add_argument('output_folder', type=str, help='Output folder to sort files into')
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.is_dir():
        logger.error(f"Source folder {source_folder} does not exist or is not a directory")
        return

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == '__main__':
    main()
