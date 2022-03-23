import re


def pair(s, cp='()', d=0):
    n1 = n2 = 0
    for n, c in enumerate(s):
        n1 += c == cp[0]
        n2 += c == cp[1]
        if n and n2 - n1 == d:
            return n
    raise ValueError('pair not found')


def find_word(s, word):
    for m in re.finditer(r'\b%s\b' % word, s):
        yield m.start()


def parent(s, pos, n):
    return pos - pair(reversed(s[:pos]), ')(', n)


def find(path, string):
    with open(path) as f:
        s = f.read()

    for p1 in find_word(s, string):
        p2 = parent(s, p1, 3)
        s2 = s[p2:]
        if s2.startswith('port'):
            port = s2.split()[1]
            for p3 in find_word(s, port):
                p4 = parent(s, p3, 2)
                s4 = s[p4:]
                if s4.startswith('joined'):
                    q4 = pair(s4, d=1)
                    joined = s4[:q4]
                    ports = re.findall('portRef (.+?) ', joined)
                    for port2 in ports:
                        if port2 != port:
                            for p5 in find_word(s, 'port +' + port2):
                                s5 = s[p5:]
                                q5 = pair(s5, d=1)
                                port2_s = s5[:q5]
                                result = re.findall(r'\(rename Simulation_Value "Simulation Value"\) +\(string "(\w+)"\)', port2_s)
                                yield result[0]


path = '1.edn'
string = 'D_DATA'

print(list(find(path, string)))




