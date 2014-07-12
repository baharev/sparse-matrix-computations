import fileinput
import matplotlib.pyplot as plt
import networkx as nx
import edge_line
import info_line
import node_line
from representation.problem import Problem
from nodes.attributes import NodeAttr

def lines(iterable):
    for line in iterable:
        first_space = line.find(' ')
        kind  = line[1:first_space-1]
        elems = [e.split() for e in line[first_space:].split(':')]
        if kind.isdigit():
            elems.append(int(kind))
            kind = 'I'
        yield kind, elems

def parse(f):
    funcs = { 'N': info_line.parse,
              'I': node_line.parse,
              'E': edge_line.parse }
    p = Problem()
    for kind, elems in lines(f):
        func = funcs.get(kind)
        if func:
            func(p, elems)
    dag = p.dag

    print 'Finished reading the dag file'
    print 'Some sanity checks'
    #print 'Is connected?', nx.is_connected(dag.to_undirected())
    print 'Is DAG?', nx.is_directed_acyclic_graph(dag)
    print 'Nodes:', nx.number_of_nodes(dag), 'edges:', nx.number_of_edges(dag)

    p.setup_nodes()

    node_labels = nx.get_node_attributes(dag, NodeAttr.display)

    # Why does this crash?
    #dag_copy = dag.to_directed()
    #for _, d in dag_copy.nodes_iter(data=True):
    for _, d in dag.nodes_iter(data=True):
        d.clear()
    # Why does this try to copy attributes that it cannot?
    positions = nx.graphviz_layout(dag, prog='dot')

    nx.draw_networkx(dag, pos=positions, labels=node_labels)
    plt.show()

def read_dag(filename):
    try:
        f = fileinput.input(filename, mode='r')
        return parse(f)
    finally:
        print 'Read', f.lineno(), 'lines'
        f.close()