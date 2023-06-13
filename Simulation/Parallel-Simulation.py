## Simulation to calculate average noise across parallel series of trusted nodes
## BP-2
from LinearFormula import *
from Node import *
## Now lets ask the user for the network

## First lets ask for number of paths
numPaths = int(input("How many paths are in our network?"))

## Now we will get the number of nodes for each path
i = 0
numNodesPath = []

## starting node
startNode = Node("startNode", [])
## ending node
endNode = Node("endNode", [], True)


while i < numPaths:
  tempNodes = int(input("How many trusted nodes are in path: " + str(i+1)))
  numNodesPath.append(tempNodes)
  i += 1
  
## Now we will get each node for each path
i = 0
j = 0
while i < numPaths:
  ## node as iterator
  jumpNodeEx = startNode
  j= 0
  first = True
  while j < numNodesPath[i]:
    ## node to be connected
    connectNode = Node("T", [])
    ## append new node
    jumpNodeEx.nextNodes.append(connectNode)
    arcNoise = float(input("Path: " + str(i+1) + "Please input noise % of arc " + str(j+1)))
    ## convert to decimal from percent
    arcNoise /= 100
    ## add arcs and go to next node
    addArc = Arc(arcNoise)
    jumpNodeEx.arcs.append(addArc)
    if first:
      jumpNodeEx = jumpNodeEx.nextNodes[i]
      first = False
    else:
      jumpNodeEx = jumpNodeEx.nextNodes[0]
    j += 1
  ## This is because you will always have one more arc than nodes
  arcNoise = float(input("Path: " +str(i+1) + "Please input noise % of arc " + str(numNodesPath[i])))
  arcNoise /= 100
  addArc = Arc(arcNoise)
  jumpNodeEx.arcs.append(addArc)
  jumpNodeEx.nextNodes.append(endNode)
  i += 1


## Display current independent noises and add to averages array
i = 0
averages = []
# print("Individual approximate noise percent of path: " + str(i+1) + " "+ str(linear_formula_indexed(startNode.nextNodes[0], startNode.arcs[0].noise)[0]))
# print("Individual approximate noise percent of path: " + str(i+2) + " " +str(linear_formula_indexed(startNode.nextNodes[1], startNode.arcs[1].noise)[0]))

while i < numPaths:
  noise = (linear_formula_indexed(startNode.nextNodes[i], startNode.arcs[i].noise)[0])
  averages.append(noise)
  print("Individual approximate noise percent of path: " + str(i+1) + " " + str(averages[i]))
  i+=1


## Now we ask for weights of each path, and apply equation 4
i = 0
weights = []
while i < numPaths:
  tempWeight = float(input("What is the weight of path: " + str(i+1)))
  weights.append(tempWeight)
  i += 1

## Apply weights
avgNoise = 0
i = 0
for x in weights:
  avgNoise += x * averages[i]
  i += 1
print("Average noise in system: " + str(avgNoise))
