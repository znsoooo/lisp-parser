"""
Parameters:
    cell_name: CAP_0402 CAP_0603 RES_0805
    inst_name: R1 R2 C1
    inst_ref: &0123I4567
    port_name: IN1 IN2 OUT1 OUT2
    net_name: GND +5V +3V3

"""


import lisp
from pprint import pprint


def GetName(node):
    if 'rename' not in node.children[0]:
        return node[0].stripname
    else:
        return node[0][1].stripname


def GetCells(root):
    return [GetName(cell) for cell in root['cell']]


def GetInstance(root):
    insts = {}
    for inst in root['instance']:
        inst_ref = inst[0][0].stripname
        cell_name = inst[1][1][0].stripname
        inst_name = inst[4][0].stripname
        insts[inst_ref] = [cell_name, inst_name]
    return insts


def GetNets(root):
    nets = {}
    for net in root['net']:
        net_name = GetName(net)
        net_ports = []
        for port in net[1].children:
            port_name = port[0].stripname
            inst_ref = port[1][0].stripname
            net_ports.append([inst_ref, port_name])
        nets[net_name] = net_ports
    return nets


path = '1.edn'
text = open(path).read()
root = lisp.ParseLisp(text)

cells = GetCells(root)
insts = GetInstance(root)
nets = GetNets(root)

for net_name, net_ports in nets.items():
    for port in net_ports:
        inst_ref, port_name = port
        cell_name, inst_name = insts[inst_ref]
        port[:] = [cell_name, port_name]

for net_name, net_ports in nets.items():
    print()
    print(net_name)
    for cell_name, port_name in net_ports:
        print(' ', cell_name, '->', port_name)
