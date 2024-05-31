import re


scanner = re.Scanner([
    (r'\s+', None),
    (r'[^"()\s]+|"[^"]*"', lambda scanner, token: ('NAME', token)),
    (r'\(', lambda scanner, token: (token, token)),
    (r'\)', lambda scanner, token: (token, token)),
])


class Node:
    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name if parent else 'root'
        self.children = []
        if parent:
            parent.children.append(self)

    @property
    def stripname(self):
        return self.name.strip('"')

    def __add__(self, item):
        assert isinstance(item, str), type(item)
        if self.name is None:
            self.name = item
        else:
            Node(self, item)
        return self

    def __contains__(self, item):
        return any(item == node for level, node in self)

    def __eq__(self, item):
        assert isinstance(item, str), type(item)
        return item == self.name

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
        return f'Node({self.name!r})'

    def __str__(self):
        lines = [level * '| ' + node.name for level, node in self]
        return '\n'.join(lines)


def ParseLisp(text):
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])
    types = [typ for typ, name in results]
    assert types.count('NEXT') == types.count('PREV'), (types.count('NEXT'), types.count('PREV'))
    root = node = Node()
    for typ, name in results:
        if typ == '(':
            node = Node(node)
        elif typ == ')':
            node = node.parent
        elif typ == 'NAME':
            node += name
    return root

