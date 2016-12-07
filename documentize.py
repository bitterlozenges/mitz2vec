# Create documents based on random walk on adajcency list representation
# Each document is its own line

import random
from numpy.random import choice
import sys

class Node(object):
    """ Node object representing id with outedges.
    
    Fields:
        id : None if invalid node
        weighted : True if weighted edges
        dests: 
            if weighted, list of destinations
            otherwise, dictionary of destinations : weight
        outdegree: 
            if weighted, len(dests)
            else sum of weights
    """
    def __init__(self, s, weighted):
        lst = s.split(" ")
        self.weighted = weighted

        # verify formatting
        if not len(lst):
            self.id = None
            print("Invalid Node string:", s)
            return
        
        self.id = lst[0]
        lst = lst[1:]
        
        # parse endpoints
        if self.weighted:
            # ensure 1 weight per node
            if len(lst) % 2 == 1:
                self.id = None
                print("Invalid weighted Node string:", s)
                return

            node_count = int(len(lst) / 2)
            self.outdegree = 0           
            self.dests = {}

            # save each node
            for i in range(node_count):
                nodeid = lst[2*i]
                w = int(lst[2*i+1])
                
                self.dests[nodeid] = w
                self.outdegree += w
                
            for k in self.dests.keys():
                self.dests[k] = float(self.dests[k]) / self.outdegree
        else:
            self.outdegree = len(lst)
            self.dests = lst

    def next(self):
        if not weighted:
            return random.choice(self.dests)
  
        return choice(list(self.dests.keys()), p=list(self.dests.values()))

if __name__ == "__main__":
    # verify args
    if len(sys.argv) < 3:
        print("Usage: python documentize.py adjlist.txt outfile.txt [restart_probability] [num_docs] \nDefaults: restart_probability=0.1 num_docs=10000")
        sys.exit(-1)

    in_fname = sys.argv[1]
    out_fname = sys.argv[2]
    if in_fname[-4:] != ".txt" or out_fname[-4:] != ".txt":
        print("files must have extension '.txt'")
        sys.exit(-2)
    
    # restart probability
    p = 0.01
    # num docs
    D = 10000
    if len(sys.argv) >= 4:
        p = sys.argv[3]
    if len(sys.argv) >= 5:
        D = sys.argv[4]
    
    print("PROCESSING GRAPH")
    # parse infile        
    with open(in_fname) as f:
        # is the graph weighted?
        header = f.readline().strip()
        weighted = False
        if header == "1":
            weighted = True

        # create graph
        graph = {}
        for line in f:
            node = Node(line, weighted)
            if not node.id:
                sys.exit(-3)
            graph[node.id] = node

    print("WRITING TO FILE")
    # write outfile
    with open(out_fname, 'w') as f:
        keys = list(graph.keys())
        for _ in range(D):
            curr = graph[random.choice(keys)]
            # probability p of restarting
            while random.random() > p:
                f.write(curr.id + " ")               
                curr = curr.next()
                if curr not in graph:
                    break
                curr = graph[curr]
            f.write(curr.id + " \n")