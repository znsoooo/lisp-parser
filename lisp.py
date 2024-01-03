import re


class Lisp:
    def __init__(self, path):
        self.text = open(path).read()

    def __getitem__(self, key):
        return self.text[key]

    def match(self, pos, patt):
        return re.match(patt, self.text[pos:])

    def find_word(self, word):
        for m in re.finditer(rf'\b{word}\b', self.text):
            yield m.start()

    def find_level(self, pos, level):
        text = self.text[pos:] if level >= 0 else ''.join(reversed(self.text[:pos]))
        n1 = n2 = 0
        for n, c in enumerate(text):
            n1 += c == '('
            n2 += c == ')'
            if n and n2 - n1 == level:
                return pos + n if level >= 0 else pos - n
        else:
            raise ValueError('pair not found')


def find(path, string):
    lisp = Lisp(path)

    for p1 in lisp.find_word(string):
        p2 = lisp.find_level(p1, -3)
        if not lisp.match(p2, 'port'):
            continue
        port = lisp[p2:].split()[1]
        for p3 in lisp.find_word(port):
            p4 = lisp.find_level(p3, -2)
            if not lisp.match(p4, 'joined'):
                continue
            q4 = lisp.find_level(p4, 1)
            joined = lisp[p4:q4]
            for port2 in re.findall('portRef (.+?) ', joined):
                if port2 == port:
                    continue
                for p5 in lisp.find_word('port +' + port2):
                    q5 = lisp.find_level(p5, 1)
                    port2detail = lisp[p5:q5]
                    result = re.findall(r'\(rename Simulation_Value "Simulation Value"\) +\(string "(\w+)"\)', port2detail)
                    yield result[0]


path = '1.edn'
string = 'D_DATA'

print(list(find(path, string)))
