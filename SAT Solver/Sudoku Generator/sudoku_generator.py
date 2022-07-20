import csv
import os
import random
from pysat.formula import CNF
from pysat.solvers import Solver

def pos(k,i,j,l):
    return k**4*(i-1)+k**2*(j-1)+l

def depos(k,lis):
    sudoku1,temp=[],[]
    for r in range(2*k**2):
        for c in range(k**2):
            temp.append(0)
        sudoku1.append(temp)
        temp=[]
    for x in lis:
        x-=1
        i=x//k**4
        j=x%k**4//k**2
        l=x%k**2
        l+=1
        sudoku1[i][j]=l
        sudoku1[k**2+i][j]=l+1
        if(l+1>k**2):
            sudoku1[k**2+i][j]=1
    directory=os.path.dirname(os.path.abspath(__file__))
    st=directory+"\sudoku.csv"
    with open(st, 'w',newline='') as csvfile: 
        csvwriter=csv.writer(csvfile) 
        csvwriter.writerows(sudoku1)
    print("File created successfully")

def add_clauses(k,result):
    p=k**2+1
    for i in range(1,p):        #at least 1 element in square
        for j in range(1,p):
            result.append([pos(k,i,j,l) for l in range(1,p)])
            for x in range(1,p):        #at most 1 element in square
                for x1 in range (x+1,p):
                    result.append([-pos(k,i,j,x),-pos(k,i,j,x1)])
    for i in range(1,p):        #no same element in column
        for j in range(1,p):
            for l in range(1,p):
                for j1 in range(j+1,p):
                    result.append([-pos(k,i,j,l),-pos(k,i,j1,l)])
    for j in range(1,p):        #no same element in row
        for i in range(1,p):
            for l in range(1,p):
                for i1 in range(i+1,p):
                    result.append([-pos(k,i,j,l),-pos(k,i1,j,l)])
    for a in range(1,p,k):      #no same element in kxk square
        for b in range(1,p,k):
            lis=[(a+c%k, b+c//k) for c in range(p-1)]
            for (i,i1) in enumerate(lis):
                for (j,j1) in enumerate(lis):
                    if(i<j):
                        for l in range(1, p):
                            result.append([-pos(k,i1[0],i1[1],l),-pos(k,j1[0],j1[1],l)])
    return result;

def sudoku_generate(k):
    total=[v for v in range(k**6)]
    random.shuffle(total)
    global cnf
    cnf=CNF()
    s=Solver()
    add_clauses(k,cnf)
    r=random.randint(1,k**6)
    cnf.append([r])
    s.append_formula(cnf.clauses)
    if(s.solve()):
        solution=[i for i in s.get_model() if i>0]
        S=set(solution)
    s.add_clause([-i for i in solution])
    untested=solution[:]
    random.shuffle(untested)
    necc=[]
    s.set_phases(v*random.randint(0,1)*2-1 for v in total)
    while(len(untested)>0):
        test=untested.pop()
        if(s.solve(assumptions=necc+untested)):
            necc.append(test)
        else:
            core=s.get_core()
            untested=[i for i in untested if i in core]
    necc.sort()
    depos(k,necc)


global k
k=int(input("Enter the value of k: "))

sudoku_generate(k)