# Power Analysis

# Given the (theoretical) discrete probability distribution p, we postulate a potential deviation ptest from this.
# Our goal is to find the required sample size so that we will "likely" (see below) be able to detect such a deviation

# This is what happens:
#  1) Draw a random sample with sample size N from ptest
#  2) Calculate Chi^2 of this sample w.r.t. the distribution p
#  3) Note if the Chi-test is significant (e.g. at the 95% level)
#  4) Repeat 1-3 Ntests times
#  5) Check how many Chi-tests (out of the Ntests ones) are significant.
#  6) Our goal is to get a ratio of 95%
#     We can achieve this by rerunning the programm with a higher/lower sample size.

import numpy as np
import random

################################ Constants (change as you see fit) #######################################################

# Numberof tests. The more tests, the more accurate the result
Ntests = 10000

# Sample size. This is the value to be varied.
# We want to know which value of N will yield a ratio of ~95% signficant chitests (for given p and ptest)
N=1300     

# The theoretical probability distribution which we assume to be the case (null hypothesis)
# It should not have more than 21 elements, because that's the limit of chisq_reference 
# For example, use [0.5,0.5] for a fair coin
p = np.array([0.5,0.5])

# The probability distribution that we might potentially expect. For example when some reports of changed rates come up.
# For example, use [0.45,0.55] if you suspect a coin might be slightly biased
ptest = np.array([0.45,0.55])

# The chi-square values at which we have 95% significance (c.f. the table at the bottom)
# E.g. chisq_reference[1] contains the chi-square value for 1 degree of freedom
# No need to modify this
chisq_reference = np.array([0,3.84, 5.99, 7.81, 9.49, 11.07, 12.59, 14.07, 15.51, 16.92, 18.31, 19.68, 21.03, 22.36, 23.68, 25.00, 26.30, 27.59, 28.87, 30.14, 31.41])

################################# Input Check (do not modify) ############################################################

dim_p = len(p)
dim   = len(ptest)
if( dim_p != dim ):
    raise ValueError("p and ptest do not have the same dimension")

if( np.sum(p) != 1):
    raise ValueError("The probabilities in p do not sum to 1, but rather "+str(np.sum(p)) )
if( np.sum(ptest) != 1):
    raise ValueError("The probabilities in ptest do not sum to 1"+str(np.sum(ptest)))

################################# Start calculation (do not modify) ######################################################

significantCount = 0
for _ in range(0,Ntests):

    #Array to store the sample in
    count = [0 for _ in range(0,dim)]

    sample = np.random.choice(dim, size=N, p=ptest)
    for i in sample:
        count[i] += 1


    #Perform Pearsons chi-test
    count = np.array(count)
    chisq_arr = (count/(1.0*N) - p)**2/p
    chisq = N*np.sum(chisq_arr)

    #print(chisq)

    #d.o.f. should be 13-1=12, so every chisq value above 21.03 can be considered significant at the 95% level
    
    if( chisq > chisq_reference[dim-1] ):
        significantCount += 1

print("Number of Tests: "+str(Ntests))
print("Sample size N:"+str(N))
print("The ratio of significant to total chi-square tests is "+str(significantCount*1.0/Ntests)+". Ideally, this should be 95% or higher.")


#---------------------------------------
# Reference table:
# d.o.f.      chi^2 for 95% level
# 1             3.84
# 2             5.99
# 3             7.81
# 4             9.49
# 5             11.07
# 6             12.59
# 7             14.07
# 8             15.51
# 9             16.92
# 10            18.31
# 11            19.68
# 12            21.03
# 13            22.36
# 14            23.68
# 15            25.00
# 16            26.30
# 17            27.59
# 18            28.87
# 19            30.14
# 20            31.41

