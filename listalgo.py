val = 0
lst = []
counter = 0

import random

def rng(lim):

    while(lim < 0): 
        if lim < 0:
            myError = ValueError('Lim should be positive')
            raise myError
        else: 
            break

    randval = random.randint(0,lim)
    return randval

def fk(lst, xxx):
    lst.append(xxx)

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
