import sys
import os

# Dictionary of Instruction opcodes - { binary: [instruction type, instruction] }
opcodes = {
    '10001011000': ['R', 'ADD X{Rd}, X{Rn}, X{Rm}'],
    '1001000100': ['I', 'ADDI X{Rd}, X{Rn}, #{ALUImmediate}'],
    '10001010000': ['R', 'AND X{Rd}, X{Rn}, X{Rm}'],
    '1001001000': ['I', 'ANDI X{Rd}, X{Rn}, #{ALUImmediate}'],
    '000101': ['B', 'B '],
    '100101': ['B', 'BL '],
    '01010100': ['CB', 'B.{Cond} '],
    '11010110000': ['R', 'BR X{Rn}'],
    '10110101': ['CB', 'CBNZ X{Rd}, '],
    '10110100': ['CB', 'CBZ X{Rd}, '],
    '11111111110': ['R', 'DUMP'],
    '11001010000': ['R', 'EOR X{Rd}, X{Rn}, X{Rm}'],
    '1101001000': ['I', 'EORI X{Rd}, X{Rn}, #{ALUImmediate}'],
    '11111111111': ['R', 'HALT'],
    '11111000010': ['D', 'LDUR X{Rd}, [X{Rn}, #{DT_address}]'],
    '11010011011': ['R', 'LSL X{Rd}, X{Rn}, #{Shamt}'],
    '11010011010': ['R', 'LSR X{Rd}, X{Rn}, #{Shamt}'],
    '10011011000': ['R', 'MUL X{Rd}, X{Rn}, X{Rm}'],
    '10101010000': ['R', 'ORR X{Rd}, X{Rn}, X{Rm}'],
    '1011001000': ['I', 'ORRI X{Rd}, X{Rn}, #{ALUImmediate}'],
    '11111111100': ['R', 'PRNL'],
    '11111111101': ['R', 'PRNT X{Rd}'],
    '11111000000': ['D', 'STUR X{Rd}, [X{Rn}, #{DT_address}]'],
    '11001011000': ['R', 'SUB X{Rd}, X{Rn}, X{Rm}'],
    '1101000100': ['I', 'SUBI X{Rd}, X{Rn}, #{ALUImmediate}'],
    '1111000100': ['I', 'SUBIS X{Rd}, X{Rn}, #{ALUImmediate}'],
    '11101011000': ['R', 'SUBS X{Rd}, X{Rn}, X{Rm}']
}

# Dictionary of (Hex) branch condition codes
branch_conditions = {
    '0': 'EQ',
    '1': 'NE',
    '2': 'HS',
    '3': 'LO',
    '4': 'MI',
    '5': 'PL',
    '6': 'VS',
    '7': 'VC',
    '8': 'HI',
    '9': 'LS',
    'a': 'GE',
    'b': 'LT',
    'c': 'GT',
    'd': 'LE'
}

instruction_list = [] # List of instructions for LEGv8 program
label_queue = {} # Queue of branch labels that need to be in LEGv8 program
hex_instructions = [] # Hex instructions saved after reading from input file
binary_instructions = [] # Binary instructions saved after converting hex from input file

# Convert binary to decimal (implements two's complement)
def binToDec(binary):
    if binary[0] == '1':
        # binary represents negative number. Invert all bits and add 1
        n = ''
        for bit in binary:
            n += '1' if bit == '0' else '0'
        result = 0 - (int(n, 2) + 1)
    
    else:
        result = int(binary, 2)

    return result

# Update the queue of labels that are to be inserted
def updateLabelQueue(instructions, address, queue):
    label_addr = len(instructions) + binToDec(address)
    # Check if there is another instrution (branch) pointing to this instruction address. Act accordingly
    if label_addr in queue:
        val = queue.get(label_addr)
        val.append(len(instructions))
        queue.update({label_addr: val})
    else:
        queue.update({label_addr: [len(instructions)]})




try:
    # Open the given file and read the binary. Save its values in hex
    with open(sys.argv[1], 'rb') as instructions:
        line = instructions.read(4)
        while line:
            hex_instr = ''.join(map('{:02X}'.format, line))
            hex_instructions.append(hex_instr)
            line = instructions.read(4)
