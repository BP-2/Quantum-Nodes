# BP-2
# Simulation of the simplified proof


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

if measure == "z" and (values[0] == "+" or values[0] == "-"):
    print("Broken case")
    
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
