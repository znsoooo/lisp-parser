import re


class Node:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.args = []
        self.level = 0 if parent is None else parent.level + 1
        if parent:
            parent.args.append(self)

    def __add__(self, item):
        assert isinstance(item, str), type(item)
        if self.name is None:
            self.name = item
        else:
            Node(self, item)
        return self

    def __getitem__(self, item):
        assert isinstance(item, int), type(item)
        return self.args[item]

    def __repr__(self):
        result = [self.level * '| ' + self.name if self.name else 'TOP']
        result += [str(arg) for arg in self.args]
        return '\n'.join(result)


scanner = re.Scanner([
    (r'\s+', None),
    (r'[^"()\s]+|"[^"]*"', lambda scanner, token: ('NAME', token)),
    (r'\(', lambda scanner, token: ('NEXT', token)),
    (r'\)', lambda scanner, token: ('PREV', token)),
])


def parse(path):
    # 读取文件
    text = open(path).read()

    # 扫描全部文本
    results, remainder = scanner.scan(text)

    # 检测文本处理完毕
    assert remainder == '', repr(remainder[:50])

    # 检测括号数量匹配
    types = [typ for typ, name in results]
    assert types.count('NEXT') == types.count('PREV'), (types.count('NEXT'), types.count('PREV'))

    # 结构化语法树
    root = node = Node()
    for typ, name in results:
        if typ == 'NEXT':
            node = Node(node)
        elif typ == 'PREV':
            node = node.parent
        elif typ == 'NAME':
            node += name

    return root


root = parse('test.edn')
print(root)
