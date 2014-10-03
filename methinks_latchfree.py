# Dawkin's "METHINK IT IS LIKE A WEASEL" program.  Latch free and highly configureable 
# Inspired by http://scienceblogs.com/pharyngula/2009/08/but_why_would_dawkins_want_to.php
# GPLv3 Philip Kahn 2009
## Todo - add generalizations to use genetics to brute-force things

import random, math, time

###########################
# Configuration
###########################
selector = "ABCDEFGHIJKLMNOPQRSTUVWXYZ " # Can change to goal alphabet, such as including lower case, or GTAC.
soln = "METHINKS IT IS LIKE A WEASEL" #Target output

### Announce to user
print("This program is a demo of Single Nucleotide Polymorphisms, or SNPs.")
print("Using arbitrary text, the program will track how long it takes to reach the string '"+soln+"', where that text is the most 'fit'")
try: query=raw_input("Please enter a start string >> ")
except NameError: query=input("Please enter a start string >> ")
wstring = query.upper()


# Mutation rates
pointrate = .05 #Accepts to .001 percent.
duprate = .005  #Accepts to .001 percent

# Number of offspring the sample population will have, starting from one individual, in the generation time.
children = 10 
generationtime = 2 # Generation time in years. For final output.

localpeak = 20000 # Evolutionary peak stopper. Stops when reaches a local maxima for N generations.
## Would reccommend 500 000 / generationtime. (half million years) for physical resembelance; 250000/children for speed.

# What degree of unoptomized individuals in a generation prosper (score variance). 
var_mult = 1 # Strongly reccommend > 0.3

# How "valued" are correct characters?
cstringweight = 1.1 
## 1 would be equally valued to everything; values greater than 1 select for correct characters over expansion of genome. Values of less than 1 selects for expansion more than correctness.


penalty = 1 # If mismatches are penalized. 1 for yes, 0 for no.
debug = 0 #Display debug code. 1 for yes, 0 for no.

################## End Configuration Here ##################

charweight = (1/len(soln))

var = var_mult * charweight

i = 0 #counter

scoreold = 0
matchold = 0
nimp=0

wstringn = wstring
starts = wstring

