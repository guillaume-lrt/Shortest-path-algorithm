# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 17:35:13 2018

@author: ptitg
"""

"""
Return, with a hight probability, the shortest path
going through all points of a given set.
We assume we are in an Euclidean space.
The main function is a greedy algorithm, which choose the best option
at each step (which is why it is not true 100% of the time)
"""

from decimal import Decimal
import math
import copy
import random
import matplotlib.pyplot as plt

def distance(A,B):
    '''euclidean distance between two points'''
    return ((A[0]-B[0])**2+(A[1]-B[1])**2)**0.5

def closest_point(p,L):
    '''return the closest point to p in L'''
    i =1
    D = []
    while len(D) == 0:
        for j in range(len(L)):
            if distance(p,L[j]) <= i:
                D.append(L[j])
        i += 1
    return min(D)

def choose_by_closest(Lx):
    '''start from a random point and always choose the closest one'''
    L = copy.deepcopy(Lx)
    D = [L[0]]
    while len(L) != 1:
        close = closest_point(L[0],L[1:])
        D.append(close)
        L.remove(close)
        L[0] = close
    L = Lx
    # D.append(L[0]) #loop to the beginnning
    return D

def equation_line(A,B):
    if A[0]-B[0] != 0:
        m = (A[1]-B[1])/(A[0]-B[0])
    else:
        return (A[0],math.inf) #x = A[0]
    b = B[1] - m*B[0]
#    print('y = {}x + {}'.format(m,b))
    return (m,b) #y = mx + b


def is_intersection(A,B,C,D):
    '''input: 4 points
       output:  if intersection -> return [True,coordinate intersection]
                else -> [False]    '''
    if (A==D) or (B == C):
        return [False]
    d1 = equation_line(A,B)
    d2 = equation_line(C,D)
    a1,b1 = d1[0],d1[1] #y = a1x + b1
    a2,b2 = d2[0],d2[1]
    if b1 == math.inf:
        u = a1
        if min(C[0],D[0]) < u < max(C[0],D[0]):
            if min(A[1],B[1]) < a2*u+b2 < max(A[1],B[1]):
                return [True,u,a2*u+b2]
            else: return[False]
        else: return [False]
    if b2 == math.inf:
        u = a2
        if min(A[0],B[0]) < u < max(A[0],B[0]):
            if min(C[1],D[1]) < a1*u+b1 < max(C[1],D[1]):
                return [True,u,a1*u+b1]
            else: return [False]
        else: return [False]
    if a1-a2 != 0:
        u = (b2-b1)/(a1-a2)
    elif b2-b1 != 0:
        u = (-a1+a2)/(+b2-b1)
    else:
        u = 0

    v1 = int(Decimal(str(round(a1*u+b1,5)))*100000)/100000  #avoid to return (Decimal('v1'))
    v2 = int(Decimal(str(round(a2*u+b2,5)))*100000)/100000

    # print('u: ',u)
    # print('v1,v2: ',v1,v2)

    if v1 == v2:
        if max(min(A[0],B[0]),min(C[0],D[0])) <= u <= min(max(A[0],B[0]),max(C[0],D[0])):
            if max(min(A[1],B[1]),min(C[1],D[1])) <= v1 <= min(max(A[1],B[1]),max(C[1],D[1])):
                return [True,u,v1]
    return [False]

def intersection(A,B,C,D):
    E = is_intersection(A,B,C,D)
    if E[0]:
        u,v = E[1],E[2]
        return u,v
    return False


def all_intersection(L):
    '''return a dictionnary with
        keys: two segments (4 coordinates) between which there is an intersection
        values: coordinate of the intersection'''
    D = {}
    for i in range(len(L)-2):
        for j in range(i+2,len(L)-1):
            x = (L[i],L[i+1]),(L[j],L[j+1])
            inter = intersection(L[i],L[i+1],L[j],L[j+1])
            if inter != False:
                D[x] = inter
    return D

def check_all_intersection(L):
    '''return true if no intersections'''
    L1 = all_intersection(L)
    if len(L1) > 0: return False
    return True
    # return all(L1[x] == False for x in L1)


def total_length(L):
    A = []
    for i in range(len(L)-1):
        A.append(distance(L[i],L[i+1]))
    return sum(A)


def shortest_path_v1(L):
    '''
        Greedy algorithm: start with 3 points. For each new point, try all possible order such that
        the total length is minimal
        By induction, if for n points, the order is optimal, then if we add a new point that minimize
        the total length, then the order of the n+1 points is still optimal
    '''
    if len(L) < 4: return L + [L[0]]
    L1 = L[:3]   #first 3 points
    L3 = L[3:]   #list of point to add
    count = 0
    while len(L3) != 0:
        # name = 'greedy_shortest_path' + str(count) + '.png'
        # plot(L1,name)
        S = []   #list of all path without crossing
        for j in range(len(L1)):
            L2 = L1[:j] + [L3[0]] + L1[j:]
            L2 = L2 + [L2[0]]  #to have L[0] == L[-1]      (loop)
            if check_all_intersection(L2):  #if intersection => not the shortest path
                if len(S) == 0:
                    S.append(L2)
                    S.append(total_length(L2))
                else:
                    if total_length(L2) < S[1]:  #if longer, don't add it
                        S = []                  #else: remove the old one and keep only this one
                        S.append(L2)
                        S.append(total_length(L2))
        L1 = S[0][:-1]  #remove the loop
        L3.remove(L3[0])
        count += 1
    # name = 'greedy_shortest_path' + str(count) + '.png'
    # plot(L1,name)
    return L1 + [L1[0]], total_length(L1 + [L1[0]])

def inversion(Lx,p1,p2):
    L = copy.deepcopy(Lx)
    i,j = L.index(p1),L.index(p2)
    L[i],L[j] = L[j],L[i]
    return L

counter = 0

def shortest_path_v2(Lx):
    '''first solve it by choosing the closest point
        then remove all intersections
        e.g  ____          ____
             \  /         |    |
              \/     =>   |    |
              /\          |    |
             /__\         |____|
    '''
    L = copy.deepcopy(Lx)
    L.append(L[0])
    # print('L: ',L)
    # print('all intersection: ',all_intersection(L))
    # print('')
    global counter
    counter += 1

    name = 'intersection_shortest_path' + str(counter) + '.png'
    plot(L,name)

    if check_all_intersection(L):
        print('counter: ',counter,'\n')
        # plt.figure()
        # plt.plot([i[0] for i in L],[j[1] for j in L])
        # plt.show()
        return L,total_length(L)
    inter = list(all_intersection(L).keys())[0]  #only need the first one
    x1,x2 = inter[0][1],inter[1][0]
    L = inversion(L,x1,x2)
    L = L[:-1]
    return shortest_path_v2(L)

CO = [(-14,16),
      (-11,12),
      (-6,5),
      (-18,5),
      (-8,-2),
      (-12,0),
      (8,-6),
      (-23,0),
      (-27,-6),
      (9,-14),
      (-15,6),
      (26,6),
      (-18,13),
      (31,8),
      (-4,19),
      (17,-2),
      (-9,27),
      (5,21),
      (20,23),
      (14,10),
      (11,8),
      (5,5),
      (7,-1),
      (2,-2),
      (4,-7),
      (2,-11)]

random.shuffle(CO)

def shortest_path_threshold(L):
    c = 0
    random.shuffle(L)
    while shortest_path_v1(L)[-1] > 217:
        random.shuffle(L)
        c += 1
    print(shortest_path_v1(L))
    return c

def plot(list,name):
    plt.figure()
    my_dpi = 150
    plt.figure(figsize=(1000/my_dpi, 622/my_dpi), dpi=my_dpi)
    fig, ax = plt.subplots()
    plt.plot([i[0] for i in list],[j[1] for j in list])
    ax.set_xlim((-27, 31))
    ax.set_ylim((-14, 27))
    plt.scatter([i[0] for i in CO],[j[1] for j in CO], s = 10)
    fig.savefig(name, transparent=True, dpi=my_dpi)                   #uncomment this line to save all pictures -> create the gif
    # plt.show()

# print(shortest_path_threshold(CO))

L = [(0,0),(-1,-0.7),(1,-1),(1,1),(-1,1/4),(0,-1/2)]

tempo = choose_by_closest(CO)
print('choose by closest: ',tempo)
tempo1 = shortest_path_v2(tempo)
print('intersections: ',tempo1)
print('')
tempoo = shortest_path_v1(CO)
print('greedy algorithm: ',tempoo)

plot(tempo1[0],'intersection_shortest_path.png')
# plot(tempoo[0],'greedy_shortest_path.png')

# print(is_intersection((7, -1), (-15, 6), (-18, 5),(-6,5)))
