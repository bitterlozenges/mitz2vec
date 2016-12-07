import sys

class AdjList(object):
    def __init__(self, directed):
        self.dct = {}
        self.directed = directed

    def add(self, hd, tail):
        # update head adjacency list
        self.add_helper(hd, tail)

        # update tail adjacency list
        if not self.directed:
            self.add_helper(tail, hd)
    
    def add_helper(self, hd, tail):
        if hd not in self.dct:
            self.dct[hd] = []
        self.dct[hd].append(tail)

    def write(self, f):
        for id1, idlst in self.dct.iteritems():
            f.write(id1)
            f.write(" ".join(idlst))
            f.write("\n")

def main(argv):
    if len(argv) != 2 and len(argv) != 3:
        print "Usage: python preprocess_snap.py filename.txt [weighted]"
        sys.exit(-1)
    
    # first arg
    fname = argv[1]
    if fname[-4:] != ".txt":
        print "file must have extension '.txt'"
        sys.exit(-2)
    fprefix = fname[:-5]

    # second arg
    directed= False
    if len(argv) == 3 and argv[2].lower() != "undirected":
        directed = True

    print "Constructing adjacency list"
    # user_id: [user_ids]
    adjlst = AdjList(directed)
    with open(fname) as f:
        for line in f:
            nodes = line.strip().split(" ")
            
            if len(nodes) != 2:
                print "Wrong formatting! Two nodeids per line!"
            
            # populate list
            hd = nodes[0]
            tl = nodes[1]
            adjlst.add(hd, tl)


    # write to file
    print "Writing to file"
    with open(fprefix + "lst.txt", 'w') as f:
        # header for unweighted graph
        f.write("0\n")
        adjlst.write(f)

if __name__ == "__main__":
    main(sys.argv)
