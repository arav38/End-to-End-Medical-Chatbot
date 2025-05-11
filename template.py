import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] : %(message)s:')

list_of_files = [
    'src/__init__.py',
    'src/helpers.py',
    'src/prompt.py',
    '.env',
    'requirements.txt',
    'setup.py',
    'app.py',
    'research/trails.ipynb',
]

for file in list_of_files:
    file_path = Path(file)
    file_dir, filename = os.path.split(file_path)

    if file_dir:
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Directory {file_dir} created.")

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as f:
            pass
        logging.info(f"File {file_path} created.")
    else:
        logging.info(f"File {file_path} already exists and is not empty. Skipping creation.")
