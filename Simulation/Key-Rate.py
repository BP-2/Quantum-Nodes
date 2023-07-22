## By BP-2
## Purpose: Model Potential States for QKD Rate, given a value of a and b (a bit flip error and b phase error)

from qiskit import * 
from qiskit.tools.visualization import plot_histogram
from IPython.display import display

# First entanglement based BB84 protocol is done and leaves us with a Bell State which represents AT AT and TB TB

print( "a1 is bit error for channel 1, b1 is phase error for channel 1, a2 is bit error for channel 2, b2 is phase error for channel 2")
# Let us first prompt users for a and b values for Phi (for both Phi)
a = int(input("Please give value of a1"))
b = int(input("Please give value of b1"))
a_two = int(input("Please give value of a2"))
b_two = int(input("Please give value of b2"))

# measure_one = int(input("Please type 1 for Z measurement for Alice, 2 for X measurement"))
# measure_two = int(input("Please type 1 for Z measurement for Trusted Node (1), 2 for X measurement"))
# measure_three = int(input("Please type 1 for Z measurement for Trusted Node (2), 2 for X measurement"))
# measure_four = int(input("Please type 1 for Z measurement for Bob, 2 for X measurement"))





# Now we take these value and create Bell states based on the input

qc_one = QuantumCircuit(2,2)
qc_two = QuantumCircuit(2,2)


# Create regular Bell State
qc_one.h(0)
qc_one.cx(0,1)

# Flip phase
if b == 1:
    qc_one.z(0)
# Flip second bit
if a == 1:
    qc_one.x(1)


# Create regular Bell State
qc_two.h(0)
qc_two.cx(0,1)

# Flip phase
if b_two == 1:
    qc_two.z(0)
# Flip second bit
if a_two == 1:
    qc_two.x(1)


# Now we have both States prepared, we can take the tensor product to evaluate all outcomes (For our two parties it will be 4 4 bit outcomes)
qc_one = qc_one.tensor(qc_two)

# display to users
backend = Aer.get_backend('statevector_simulator')
job = execute(qc_one, backend=backend, shots=500, memory=True)
job_result = job.result()
print(job_result.get_statevector(qc_one))
aer_sim = Aer.get_backend('aer_simulator')
qc_one.measure(0, 0)
qc_one.measure(1, 1)
qc_one.measure(2, 2)
qc_one.measure(3, 3)
job = aer_sim.run(qc_one)
print("All tensor product: ")
print(job.result().get_counts())
print(qc_one)


# Map function

# |a,t1,t2,b> => |a,t1,t2,t1 XOR t2, b XOR t1 XOR t2>

# For this we need only check one instance, due to linearity, result should hold for all instances ****

a = int(input("Select which of the shown tensor products you would like to map (index from zero)"))

original_arr = []

original_arr.append(int(list(job.result().get_counts().keys())[a]))

# rewrite original_arr
original_arr.append(original_arr[0]%10)
original_arr[0] /= 10
original_arr.append(int(original_arr[0]%10))
original_arr[0] /= 10
original_arr.append(int(original_arr[0]%10))
original_arr[0] /= 10
original_arr.append(int(original_arr[0]%10))
original_arr.pop(0)
original_arr.reverse()

print("Mapping: |a,t1,t2,b> => |a,t1,t2,t1 XOR t2, b XOR t1 XOR t2>")
print("Original values" + str(original_arr))

def map_func(original):
    new_arr = []
    # a -> a
    new_arr.append(original[0])
    # t1 -> t1
    new_arr.append(original[1])
    # t2 -> t2
    new_arr.append(original[2])
    # t1 XOR t2
    xor = original[1] ^ original[2]
    new_arr.append(xor)
    # b XOR t1 XOR t2
    xor = original[3] ^ original[1]
    xor ^= original[2]
    new_arr.append(xor)
    return new_arr
    
new_arr = map_func(original_arr)

print("Mapped values: " + str(new_arr))


if new_arr[0] == new_arr[len(new_arr)-1]:
    print("We can see the a and b values match, so, we have a successful pairing")
else:
    print("We can see the a and b values do not match, so, we have an unsuccessful pairing")

