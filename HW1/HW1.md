## Homework 1

Problems (to be solved on LEGv8 assembly; all code should adhere to standard
register, stack use, paremeter passing, etc. conventions, as discussed in 
lecture and the textbook):

* Implement a swap procedure that swaps the values in two different 8-byte
  integers in memory.
* Implement a find smallest procedure that finds the smallest 8-byte integer
  in an array and returns its index.
* Implement selection sort using your find smallest and swap procedures.  To
  be clear, selection sort can be more efficiently implemented without any
  helper procedures, but implementing it in assembly is easier with the
  helpers--and it gives you experience with procedure calls and stack
  manipulation--so we are requiring that you do it this way.

  Pseudocode for the selection sort:

```
SelectionSort(array)
  for each element in array in order from first to last:
    swap element with smallest element in the subarray that it begins
```
* Implement a procedure to fill an array with consecutive 8-byte integers in
  reverse-sorted (high to low) order
* Implement a "main" procedure that ties all of this together by:
    * Calling your fill procedure to create a reverse sorted array in main
   memory.
    * Sorting that array using your selection sort implementation
    * Program ends with a DUMP


Note that your procedures should handle arrays of any size, so passing an array requires two parameters: the array, and the number of elements in that
array!

How to get started:

1) Get an environment running
2) Write all of your algorithms in C, or some similar language.  If you do it
   in, e.g., Java, keep it C like (use only primitives and arrays).  Make
   sure your code works.  You'll use it to help you reason about your
   assembly.  In a sense, you'll compile it by hand.
3) Write the array builder first.  It will configure your memory in a way
   that makes it easy to check that other procedures work.
4) Do swap next.  Run your array builder.  Then test that you can swap any
   arbitrary pair of values in the array.
5) Find smallest is next.  If you run it on your whole array, it will always
   return the array size - 1 (if you haven't swapped).  It should also work
   on some arbitrary sub array specified by changing the parameters (hint,
   there need to be two of them).
6) Finally do selection sort (you should have been developing "main" all 
   along to test your other procedures).

Gotchas:

Be very careful about the 8s you're going to need all over the place.  It's
easy to forget them, and then things simply don't work!


What to turn in:

A single file, assignment1.legv8asm, containing your program.


Using legv8emul:

Running the emulator with no parameters will give usage instructions.  Code
may have comments.  Comments start with // and continue to the end of the
line (actually, I never check for the second slash, so technically they start
with /).

There are two debugging "instructions" available to you:

  `PRNT reg`

will print the contents of `reg`.

  `DUMP`

will print a complete core dump, including all registers, and display the
program code with an arrow (-->) indicating the line where the dump was
produced.  This arrow is not particularly useful when you explicitly DUMP,
but it is useful when the emulator generates a core dump for you (below).

  `PRNL`

will print a blank line.

  `HALT`

will terminate the simulation.

Unlike a real computer, the emulator will start up with all registers and
memory initialized to zero (except for SP and FP, which are initialized to
the size of the stack).

Also unlike a real computer, the emulator will instantly crash when you
attempt to access an address outside your address space.  Upon crashing, the
emulator will dump core with the arrow indicating the line that attempted to
make the erroneous access.

`legv8emul`

If using this file in a VM or some other Linux system, after downloading it, you will need to make it executable by issuing the command (in a terminal):

```
chmod +x legv8emul
```
