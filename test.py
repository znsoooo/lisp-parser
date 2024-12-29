"""
Parameters:
    cell_name: CAP_0402 CAP_0603 RES_0805
    inst_name: R1 R2 C1
    inst_ref: &0123I4567
    port_name: IN1 IN2 OUT1 OUT2
    port_ref: &1A &2Y
    net_name: GND +5V +3V3

"""


import lisp
from pprint import pprint


def GetRefname(node):
    node2 = node[0, 0] if node[0] == 'rename' else node[0]
    return str(node2)


def GetRename(node):
    node2 = node[0, 1] if node[0] == 'rename' else node[0]
    return str(node2)


def GetCells(root):
    table = {}
    for cell in root['cell']:
        table[GetRefname(cell)] = cell_table = {}
        for port in cell['port']:
            cell_table[GetRefname(port)] = GetRename(port)
    return table


def GetInstance(root):
    table = {}
    for inst in root['instance']:
        inst_ref = str(inst[0, 0])
        cell_ref = str(inst[1, 1, 0])
        inst_name = str(inst['designator', -1, 0])
        table[inst_ref] = [cell_ref, inst_name]
    return table


def GetNets(root):
    table = {}
    for net in root['net']:
        net_name = GetRename(net)
        net_ports = []
        for port in net[1]:
            assert len(port) == 2, len(port)
            port_ref = str(port[0])
            inst_ref = str(port[1, 0])
            net_ports.append([inst_ref, port_ref])
        table[net_name] = net_ports
    return table


path = 'demo.lisp'
text = open(path).read()
root = lisp.ParseLisp(text)

cells = GetCells(root)
insts = GetInstance(root)
nets = GetNets(root)

for net_name, net_ports in nets.items():
    for port in net_ports:
        inst_ref, port_ref = port
        cell_ref, inst_name = insts[inst_ref]
        port_name = cells[cell_ref][port_ref]
        port[:] = [cell_ref, port_name]

for net_name, net_ports in nets.items():
    print(net_name)
    for cell_name, port_name in net_ports:
        print(' ', cell_name, '->', port_name)
    print()
