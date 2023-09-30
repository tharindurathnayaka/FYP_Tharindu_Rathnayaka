# Initialize JTAG connection
import intel_jtag
import sys
print("Initializing JTAG connection")
try:
    ju = intel_jtag.intel_jtag_uart()
except Exception as e:
    print(e)
    sys.exit(0)
print("JTAG Connected")
print("Reading Data.... (Press \"Q\" to exit)")


def process(data):
    global R1
    global I1
    global M1
    global PC

    lower_4_bytes = data[1:]  # Assuming data_to_print is a list of 4 bytes
    upper1 = data[0]
    # Convert the lower 3 bytes to a 24-bit binary representation
    binary_str = ''.join(
        [format(byte, '08b') for byte in lower_4_bytes])  # Convert bytes to binary strings
    binary_str2 = upper1  # ''.join([format(byte, '08b') for byte in upper1])

    # Convert the binary representation to a decimal value
    decimal_value = int(binary_str, 2)

    if (binary_str2 == 8):
        R1 = decimal_value

    elif (binary_str2 == 7):
        I1 = decimal_value

    elif (binary_str2 == 5):
        M1 = decimal_value

    elif (binary_str2 == 6):
        PC = decimal_value

    else:
        ER = 1

    print("R1", R1)
    print("M1", M1)
    print("I1", I1)
    print("PC", PC)
    print(binary_str2)

    print(" ".join(
        [f"{byte:02X}" for byte in data_to_print]))  # Print original bytes in hexadecimal format
    print(f"Converted to 24-bit binary: {binary_str}")
    print(f"Decimal Value: {decimal_value}")





buffer = []  # Initialize a buffer to store received bytes
R1=0
M1=0
I1=0
PC=0
inc=0
status=0

while True:
    try:
        read_packet = ju.read()
    except Exception as e:
        print(e)

    if len(read_packet):

        # Append the received bytes to the buffer
        buffer.extend(read_packet)

        while len(buffer) >= 5:
            #print(buffer)
            # Extract and print the first 4 bytes from the buffer
            data_to_print = buffer[:5]
            buffer = buffer[5:]
            inc=inc+1
            if(inc > 5):
                if(status==1):
                    process(data_to_print)

                else:
                    if(data_to_print[0]==255):
                        process(data_to_print)
                        status=1
                    else:
                        buffer = buffer[1:]

            else:
                print("Processor data initilizing")





