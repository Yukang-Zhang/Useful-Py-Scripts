import struct

def read_int16_from_binary_file(input_filename):
    with open(input_filename, 'rb') as file:
        while True:
            data = file.read(2)
            if not data:
                break
            yield struct.unpack('h', data)[0]  # 解析成int16_t

def write_int16_to_text_file(output_filename, int16_values):
    with open(output_filename, 'w') as file:
        for value in int16_values:
            file.write(f"{value} ")

def main():
    input_filename = 'flow1_file.bin'
    output_filename = 'flow1_file.txt'

    int16_values = list(read_int16_from_binary_file(input_filename))

    write_int16_to_text_file(output_filename, int16_values)

if __name__ == "__main__":
    main()