while wstring != soln:
    j = 0
    wstringa = []
    while j < children:
        wstringa.append(wstring) #creates a $children number of copies
        # See if there is a bit replication
        wstringn = wstringa[j]
        ratecheck = random.randrange(1,10000)/10000
        if ratecheck < duprate:
            num = math.floor(duprate/ratecheck) #Number of duplications that appear
            slength = len(wstringn)
            if slength is not 1: bit = random.randrange(0,slength)
            else: bit = 0 #you can only duplicate bit 0 if there is one bit
            if random.random() > .5: #duplication or deletion?
                if bit is not 0: wstringn = wstringn[:bit] + wstringn[bit-num:] #duplicate a random bit
                else: wstringn = wstringn + wstringn #fix for single character
            else: 
                wstringn = wstringn[:bit+1] + wstringn[bit-num:] #delete a random bit
        ratecheck = random.randrange(1,10000)/10000
        if ratecheck < pointrate:
            num = math.floor(pointrate / ratecheck) #number of SNPs (single-bit changes)
            nc = 0
            while nc < num: #loop over it
                slength = len(wstringn)
                bit=random.randrange(0,slength,1)
                letter = selector[random.randrange(0,len(selector),1)]
                while letter == wstringn[bit]: # Don't replace with same letter
                    letter = selector[random.randrange(0,len(selector),1)]
                if debug is 1: 
                    if nimp > 500: print("  Before: "+wstringn+" @ bit "+str(bit)+" with "+letter)
                if bit!=0: wstringn = wstringn[:bit] + letter + wstringn[bit+1:] #replace a random bit with a random letter
                else: wstringn = letter + wstringn[1:]
                nc +=1
            if debug is 1: 
                if nimp > 500: print(wstringn)
        # Mutations are done on this child.  Replace the stored version with this one.
        wstringa[j]=wstringn
        j+=1 # Increment child number and repeat for next child
    # Score the children
    wstringscore=0
    wstringscore = []
    n=0
    matchhigh = 0
    for x in wstringa:
        if len(soln) > len(x): lenweight = len(x)
        else: lenweight = 2*len(soln) - len(x) #for when it goes above the target length
        score = lenweight*charweight #Score for length
        # Check each bit, and score for correctness
        k = 0
        scoremax = 0
        match = 0
        while k < len(x):
            if k < len(soln):
                if x[k] == soln[k]: # Score correct bits up to length of target
                    score = score + charweight*cstringweight
                    match += 1
                elif penalty == 1: score = score - charweight #If penalties are on, penalizes wrong bits
            else: score = score - charweight*cstringweight #penalizes extra bits, longer than target ## Maybe lessen this penalty?
            k += 1
        if match > matchhigh: # Checks matched bits
            matchhigh = match
            if matchhigh > matchold:
                if debug is 1: print("High match, "+str(matchhigh)+"|"+str(matchold)+": "+x)
                matchold = matchhigh
                if debug is 1: 
                    print(score,n)
                    print(wstringscore)
        if debug is 1: 
            if nimp > 500: print(score)
        wstringscore.append(score) # add the score to the list
        n+=1
    # Create a list of all items with max score, within variability tolerances
    m = 0
    higharr=0
    higharr = []
    while m < len(wstringscore):
        if wstringscore[m] > max(wstringscore)-var: # To allow variability
            higharr.append(m)
        m += 1
    index = random.randrange(0,len(higharr)) # Selects random individual from most-fit population
    if wstringscore[higharr[index]] < max(wstringscore): 
        if debug is 1: 
            print("ERROR 1: Not most fit individual selected, or rounding error") # Debugging
            time.sleep(1) # Debugging
    elif wstringscore[higharr[index]] < scoreold: 
        if debug is 1: 
            print("ERROR 2: Fittest individual is less fit than any in previous generation.")  # Debugging
            time.sleep(1) # Debugging
    else: 
        improvement = wstringscore[higharr[index]] - scoreold ###Book-keeping for generational cap
        scoreold = wstringscore[higharr[index]]###
        if improvement == 0: nimp += 1  ###
        else: nimp = 0 ###
        if debug is 1: print("Improvement: "+str(improvement)) # Debugging
        if improvement < 0: 
            if debug is 1: 
                print("ERROR 3: Fittest regression from peak.") # Debugging
                time.sleep(1) # Debugging
    winner=higharr[index] # Selects the actual individual
    if debug is 1: print("Winner: "+str(higharr[index]))
    wstring = wstringa[winner] # Stores individual for next loop
    if debug is 1: 
        if i % 500 is 0: wstring = wstringa[random.randrange(0,len(wstringscore))] # Every 500 generations we just pick a random individual
    i+=1
    ## Output formatting, and remainders from debugging
    cnum=higharr[index]
    for good in higharr:
        if good is winner: wstring = wstringa[good]
    if cnum < 10: cnum = " "+str(cnum)
    else: cnum = str(cnum)
    lenmatch = len(wstring)/len(soln)
    totalmatch =  (len(soln) - matchhigh)/len(soln) + math.fabs(lenmatch-1)*100
    if debug is 1: scoreoutput = "Score: " + str(wstringscore[higharr[index]]) + " with "
    else: scoreoutput = "Currently with "
    ## output
    print("Generation " + str(i) + ", child "+cnum+": " + wstring + ". "+scoreoutput+str(matchhigh)+" character matches and "+str(len(wstring)/len(soln))+" length match for "+str(totalmatch)+"% error.")
    if nimp > localpeak: wstring = soln # Escapes out from local peak
#Final outputs
if nimp < localpeak: print("Goal "+str(len(soln))+"-bit sequence achieved from source "+str(len(starts))+"-bit sequence in "+str(generationtime*i)+" years with a "+str(len(selector))+"-bit alphabet.")
else: 
    print("Evolutionary local maxima reached in "+str((i-localpeak)*generationtime)+" years.  Further improvement required too much regression (total evolution stopped after "+str(i*generationtime)+" years). Difference from goal was "+str(totalmatch)+"%.")
    print("Run again, or consider increasing the local maxima variable, or decreasing the weight of correct letters.")

