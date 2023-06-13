from LinearFormula import *
from Node import *
import sys

## Now lets create an example linear model
## BP-2

## A - .04 -> T - .03 -> T - .5 -> B

## Begin with node A (Alice)
A = Node("A")
T1 = Node("T1")
T2 = Node("T2")
B = Node("B", isFinalNode=True)

# Create arcs and connect nodes
arc1 = Arc(0.04)
A.arcs.append(arc1)
A.nextNodes.append(T1)

arc2 = Arc(0.03)
T1.arcs.append(arc2)
T1.nextNodes.append(T2)

arc3 = Arc(0.5)
T2.arcs.append(arc3)
T2.nextNodes.append(B)

## node iterator
jumpNode = A

i = 0 #counter
while jumpNode.isFinalNode == False:
  print("node " + jumpNode.name + ": " + str(jumpNode.arcs[0].noise))
  jumpNode = jumpNode.nextNodes[0]
  i += 1


## Let's use our formula to calculate the noise
print(linear_formula(A))


