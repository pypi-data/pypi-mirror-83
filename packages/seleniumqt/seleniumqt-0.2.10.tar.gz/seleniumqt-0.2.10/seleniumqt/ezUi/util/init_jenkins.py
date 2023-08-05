#coding: utf-8
import os


def walkFile(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            dir_path = os.path.join(root, d)
            for file in os.listdir(dir_path):
                if os.path.splitext(file)[1] == '.py':
                    path = os.path.join(root, d, '__init__.py')
                    if not os.path.isfile(path):  # 无文件时创建
                        fd = open(path, mode="w", encoding="utf-8")
                        fd.close()
                        print("init .py", path)
                    else:
                        pass


if __name__ == '__main__':
    walkFile('.')
