import hashlib
import zlib
import os
from .repo import Repository as VerzaRepository     

class Blob:
    """
    A class to represent a blob object in the Verza repository.
    It is used to store file contents.
    """

    def __init__(self, repo: VerzaRepository, data: bytes):
        self.repo = repo
        self.data = data
        self.type = 'blob'
        self.sha = None


    def serialize(self) -> bytes:
        """
        Serialize the blob data with its type and length.
        :return: Serialized blob data.
        """
        header = f'{self.type} {len(self.data)}\0'.encode('utf-8')
        return header + self.data

    def write(self) -> str:
        """
        Write the serialized blob data to the repository and return its SHA-1 hash.
        :return: SHA-1 hash of the blob.
        """
        serialized_data = self.serialize()
        sha1 = hashlib.sha1(serialized_data).hexdigest()
        self.sha = sha1
        object_path = os.path.join(self.repo.vcsdir, 'objects', sha1)

        if not os.path.exists(object_path):
            os.makedirs(os.path.dirname(object_path), exist_ok=True)
            with open(object_path, 'wb') as f:
                f.write(zlib.compress(serialized_data))

        return sha1        
    


class Tree:
    """
    A class to represent a tree object in the Verza repository.
    It is used to store directory contents.
    """

    def __init__(self, repo: VerzaRepository, entries=None):
        """
        Initialize the tree with the repository and entries.
        :param repo: The Verza repository instance.
        :param entries: List of entries in the tree.
        """
        self.repo = repo
        self.entries = entries if entries is not None else []
        self.type = 'tree'
        self.sha = None


    def serialize(self) -> bytes:
        """
        Serialize the tree entries.
        :return: Serialized tree data.
        """

        out = b"" 
        for mode, fname, sha in self.entries:
            mode_str = mode.encode('utf-8')
            fname_str = fname.encode('utf-8')
            sha_bytes = bytes.fromhex(sha)
            out += mode_str + b' ' + fname_str + b'\0' + sha_bytes

        header = f'{self.type} {len(out)}\0'.encode('utf-8')
        return header + out


    def write(self) -> str:
        """
        Write the serialized tree data to the repository and return its SHA-1 hash.
        :return: SHA-1 hash of the tree.
        """
        serialized_data = self.serialize()
        sha1 = hashlib.sha1(serialized_data).hexdigest()
        self.sha = sha1
        object_path = os.path.join(self.repo.vcsdir, 'objects', sha1)

        if not os.path.exists(object_path):
            os.makedirs(os.path.dirname(object_path), exist_ok=True)
            with open(object_path, 'wb') as f:
                f.write(zlib.compress(serialized_data))

        return sha1        