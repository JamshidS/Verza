import os
from core.objects import hash_object

def run(files):
    """
    Add files to the Verza repository by hashing them and storing them in the objects directory.
    :param files: List of file paths to add.
    """
    for file_path in files:
        if not os.path.isfile(file_path):
            print(f"Error: {file_path} is not a valid file.")
            continue

        with open(file_path, 'rb') as f:
            data = f.read()

        obj_type = 'blob'  # Default object type
        sha1 = hash_object(data, obj_type)

        print(f"Added: {file_path} ({sha1})")