import tkinter as tk
from tkinter import messagebox
import copy

# Define Node and Arc classes 
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

# Define the linear_formula function 
def linear_formula(startingNode):
  noiseLinearPair = [startingNode.arcs[0].noise, 1 - startingNode.arcs[0].noise]

  ## Next, we must calculate the effects of the ensuing noisy channel
  ## However, if a bit is reflipped, that is no longer considered "bad", and can be moved back to the good position.  If a good value is flipped, it is moved to bad.
  jumpNode = startingNode.nextNodes[0]

  i = 1 #counter

  ## performing formula over each node
  while jumpNode.isFinalNode == False:
    #print(jumpNode.arcs[0].noise)
    #print(jumpNode.name)
    badDiff = noiseLinearPair[0] * jumpNode.arcs[0].noise
    goodDiff = noiseLinearPair[1] * jumpNode.arcs[0].noise

    noiseLinearPair[0] -= badDiff
    noiseLinearPair[0] += goodDiff
    noiseLinearPair[1] -= goodDiff
    noiseLinearPair[1] += badDiff
    #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))

    jumpNode = jumpNode.nextNodes[0]
    i += 1

  #print("Bad: " + str(noiseLinearPair[0]) + " Good: " + str(noiseLinearPair[1]))
  #print("Bad = Qtavg")
  return noiseLinearPair

# Create a Tkinter GUI window
window = tk.Tk()
window.title("Trusted Quantum Nodes Noise Simulation")

# Create a label to display the welcome message
welcomeLabel = tk.Label(window, text="Welcome to the Trusted Quantum Nodes Noise Simulation!")
welcomeLabel.pack(pady=10)

# Function to handle the calculation
def calculate_noise():
    num_nodes = int(numNodesEntry.get())

    # Create the starting and ending nodes
    start_node = Node("startNode", [])
    end_node = Node("endNode", [], True)

    jump_node_ex = start_node
    i = 0

    while i < num_nodes:
        connect_node = Node("T", [])
        jump_node_ex.nextNodes.append(connect_node)
        arc_noise = float(channelNoiseEntries[i].get()) / 100
        add_arc = Arc(arc_noise)
        jump_node_ex.arcs.append(add_arc)
        jump_node_ex = jump_node_ex.nextNodes[0]
        i += 1

    final_arc_noise = float(channelNoiseEntries[i].get()) / 100
    add_arc = Arc(final_arc_noise)
    jump_node_ex.arcs.append(add_arc)
    jump_node_ex.nextNodes.append(end_node)

    result = linear_formula(start_node)

    messagebox.showinfo("Noise Calculation", f"Approximate noise percent of path: {result[0]}")

#Entry widget to get the number of trusted nodes
numNodesLabel = tk.Label(window, text="How many trusted nodes are in your network path?")
numNodesLabel.pack()
numNodesEntry = tk.Entry(window)
numNodesEntry.pack(pady=10)

# Create a list to store the arc noise entry widgets
channelNoiseEntries = []

# Function to add an arc noise entry widget dynamically
def add_arc_noise_entry():
    num_nodes = int(numNodesEntry.get())

    # Clear any existing arc noise entries
    for entry in channelNoiseEntries:
        entry.destroy()
    channelNoiseEntries.clear()

    # Add the correct number of arc noise entry widgets
    for i in range(num_nodes + 1):
        labelText = f"Noise % of arc {i + 1}:"
        arcNoiseLabel = tk.Label(window, text=labelText)
        arcNoiseLabel.pack()
        arcNoiseEntry = tk.Entry(window)
        arcNoiseEntry.pack()
        channelNoiseEntries.append(arcNoiseEntry)


# Create a button to add an arc noise entry widget
channelNoiseButton = tk.Button(window, text="Add Arc Noise", command=add_arc_noise_entry)
channelNoiseButton.pack(pady=10)

# Create a button to calculate the noise
calculateButton = tk.Button(window, text="Calculate Noise", command=calculate_noise)
calculateButton.pack(pady=20)

# Start the Tkinter event loop
window.mainloop()
