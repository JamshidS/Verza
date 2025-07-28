import hashlib
import zlib
import os
from .repo import Repository as VerzaRepository     
import time

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
    :param repo: The Verza repository instance.
    :param entries: List of entries in the tree, where each entry is a tuple (mode, filename, sha).
    Each entry represents a file or subdirectory in the tree.
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


class Commit:
    """
    A class to represent a commit object in the Verza repository.
    It is used to store commit metadata and the tree it points to.
    """

    def __init__(self, repo: VerzaRepository, tree_sha: str, parent_shas: str = None, message: str = '', author: str = None):
        """
        Initialize the commit with the repository, tree SHA, parent SHA, commit message, and author.
        :param repo: The Verza repository instance.
        :param tree_sha: SHA of the tree this commit points to.
        :param parent_shas: SHA of the parent commit (if any).
        :param message: Commit message.
        :param author: Author of the commit.
        """
        self.repo = repo
        self.tree_sha = tree_sha
        self.parent_sha = parent_shas if parent_shas else []
        self.author = author if author else 'Verza User <?>'
        self.message = message
        self.type = 'commit'
        self.sha = None


    def serialize(self) -> bytes:
        """
        Serialize the commit data.
        :return: Serialized commit data.
        """   

        lines = [f'tree {self.tree_sha}']
        for parent in self.parent_sha:
            lines.append(f'parent {parent}')

        timestamp = int(time.time())
        time_zone = time.strftime('%z', time.gmtime(timestamp)) #TODO: Adjust time zone handling as needed
        lines.append(f'author {self.author} {timestamp} {time_zone}')
        lines.append(f'committer {self.author} {timestamp} {time_zone}')
        lines.append('')
        lines.append(self.message)
        content = '\n'.join(lines).encode('utf-8')
        header = f'{self.type} {len(content)}\0'.encode('utf-8')
        return header + content


    def write(self) -> str:
        """
        Write the serialized commit data to the repository and return its SHA-1 hash.
        :return: SHA-1 hash of the commit.
        """

        serialized = self.serialize()
        sha1 = hashlib.sha1(serialized).hexdigest()
        self.sha = sha1
        object_path = os.path.join(self.repo.vcsdir, "objects", sha1)

        if not os.path.exists(object_path):
            with open(object_path, "wb") as f:
                f.write(zlib.compress(serialized))

        return sha1
