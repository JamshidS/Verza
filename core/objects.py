import hashlib
import zlib
import os

def hash_object(data, obj_type: str = 'blob') -> str:
    """
    Hash the given data and return its SHA-1 hash as a hexadecimal string.
    :param data: The data to hash.
    :param obj_type: The type of the object (default is 'blob').
    :return: The SHA-1 hash of the data as a hexadecimal string.
    """
    header = f'{obj_type} {len(data)}\0'.encode('utf-8')
    full_data = header + data

    sha1 = hashlib.sha1(full_data).hexdigest()
    path = os.path.join('.verza', 'objects', sha1)

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(zlib.compress(full_data))

    return sha1        