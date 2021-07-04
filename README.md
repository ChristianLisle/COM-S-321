## COM S 321 - Computer Architecture

This is an archive of my assignments from the course Computer Science 321 (Computer Architecture) at Iowa State University in the Spring of 2021.

This course covered many topics including assembly programming languages. Homework assignments involved a subset ARMv8 (assembly) language called LEGv8 ([learn more](http://harmanani.github.io/classes/csc320/Notes/ch02.pdf)).


### Using the LEGv8 Emulator:

In order to execute `legv8asm` files on ordinary computers, the LEGv8 emulator must be used. The emulator can be compiled using the following command in the same directory as the `legv8emul` file:

```
chmod +x legv8emul
```

After compiling the LEGv8 emulator, you should be able to use the emulator like so:

```
./legv8emul <LEGv8 file>
```

##### Optional parameters

`-a`: Run the emulator as an assembler, outputing a `.machine` file

`-b`: Run the emulator in binary emulation mode

### Homework 1

Create a LEGv8 program that implements selection sort.`SelectionSort.java` was used as a reference. 

View the full assignment prompt [here](HW1/HW1.md).

### Homework 2

Create a LEGv8 dissassembler. A dissassembler reads a binary file and converts it into LEGv8 code.

View the full assignment prompt [here](HW2/HW2.md).
