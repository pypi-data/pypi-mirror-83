import os

def save_write_file(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return path


if __name__ == '__main__':
    path = 'a/a.txt'
    with open(save_write_file(path),'w') as f:
        f.write('123')