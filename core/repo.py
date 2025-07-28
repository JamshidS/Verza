import os
import configparser


class Repository:
    """
    A class to represent a Verza repository.
    It manages the repository's configuration and provides methods to interact with it.
    """

    def __init__(self, repo_path: str, force: bool = False):
        """
        Initialize the repository at the given path.
        :param repo_path: Path to the repository.
        :param force: If True, force initialization even if the repository already exists.
        """
        self.worktree = repo_path
        self.vcsdir = os.path.join(repo_path, ".verza")

        if not (force or os.path.exists(self.vcsdir)):
            raise Exception(f"Not a Verza repository: {repo_path}")
        
        self.config = configparser.ConfigParser()
        config_path = os.path.join(self.vcsdir, "config")

        if os.path.exists(config_path):
            self.config.read(config_path)
        elif not force:
            raise Exception(f"Configuration file not found in {self.vcsdir}")
        
        if not force:
            version = self.config.get('core', 'repositoryformatversion', fallback=None)
            if isinstance(version, str):
                version = int(version)
            if version != 0:
                raise Exception(f"Unsupported repository format version: {version}")