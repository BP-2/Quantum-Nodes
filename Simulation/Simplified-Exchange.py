# BP-2
# The following simulation creates an entangled pair of cubits between user A and a trusted node and user B and a trusted node to
# mimic the simplified trusted node model.

from qiskit import * 
from qiskit.tools.visualization import plot_histogram
from IPython.display import display

# Create a circuit to hold all data (Bit A, T1, T2, B, and one to perform calculation)
qc = QuantumCircuit(5,1)

# First, we will ask user A for a basis they would like to encode in
prepare_a = input("Hello user A, which basis would you like to prepare in?")

prepare_b = prepare_a # for now, we will work with uniformly prepared basis

print("Now an exchange will be performed with the trusted node, establishing A, T1, T2, and B")


# At this point, we could use the other simulations and ask for channel noises and using this information, run the simulation X amount
# of times with errors that occur at the frequency of the estimated total noise

errors = []
# For now, we will just ask the user for the errors and perform this once
error_a = input("Please provide an error for A (0 for none, 1 for bit-flip, 2 for phase, 3 for both)")
error_t1 = input("Please provide an error for t1 (0 for none, 1 for bit-flip, 2 for phase, 3 for both)")
error_t2 = input("Please provide an error for t2 (0 for none, 1 for bit-flip, 2 for phase, 3 for both)")
error_b = input("Please provide an error for B (0 for none, 1 for bit-flip, 2 for phase, 3 for both)")

errors.append(error_a)
errors.append(error_t1)
errors.append(error_t2)
errors.append(error_b)

print("Now please input the values of each bit, this must be consistent with the prepare basis")
value_a = ""
value_t1 = ""
value_t2 = ""
value_b = ""
if prepare_a == "x":
    value_a = input("Please provide a value for A (+ or -)")
    value_t1 = input("Please provide a value for t1 (+ or -)")
    value_t2 = input("Please provide a value for t2 (+ or -)")
    value_b = input("Please provide an value for B (+ or -)")
elif prepare_a == "z":
    value_a = input("Please provide an value for A (0 or 1)")
    value_t1 = input("Please provide an value for t1 (0 or 1)")
    value_t2 = input("Please provide an value for t2 (0 or 1)")
    value_b = input("Please provide an value for B (0 or 1)")
else:
    print("Incorrect basis input")
    quit()

values = [value_a, value_t1, value_t2, value_b] # |A,T1,T2,B>
counter = 0
# Flip values for given errors
for err in errors:
    match err:
        case "0":
            break
        case "1":
            if values[counter] == "1":
                values[counter] = "0"
            elif values[counter] == "0":
                values[counter] = "1"
            elif values[counter] == "-":
                values[counter] = "-x"
            elif values[counter] == "+":
                values[counter] = "+x"
        case "2":
            if values[counter] == "+":
                values[counter] = "-"
            elif values[counter] == "-":
                values[counter] == "+"
            elif values[counter] == "0":
                values[counter] = "0z"
            elif values[counter] == "1":
                values[counter] = "1z"
        case "3":
            if values[counter] == "1":
                values[counter] = "0z"
            elif values[counter] == "0":
                values[counter] = "1z"
            elif values[counter] == "+":
                values[counter] = "-x"
            elif values[counter] == "-":
                values[counter] = "+x"
        case _:
            print("Incorrect input")
    counter += 1
        
measure =  input("Now we choose measurement basis. Please input measurement basis")


# Now that we have all the needed information, we can begin to construct a quantum circuit to represent the given information

# First we need to create the values
counter = 0
for x in values:
    match x:
        case "+":
            qc.h(counter)
        case "-":
            qc.x(counter)
            qc.h(counter)
        case "1":
            qc.x(counter)
        case "0":
            pass
        case "0z":
            qc.z(counter)
        case "1z":
            qc.x(counter)
            qc.z(counter)
        case "+x":
            qc.h(counter)
            qc.x(counter)
        case "-x":
            qc.x(counter)
            qc.h(counter)
            qc.x(counter)
        case _:
            quit()
    counter += 1

# Now we have to measure the values with the provided basis

# Measure in x basis
if measure == "x":
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)

# Computer classical bit
qc.cx(1,4)
qc.cx(2,4)
qc.measure(4,0)
aer_sim = Aer.get_backend('aer_simulator')
job = aer_sim.run(qc)
print(job.result().get_counts())
print(qc)

# Mismatch case, we display pure abstract states
if measure != prepare_a:
    # First we have to break '+' and '-' into |0> + |1> and |0> - |1> respectively
    expanded_values = []
    counter = 0
    while counter < 3:
        tempVal = []
        if values[counter] == "0":
            # 0 reading in x basis is +
            # values[counter] = "|0> + |1>"
            tempVal.append(0)
            tempVal.append(1)
            expanded_values.append(tempVal)
            
        elif values[counter] == "1":
            # 1 reading in x basis is -
            # values[counter] = "|0> - |1>"
            tempVal.append(0)
            tempVal.append(-1)
            expanded_values.append(tempVal)
        elif values[counter] == "+":
            # + reading in z basis is +
            # values[counter] = "|0> + |1>"
            tempVal.append(0)
            tempVal.append(1)
            expanded_values.append(tempVal)
            print("hit")
        elif values[counter] == "-":
            # - reading in z basis is -
            # values[counter] = "|0> - |1>"
            tempVal.append(0)
            tempVal.append(-1)
            expanded_values.append(tempVal)
        elif values[counter] == "1z":
            # 1 reading in x basis is -
            # values[counter] = "|0> - |1>"
            tempVal.append(0)
            tempVal.append(-1)
            expanded_values.append(tempVal)
        elif values[counter] == "0z":
            # 0 reading in x basis is +
            # values[counter] = "|0> + |1>"
            tempVal.append(0)
            tempVal.append(1)
            expanded_values.append(tempVal)
        elif values[counter] == "+x":
            # + reading in z basis is +
            # values[counter] = "|0> + |1>"
            tempVal.append(0)
            tempVal.append(1)
            expanded_values.append(tempVal)
        elif values[counter] == "-x":
            # -x read in the z basis is different, when a bit flip is applied to the - state, it changes the state unlike the other values
            #values[counter] = "-|0> + |1>" #bro what
            tempVal.append(-0)
            tempVal.append(1)
            expanded_values.append(tempVal)
        counter += 1
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
    
    print("Since we are measuring in mismatched basis for qubits prepared in the X basis, we follow the following formula for mapping our states...")
    print("|i,j> => (|00>+(i*j)|11>)|0>, ((j)|01>+(i)|10>)|1>")
    for x in condensed_vals:
        print(x)    
    # 00, - 01 + 10
  