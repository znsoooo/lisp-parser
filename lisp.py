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


from pprint import pprint
from contextlib import suppress


path = 'XINXICHULI_BD.edn'
text = open(path).read()
root = ParseLisp(text)


cells = {}
for cell in root['cell']:
    cell_name = cell[0].name
    for port in cell['port']:
        port_name = port[0].name
        with suppress(StopIteration):
            string = next(port['PORTCHARA']).parent[1][0].name.strip('"')
            cells.setdefault(cell_name, {})[port_name] = string


instances = {}
for instance in root['instance']:
    instances[instance[0][0].name] = instance[1][1][0].name


for net in root['net']:
    print('=' * 40)
    for portRef in net['portRef']:
        with suppress(IndexError, KeyError):
            x1 = portRef[0].name
            x2 = portRef[1][0].name
            x3 = instances[x2]
            x4 = cells[x3][x1]
            print((x1, x2, x3, x4))
