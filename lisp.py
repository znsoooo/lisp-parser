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
        self._name = name if parent else 'root'
        self.name = self._name and self._name.strip('"')
        self.children = []
        if parent:
            parent.children.append(self)

    def __add__(self, item):
        assert isinstance(item, str), type(item)
        if self._name is None:
            self._name = item
            self.name = self._name and self._name.strip('"')
        else:
            Node(self, item)
        return self

    def __contains__(self, item):
        assert isinstance(item, str), type(item)
        return any(item == node for lv, id, node in self.iter())

    def __eq__(self, item):
        if isinstance(item, str):
            return self.name == item
        if isinstance(item, Node):
            return self is item
        raise TypeError(type(item))

    def __getitem__(self, item):
        if isinstance(item, tuple):
            for key in item:
                self = self[key]
            return self
        if isinstance(item, type(...)):
            return self.parent
        if isinstance(item, int):
            return self.children[item]
        if isinstance(item, str):
            return [node for lv, id, node in self.iter() if node == item]
        raise TypeError(type(item))

    def __iter__(self, lv=0):
        yield from self.children

    def __repr__(self):
        return f'Node({self.name!r})'

    def __str__(self):
        return self.name

    def index(self):
        ancient = []
        while self.parent:
            ancient.insert(0, self.parent.children.index(self))
            self = self.parent
        return tuple(ancient)

    def iter(self, lv=0, id=0):
        yield lv, id, self
        for id, child in enumerate(self.children):
             yield from child.iter(lv + 1, id)

    def tree(self):
        lines = [lv * ' | ' + f'[{id}] {node._name}\n' for lv, id, node in self.iter()]
        lines[0] = '[/]' + lines[0][3:]
        print(''.join(lines))


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

