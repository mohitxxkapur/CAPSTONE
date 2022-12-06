#this script is the formulation process of the algorithm used
# this data processing algorithm takes randomly generated numbers and adds them to a list
#values are added until a list reaches a set limit
#at that limit, the last x values are kept aside and put into a new list, to then be transferred back to the newly empty original list
#the loop repeats until it reaches the set number of iterations
val = 0
lst = []
counter = 0

import random

#using a random number generator to create values
def rng(lim):

    while(lim < 0): 
        if lim < 0:
            myError = ValueError('Lim should be positive')
            raise myError
        else: 
            break

    randval = random.randint(0,lim)
    return randval

#method for appending to a list
def fk(lst, xxx):
    lst.append(xxx)

#main counter, we can set 200 to any value necessary, same with the actual desired list as well
while(counter < 200):
    if (len(lst)<50):
        if (len(lst) == 1 or len(lst)==0 ):
            val = rng(20)
            fk(lst, val)
        else:
            i = len(lst)
            if (lst[i-2] < lst [i-1]):
                #print("move down")
                pass
            elif (lst[i-2] > lst [i-1]):
                #print("move up")
                pass
            val = rng(20)
            fk(lst, val)



    elif (len(lst) == 50):
        # xx = lst[len(lst)-1]
        # lst2 = lst
        # lst = []
        # fk(lst,xx)    <-- one element

        #multiple element?

        #this is where the swap takes place
        print("at 50: " + str(lst))
        i = -1
        lst2=[]
        for i in range (3):
            #print (i)
            fk(lst2, lst[-3+i])
        print("finding last 50: " + str(lst2))
        lst = []
        #print ("After emptying: " + str(lst))
        for i in range (len(lst2)):
            fk(lst, lst2[i])
        #print(lst)
        #print(lst2)
        lst2 = []
        #print("empty list 2: " + str(lst2))
    
    counter = counter + 1
