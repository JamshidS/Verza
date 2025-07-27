import os
import configparser
from core.repo import Repository as VerzaRepository


def repo_dir(repo: VerzaRepository, *path):
    return os.path.join(repo.vcsdir, *path)


def run():
    path = os.getcwd()
    vcsdir = os.path.join(path, ".verza")

    if os.path.exists(vcsdir):
        print("Repository already exists.")
        return

    os.makedirs(repo_dir(VerzaRepository(path, force=True), "objects"))
    os.makedirs(repo_dir(VerzaRepository(path, force=True), "refs", "heads"))

    # Create HEAD
    with open(repo_dir(VerzaRepository(path, force=True), "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # Create config
    config = configparser.ConfigParser()
    config.add_section("core")
    config.set("core", "repository_format_version", "0")
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false")

    with open(repo_dir(VerzaRepository(path, force=True), "config"), "w") as f:
        config.write(f)

    print("Initialized empty Verza repository in .verza/")