except FileNotFoundError:
    print('Incorrect file entered or no file provided to disassemble')
    sys.exit(os.system('sh run.sh'))
except:
    sys.exit("There was an issue with the file you provided")

# Convert the hex values to 32-bit big-endian binary and store in binary instruction list
for hex_instr in hex_instructions:
    binary = format(int(hex_instr, 16), '#034b') # Convert hex to binary and ensure the width to be correct (32 bit + 0b prefix)
    binary_instructions.append(binary[2:])

for binary in binary_instructions:
    # Determine instruction and its type based on opcode
    for (key, val) in opcodes.items():
        if binary.startswith(key):
            opcode = key
            instruction = val
            break
    
    rm = shamt = rn = rd = immediate = address = op = cond = '0' # Initilize all bit-fields to 0
    # Collect fields based on instruction type:

    # R-type instruction
    if instruction[0] == 'R':
        rm = binary[11:16]
        shamt = binary[16:22]
        rn = binary[22:27]
        rd = binary[27:32]
    
    # I-type instruction
    elif instruction[0] == 'I':
        immediate = binary[9:22]
        rn = binary[22:27]
        rd = binary[27:32]

    # D-type instruction
    elif instruction[0] == 'D':
        address = binary[11:20]
        op = binary[20:22]
        rn = binary[22:27]
        rd = binary[27:32]
    
    # B-type instruction
    elif instruction[0] == 'B':
        address = binary[6:32]

        updateLabelQueue(instruction_list, address, label_queue) # Update label queue

    # CB-type instruction
    elif instruction[0] == 'CB':
        address = binary[8:27]
        rd = binary[27:32]
        
        # Handle B.cond
        if opcode == '01010100':
            cond_hex = hex(binToDec(rd))[2:]
            cond = branch_conditions.get(cond_hex)
        
        updateLabelQueue(instruction_list, address, label_queue) # Update label queue

    # Store decimal form of bit-fields
    Rn, Rm, Shamt, ALUImmediate, Op = int(rn, 2), int(rm, 2), int(shamt, 2), int(immediate, 2), int(op, 2)
    Rd = Rt = int(rd, 2)
    BR_address = COND_BR_address = DT_address = binToDec(address)
    
    # Add this instruction to the instruction_list array. It will later be used to write to a file
    # Each instruction is stored in the format: [instruction type, LEGv8 instruction]
    leg_instr = [instruction[0], '{}'.format(instruction[1].format(Rd=Rd, Rt=Rt, Rn=Rn, Rm=Rm, Shamt=Shamt, ALUImmediate=ALUImmediate, BR_address=BR_address, COND_BR_address=COND_BR_address, DT_address=DT_address, Op=Op, Cond=cond))]
    instruction_list.append(leg_instr)


# Insert labels into Branch instructions
for (key, val) in label_queue.items():
    for i in val:
        instruction_list[i][1] += 'label_' + hex(key)[2:].capitalize()
        
    # Update label_queue format: {label index: label name}
    val = ['label_' + hex(key)[2:].capitalize()]
    label_queue.update({key: val})

# Insert labels into instruction list
i = 0
while i < len(list(sorted(label_queue))):
    key = list(sorted(label_queue))[i]
    
    # Format of label queue: {key = insertion index: value = [label name]}
    val = label_queue.get(key)[0]
    label = ['L',  val + ':'] # custom "instruction type" L represents label
    instruction_list.insert(key, label)

    # Iterate through label queue to shift all keys (indices) that are affected. This ensures that succeeding labels are correctly inserted
    for j in list(sorted(label_queue)):
        if j > key:
            val = label_queue.pop(j)
            label_queue.update({(j + 1): val})
    
    i += 1

# Write LEGv8 program to output file
output_name = sys.argv[1].split('.')[0] + '_dissassembled.legv8asm'
print_to_terminal = '-p' in sys.argv

with open(output_name, 'w') as output:
    for instruction in instruction_list:
        output.write(instruction[1] + '\n')
        if print_to_terminal:
            print(instruction[1])

print('Program successfully dissassembled and saved as', output_name)