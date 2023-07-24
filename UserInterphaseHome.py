import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
import copy

## Brady 
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

## <--------- GUI ---------> 

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trusted Quantum Nodes Noise Simulation")
        self.geometry("600x600")

        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Dictionary to store different frames/pages

        # Add the StartPage and any other pages you want to create
        for Page in (StartPage, PageOne, PageTwo):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Welcome to the Trusted Quantum Nodes Noise Simulation!", font=("Arial", 20))
        label.pack(pady=20)

        button1 = ttk.Button(self, text="Linear Path", command=lambda: self.controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Parallel Path", command=lambda: self.controller.show_frame(PageTwo))
        button2.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Calculate the Total Noise in a QKD Network", font=("Arial", 20))
        label.pack(pady=20)

        back_button = ttk.Button(self, text="Back to Start Page", command=lambda: self.controller.show_frame(StartPage))
        back_button.pack()

        # Create the tab control
        tabControl = ttk.Notebook(self)
        tabControl.pack(fill='both', expand=True)

        # Create the calculator tab
        calculatorTab = ttk.Frame(tabControl)
        tabControl.add(calculatorTab, text='Calculator')

        # Create the storage tab
        storageTab = ttk.Frame(tabControl)
        tabControl.add(storageTab, text='Storage')

        # Entry widget for number of trusted nodes
        numNodesLabel = tk.Label(calculatorTab, text="How many trusted nodes are in your network path?")
        numNodesLabel.pack()
        self.numNodesEntry = tk.Entry(calculatorTab)
        self.numNodesEntry.pack(pady=10)

        # Create a list to store the arc noise entry widgets and text labels
        self.channelNoiseEntries = []
        self.channelNoiseLabels = []

        # Create a button to add an arc noise entry widget
        channelNoiseButton = tk.Button(calculatorTab, text="Add Arc Noise", command=self.add_arc_noise_entry)
        channelNoiseButton.pack(pady=10) 

        # Create a button to calculate the noise
        calculateButton = tk.Button(calculatorTab, text="Calculate Noise", command=self.calculate_noise)
        calculateButton.pack(pady=20)

        # Create a text widget to display the results in the storage tab
        self.result_text = tk.Text(storageTab, height=10, width=50)
        self.result_text.pack(padx=10, pady=10)
        self.result_text.configure(state='disabled')

        # List to store the outputs
        self.outputs = []

    def add_arc_noise_entry(self):
        num_nodes = int(self.numNodesEntry.get())

        # Clear any existing arc noise entries and labels
        for entry in self.channelNoiseEntries:
            entry.destroy()
        self.channelNoiseEntries.clear()

        for label in self.channelNoiseLabels:
            label.destroy()
        self.channelNoiseLabels.clear()

        # Add the correct number of arc noise entry widgets and labels
        for i in range(num_nodes + 1):
            labelText = f"Noise % of arc {i + 1}:"
            arcNoiseLabel = tk.Label(self, text=labelText)  # Changed calculatorTab to self
            arcNoiseLabel.pack()
            arcNoiseEntry = tk.Entry(self)  # Changed calculatorTab to self
            arcNoiseEntry.pack()
            self.channelNoiseLabels.append(arcNoiseLabel)
            self.channelNoiseEntries.append(arcNoiseEntry)

    def calculate_noise(self):
        num_nodes = int(self.numNodesEntry.get())

        # Create the starting and ending nodes
        start_node = Node("startNode", [])
        end_node = Node("endNode", [], True)

        jump_node_ex = start_node
        i = 0

        while i < num_nodes:
            connect_node = Node("T", [])
            jump_node_ex.nextNodes.append(connect_node)
            arc_noise = float(self.channelNoiseEntries[i].get()) / 100
            add_arc = Arc(arc_noise)
            jump_node_ex.arcs.append(add_arc)
            jump_node_ex = jump_node_ex.nextNodes[0]
            i += 1

        final_arc_noise = float(self.channelNoiseEntries[i].get()) / 100
        add_arc = Arc(final_arc_noise)
        jump_node_ex.arcs.append(add_arc)
        jump_node_ex.nextNodes.append(end_node)

        result = linear_formula(start_node)

        # Store the result in the outputs list
        self.outputs.append(result[0])

        # Update the text widget on the storage tab
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', 'end')

        for i, output in enumerate(self.outputs, 1):
            self.result_text.insert('end', f"Path {i}: The total noise is {output:.4f}\n")
        
        self.result_text.configure(state='disabled')

        # Reset the numNodesEntry and clear the channelNoiseEntries list
        self.numNodesEntry.delete(0, tk.END)
        for entry in self.channelNoiseEntries:
            entry.destroy()
        self.channelNoiseEntries.clear()

        # Clear the text labels
        for label in self.channelNoiseLabels:
            label.destroy()
        self.channelNoiseLabels.clear()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Parallel Path", font=("Arial", 20))
        label.pack(pady=20)

        back_button = ttk.Button(self, text="Home", command=lambda: self.controller.show_frame(StartPage))
        back_button.pack()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()