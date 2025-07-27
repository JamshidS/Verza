import os

def run():
    if os.path.exists('.verza'):
        print("A Verza repository already exists in this directory.")
        return
    
    os.makedirs('.verza/objects', exist_ok=True)
    os.makedirs('.verza/refs/heads', exist_ok=True)

    with open('.verza/HEAD', 'w') as f:
        f.write('ref: refs/heads/master\n')

    print("Initialized a new Verza repository in this directory.")    