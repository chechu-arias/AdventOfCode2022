
LEN_START_PACKET = 4
LEN_START_MESSAGE = 14

with open("input_d6.txt", "r") as f:

    data = f.readlines()[0].rstrip()

    start_packet = -1
    for i in range(len(data) - LEN_START_PACKET + 1):
        if len(set(data[i:i+LEN_START_PACKET])) == LEN_START_PACKET:
            start_packet = i + LEN_START_PACKET
            break

    start_message = -1
    for i in range(len(data) - LEN_START_MESSAGE + 1):
        if len(set(data[i:i + LEN_START_MESSAGE])) == LEN_START_MESSAGE:
            start_message = i + LEN_START_MESSAGE
            break

print(f"The start of the package is at index {start_packet}.")
print(f"The start of the message is at index {start_message}.")
