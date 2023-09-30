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

buffer = []  # Initialize a buffer to store received bytes
R1 = 0
M1 = 0
I1 = 0
PC = 0

clear_data = True  # Flag to indicate whether to clear incoming data before encountering 255

while True:
    try:
        read_packet = ju.read()
    except Exception as e:
        print(e)

    if len(read_packet):
        # Append the received bytes to the buffer
        buffer.extend(read_packet)

        while len(buffer) >= 5:
            # Extract and print the first 4 bytes from the buffer
            data_to_print = buffer[:5]
            buffer = buffer[5:]

            if clear_data:
                # Check if the first byte is 255
                print(data_to_print[4])
                if data_to_print[4] != 255:
                    continue  # Skip this packet and continue clearing data

                # Clear the flag once 255 is encountered
                clear_data = False

            lower_4_bytes = data_to_print[1:]  # Assuming data_to_print is a list of 4 bytes
            upper1 = data_to_print[0]

            # Convert the lower 3 bytes to a 24-bit binary representation
            binary_str = ''.join([format(byte, '08b') for byte in lower_4_bytes])
            binary_str2 = upper1

            # Convert the binary representation to a decimal value
            decimal_value = int(binary_str, 2)

            if binary_str2 == 8:
                R1 = decimal_value
            elif binary_str2 == 7:
                I1 = decimal_value
            elif binary_str2 == 5:
                M1 = decimal_value
            elif binary_str2 == 6:
                PC = decimal_value
            else:
                ER = 1

            print("R1", R1)
            print("M1", M1)
            print("I1", I1)
            print("PC", PC)
            print(binary_str2)

            print(" ".join([f"{byte:02X}" for byte in data_to_print]))
            print(f"Converted to 24-bit binary: {binary_str}")
            print(f"Decimal Value: {decimal_value}")
