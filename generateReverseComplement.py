#python file to get the reverse read of a sequence
#@sushmitaS16

import re

f = file(raw_input("Enter the .fastq filename: "), 'r')
for line in open(f):
    line = line.rstrip()
    seq_set = set("ATGC")
    #if variable equals to a string with starting character "@" or "+", then keep it just the way it is; print it
    if line.startswith('@') or line.startswith('+'):   
          print line

    #else if variable equals to a string of A,T,G,C, then (i) transform A by T, T by A, G by C, C by G;  (ii) reverse the entire string ; print it
    elif all(char in seq_set for char in line):

        from string import maketrans
        intab = "ATGC"
        outtab = "TACG"
        trantab = maketrans(intab, outtab)
        print''.join(reversed(line.translate(trantab)))

    else:
        #else if variable equals a string with characters, then reverse the entire string ; print it
        print''.join(reversed(line))