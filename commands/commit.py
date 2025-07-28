import os
from core.repo import Repository as VerzaRepository
from core.objects import Tree, Commit, Blob

def get_head_sha(repo: VerzaRepository) -> str:
    """
    Get the SHA of the current HEAD commit.
    :param repo: The Verza repository instance.
    :return: SHA of the HEAD commit.
    """
    head_path = os.path.join(repo.vcsdir, "HEAD")

    if not os.path.exists(head_path):
        return None
    
    with open(head_path, 'r') as f:
        return f.read().strip()
    
    if ref.startswith("ref: "):
        ref_path = os.path.join(repo.vcsdir, ref[5:])
        if os.path.isfile(ref_path):
            with open(ref_path, 'r') as rf:
                return rf.read().strip()
        else:
            return ref_path

    return None


def update_ref_path(repo: VerzaRepository, ref: str, sha: str):
    ref_path = os.path.join(repo.vcsdir, ref)
    with open(ref_path, 'w') as f:
        f.write(sha + '\n')



def run(message: str):
    repo = VerzaRepository(os.getcwd())

    entries = []
    for file_name in os.listdir():
        if file_name == ".verza" or not os.path.isfile(file_name):
            continue

        with open(file_name, 'rb') as f:
            data = f.read()

        blob = Blob(repo, data)    
        sha = blob.write()
        entries.append(('100644', file_name, sha)) # mode is set to 100644 for regular files
    
    tree = Tree(repo, entries)
    tree_sha = tree.write()

    parent_sha = get_head_sha(repo)
    parents = [parent_sha] if parent_sha else []

    author = "Verza User <?>" #TODO: Will be replaced with actual user info
    commit = Commit(repo, tree_sha, parents, message, author)
    commit_sha = commit.write()

    head_path = os.path.join(repo.vcsdir, "HEAD")
    with open(head_path, 'r') as f:
        ref = f.read().strip()

    if ref.startswith("ref: "):
        ref = ref[5:]
        update_ref_path(repo, ref, commit_sha)    

    else:
        with open(head_path, 'w') as f:
            f.write(commit_sha + '\n')

    print(f"Committed changes with message: {message}")            