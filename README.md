## 📦 Verza - Simple Version Control System

Verza is a minimal, Git-like version control system written in Python for learning purposes.
I am following modern **OOP** practices and improving it step-by-step.

---

## 🛠️ Available Commands

You can use the following commands with the `verza.py` CLI interface:

```bash
python verza.py init
```

> Initializes a new Verza repository in the current directory.

```bash
python verza.py add <file1> <file2> ...
```

> Stages one or more files for the next commit.

```bash
python verza.py commit "<your commit message>"
```

> Commits staged files with a commit message.

---

## 🚀 Upcoming Features

* Full-featured CLI using [`argparse`](https://docs.python.org/3/library/argparse.html) and subcommands.
* File tracking and diffing support.
* Branching and commit history navigation.
* Object storage (blobs, trees, commits) similar to Git.
* Persistent index for faster staging.


