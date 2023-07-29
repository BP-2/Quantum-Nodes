# BP-2
# Simulation of the simplified proof


from qiskit import * 
from qiskit.tools.visualization import plot_histogram
from IPython.display import display


# First we get the measurement that we will be performing on our values
measure = input("Please type 'x' or 'z' for our measurement basis")

# Then we grab our values, for this we will need 4 values |A, T1, T2, B>
values = []
x = 0
print("Please provide input values of 1, 0, +, or - for the values at A, T1, T2, and B. (In that order)")
while x < 4:
    val = input("Please input val: ")
    values.append(val)
    x += 1


# Lets solve !!!
if measure == "z" and (values[0] == "+" or values[0] == "-"):    
    # First we have to break '+' and '-' into |0> + |1> and |0> - |1> respectively
    
    # 5 bits (4 for storing data and 1 for storing XOR vals)
    qc = QuantumCircuit(5,1)
    counter = 0
    for val in values:
        if val == "+":
            qc.h(counter)
            # expanded_values.append(qc)
            # expanded_values.append("|0> + |1>")
        else:
            qc.x(counter)
            qc.h(counter)
            #expanded_values.append(qc)
            # expanded_values.append("|0> - |1>")
        counter += 1
    # for x in expanded_values:
    #     backend = Aer.get_backend('statevector_simulator')
    #     job = execute(x, backend=backend, shots=500, memory=True)
    #     job_result = job.result()
    #     print(job_result.get_statevector(x))

    # XOR qiskit time !
    # To implement XOR, we can CNOT the second bit with the target bit, and then CNOT the third bit with the target bit
    qc.cx(1,4)
    qc.cx(2,4)
    qc.measure(4,0)
    
    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(qc)
    print(job.result().get_counts())
    print(qc)
    # 00, - 01 + 10
    
    
elif measure == "z" and (values[0] == "1" or values[0] == "0"):
    classical_bit = int(values[1]) ^ int(values[2])
    values[3] = (int(values[2]) + int(values[1])) % 2
    print("|" + str(values) +"> " + "|" + str(classical_bit) + ">")
    
elif measure == "x" and (values[0] == "+" or values[0] == "-"):
    temp = 0
    tempTwo = 0
    temp3 = 0
    if values[1] == "+":
        temp = 1
    else:
        temp = 0
    if values[2] == "+":
        tempTwo = 1
    else:
       tempTwo = 0

    classical_bit = temp ^ tempTwo
    tempThree = (temp + tempTwo) % 2
    
    if values[3] == "+" and tempThree:
        values[3] == "-"
    elif values[3] == "-" and tempThree:
        values[3] = "+"
    print("|" + str(values) +"> " + "|" + str(classical_bit) + ">")


elif measure == "x" and (values[0] == "1" or values[0] == "0"):
    # First we have create states of 0 and 1, then we apply hadamard to read in x basis
    # 5 bits (4 for storing data and 1 for storing XOR vals)
    qc = QuantumCircuit(5,1)
    counter = 0
    for val in values:
        if val == "1":
            qc.x(counter)
            qc.h(counter)
        else:
            qc.h(counter)
        counter += 1
    # for x in expanded_values:
    #     backend = Aer.get_backend('statevector_simulator')
    #     job = execute(x, backend=backend, shots=500, memory=True)
    #     job_result = job.result()
    #     print(job_result.get_statevector(x))

    #XOR qiskit time !
    # To implement XOR, we can CNOT the second bit with the target bit, and then CNOT the third bit with the target bit
    qc.cx(1,4)
    qc.cx(2,4)
    qc.measure(4,0)
    
    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(qc)
    print(job.result().get_counts())
    print(qc)
        



# TODO 
# Large simulation that actually does the stuff
# E91 or Bell exchange handoff + Simplified proof (maybe combine noise)