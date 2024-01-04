import re


scanner = re.Scanner([
    (r'\s+', None),
    (r'[^"()\s]+|"[^"]*"', lambda scanner, token: ('NAME', token)),
    (r'\(', lambda scanner, token: ('NEXT', token)),
    (r'\)', lambda scanner, token: ('PREV', token)),
])


class Node:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.children = []
        if parent:
            parent.children.append(self)

    def __add__(self, item):
        assert isinstance(item, str), type(item)
        if self.name is None:
            self.name = item
        else:
            Node(self, item)
        return self

    def __eq__(self, other):
        assert isinstance(other, str), type(other)
        return other == self.name

    def __getitem__(self, item):
        assert isinstance(item, (int, str)), type(item)
        if isinstance(item, int):
            return self.children[item]
        if isinstance(item, str):
            return (node for level, node in self if node == item)

    def __iter__(self, level=0):
        yield level, self
        for child in self.children:
             yield from child.__iter__(level + 1)

    def __repr__(self):
        return f'Node("{self.name}")'

    def __str__(self):
        lines = [level * '| ' + (node.name or 'TOP') for level, node in self]
        return '\n'.join(lines)


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
