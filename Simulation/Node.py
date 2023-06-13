## Establish node system
## Going to establish node class, this is for higher level abstraction throughout program
## Each node object has a series of arcs branching from it
class Node:
    def __init__(self, name="", arcs=None, isFinalNode=False, travelled=False, nextNodes=None):
        if arcs is None:
            arcs = []
        if nextNodes is None:
            nextNodes = []
        self.name = name
        self.arcs = arcs
        self.isFinalNode = isFinalNode
        self.travelled = travelled
        self.nextNodes = nextNodes

## Each arc object has a level of quantum noise
class Arc:
    def __init__(self, noise):
        self.noise = noise
