# PySNP

A program based on Richard Dawkins' "Methinks it is like a weasel" example. Inspired by (http://scienceblogs.com/pharyngula/2009/08/but_why_would_dawkins_want_to.php)[http://scienceblogs.com/pharyngula/2009/08/but_why_would_dawkins_want_to.php].

## Constants
The following constants can be edited in the file to change the mutation parameters.

````python
# Mutation rates
pointrate = .05 #Accepts to .001 percent.
duprate = .005  #Accepts to .001 percent

# Number of offspring the sample population will have, starting from one individual, in the generation time.
children = 10 
generationtime = 2 # Generation time in years. For final output.

localpeak = 20000 # Evolutionary peak stopper. Stops when reaches a local maxima for N generations.
## Would reccommend 500 000 / generationtime. (half million years) for physical resembelance; 250000/children for speed.

# What degree of unoptomized individuals in a generation prosper (score variance). 
var_mult = 1 
## Strongly reccommend > 0.3

#How "valued" are correct characters?
cstringweight = 1.1 
## 1 would be equally valued to everything; values greater than 1 select for correct characters over expansion of genome. Values of less than 1 selects for expansion more than correctness.


penalty = 1 # If mismatches are penalized. 1 for yes, 0 for no.
debug = 0 #Display debug code. 1 for yes, 0 for no.
````
