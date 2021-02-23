#!usr/bin/python
 #~ Code to define and solve a linear equation with triviality in solutions
 #~ in a manner so a to compute in a serial and crude way than use 
 #~ mathematical solver functions of various packages as Numpy or Scipy.
#code
a = 550*1591.55 #raw initializes
b = 1375*617.65
# loop for calclating the values 
for i in range(100000):
    for j in range(100000):
        # operative to calculate 
        # i is the icici operative and j is the hdfc operative
        c = b*i - a*j
        # checking suitability of solution 
        if(abs(c)<25):
            print(c,"\t",i,"\t",j)

# end of code
