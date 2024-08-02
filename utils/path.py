# -*- coding: utf-8 -*-
import sys
from pathlib import Path

class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0, child_path=None):
        if child_path is None:
            child_path = self.pathname
        if child_path.is_file():
            self.tree += '    |' * n + '    ' + child_path.name + '\n'
        elif child_path.is_dir():
            # 检查是否是应该跳过的目录
            if child_path.name in ['.git', '.gitignore', '.idea', '.vscode', '.vs', '__pycache__']:
                return
            self.tree += '    |' * n +  '-' * 4 + child_path.name + '\n'
            # 先获取子目录列表，然后分别按文件夹和文件排序
            dirs = [cp for cp in child_path.iterdir() if cp.is_dir()]
            files = [cp for cp in child_path.iterdir() if cp.is_file()]
            # 先添加文件夹
            for dir_path in dirs:
                self.generate_tree(n + 1, dir_path)
            # 再添加文件
            for file_path in files:
                self.generate_tree(n + 1, file_path)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)

if __name__ == '__main__':
    dirtree = DirectionTree()
    # 命令参数个数为1，生成当前目录的目录树
    if len(sys.argv) == 1:
        dirtree.set_path(Path.cwd())
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为2并且目录存在
    elif len(sys.argv) == 2 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        print(dirtree.tree)
    # 命令参数个数为3并且目录存在
    elif len(sys.argv) == 3 and Path(sys.argv[1]).exists():
        dirtree.set_path(sys.argv[1])
        dirtree.generate_tree()
        dirtree.set_filename(sys.argv[2])
        dirtree.save_file()
    else:  # 参数个数太多，无法解析
        print('命令行参数太多，请检查！')
