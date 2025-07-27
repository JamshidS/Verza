import os
from core.objects import Blob
from core.repo import Repository as VerzaRepository

def run(files):
    repo = VerzaRepository(os.getcwd()) # The cwd function gets the current working directory
    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue

        with open(file_path, 'rb') as f:
            data = f.read()

        blob = Blob(repo, data)
        sha = blob.write()
        print(f"Added: {file_path} ({sha})")