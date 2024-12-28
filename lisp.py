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
        self.rawname = 'root' if parent is None else name
        self.name = self.rawname and self.rawname.strip('"')
        self.children = []
        if parent:
            parent.children.append(self)

    def __add__(self, item):
        assert isinstance(item, str), type(item)
        if self.rawname is None:
            self.rawname = item
            self.name = self.rawname and self.rawname.strip('"')
        else:
            Node(self, item)
        return self

    def __bool__(self):
        return True

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
        err = None
        try:
            if isinstance(item, tuple):
                for key in item:
                    self = self[key]
                return self
            if isinstance(item, type(...)):
                assert self.parent is not None
                return self.parent
            if isinstance(item, int):
                return self.children[item]
            if isinstance(item, str):
                return [node for lv, id, node in self.iter() if node == item]
        except Exception as e:
            err = e
        raise ValueError(item) if err else TypeError(item)

    def __iter__(self):
        yield from self.children

    def __len__(self):
        return len(self.children)

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
        lines = [lv * ' | ' + f'[{id}] {node.rawname}\n' for lv, id, node in self.iter()]
        lines[0] = '[/]' + lines[0][3:]
        print(''.join(lines))


def ParseLisp(text):
    results, remainder = scanner.scan(text)
    assert remainder == '', repr(remainder[:50])
    types = [typ for typ, name in results]
    assert types.count('(') == types.count(')'), (types.count('('), types.count(')'))
    root = node = Node()
    for typ, name in results:
        if typ == '(':
            node = Node(node)
        elif typ == ')':
            node = node.parent
        elif typ == 'NAME':
            node += name
    assert node is root, f"node is root{list(node.index())}"
    return root


if __name__ == '__main__':
    text = '''
        (defun factorial (x)
            (cond ((or (not (typep x 'integer)) (minusp x))
                (error "~S is a negative number." x))
                ((zerop x) 1)
                (t (* x (factorial (- x 1))))
            )
        )
        (write(factorial 5))
        (terpri)
        (write(factorial -1))
    '''
    # text = open('demo.lisp').read()
    root = ParseLisp(text)
    root.tree()
