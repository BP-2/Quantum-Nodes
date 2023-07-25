# BP-2
# Simulation of the simplified proof (abstract)
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
    
    expanded_values = []
    counter = 0
    for val in values:
        temp_val = []
        if val == "+":
            temp_val.append(0)
            temp_val.append(1)
            expanded_values.append(temp_val)
        else:
            temp_val.append(0)
            temp_val.append(-1)
            expanded_values.append(temp_val)
        counter += 1
    # for x in expanded_values:
    #     print(x)
        
    # Now we only need to deal with the middle two terms
    # We will tensor the two terms together
    index = 1
    inner_index = 0
    tensor_values = []

    temp_val = []
    temp_val.append(expanded_values[index][inner_index])
    temp_val.append(expanded_values[index+1][inner_index])
    tensor_values.append(temp_val)
    temp_val = []
    temp_val.append(expanded_values[index][inner_index])
    temp_val.append(expanded_values[index+1][inner_index + 1])
    tensor_values.append(temp_val)
    temp_val = []
    temp_val.append(expanded_values[index][inner_index+1])
    temp_val.append(expanded_values[index+1][inner_index])
    tensor_values.append(temp_val)
    temp_val = []
    temp_val.append(expanded_values[index][inner_index+1])
    temp_val.append(expanded_values[index+1][inner_index+1])
    tensor_values.append(temp_val)
        
    zero_ends = []
    one_ends = []
    # Now we take the parity of the bits (ignoring sign)
    for x in tensor_values:
        parity = abs(x[0]) ^ abs(x[1])
        x.append(parity)
        if parity == 1:
            one_ends.append(x)
        else:
            zero_ends.append(x)
        
    # for x in tensor_values:
    #     print(x)
        
    # Now we condense like terms
    condensed_vals = []
    
    term = "("
    if ((zero_ends[0][0] < 0 or zero_ends[0][1] < 0) and zero_ends[0][0] * zero_ends[0][1] <= 0):
        term += "(-)"
    term += "|" + str(zero_ends[0][0]) + str(zero_ends[0][1])+"> +"
    if ((zero_ends[1][0] < 0 or zero_ends[1][1] < 0) and zero_ends[1][0] * zero_ends[1][1] <= 0):
        term += "(-)"
    term += "|" + str(abs(zero_ends[1][0])) + str(abs(zero_ends[1][1]))+">)|0>"
    condensed_vals.append(term)
    
    term = "("
    if ((one_ends[0][0] < 0 or one_ends[0][1] < 0) and one_ends[0][0] * one_ends[0][1] <= 0):
        term += "(-)"
    term += "|" + str(abs(one_ends[0][0])) + str(abs(one_ends[0][1]))+"> +"
    if ((one_ends[1][0] < 0 or one_ends[1][1] < 0) and one_ends[1][0] * one_ends[1][1] <= 0):
        term += "(-)"
    term += "|" + str(abs(one_ends[1][0])) + str(abs(one_ends[1][1]))+">)|1>"
    condensed_vals.append(term)
        
    for x in condensed_vals:
        print(x)    
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
        
