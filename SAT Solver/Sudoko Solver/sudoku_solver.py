import csv
import os
from pysat.formula import CNF
from pysat.solvers import Solver

def pos(k,i,j,l):
    return k**4*(i-1)+k**2*(j-1)+l

def depos(k,lis):
    ans=[]
    ans1=[]
    for x in lis:
        if(x>0):
            x-=1
            i=x//k**4
            j=x%k**4//k**2
            l=x%k**2
            l+=1
            ans1.append(l)
            if(j==k**2-1):
                ans.append(ans1)
                ans1=[]
    for i in range(k**2):
        for j in range(k**2):
            print(ans[i][j],end=' ')
        print()

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

def sudoku_solve(k,sudoku1,sudoku2):
    global cnf1
    cnf1=CNF()
    add_clauses(k,cnf1);
    cnf2=cnf1.copy()
    val1=[]
    val2=[]
    for i in range(k**2):
        for j in range(k**2):
            l=sudoku1[i][j];
            if(l):
                cnf1.append([pos(k,i+1,j+1,l)])
                val1.append(pos(k,i+1,j+1,l))
    s=Solver()
    s.append_formula(cnf1.clauses)
    if(s.solve()):
        model=s.get_model()
        depos(k,model)
    else:
        print("It is not possible to solve this sudoku")
        return;
    print()
    for i in range(k**2):
        for j in range(k**2):
            l=sudoku2[i][j];
            if(l):
                cnf2.append([pos(k,i+1,j+1,l)])
                val2.append(pos(k,i+1,j+1,l))
    for i in model:
        if(i>0 and (i not in val1)):
            cnf2.append([-i])
    s.delete()
    s=Solver()
    s.append_formula(cnf2.clauses)
    if(s.solve()):
        model=s.get_model()
        depos(k,model)
    else:
        print("It is not possible to solve sudoku2 with different values")
        return;

global k
k=int(input("Enter the value of k: "))
directory = os.path.dirname(os.path.abspath(__file__))
st=directory+"\sudoku.csv"
sudoku=list(csv.reader(open(st)))
sudoku1,sudoku2,temp=[],[],[]
for r in range(k**2):
    for c in range(k**2):
        temp.append(c)
    sudoku1.append(temp)
    sudoku2.append(temp)
    temp=[]
for r in range(2*k**2):
    for c in range(k**2):
        sudoku[r][c]=int(sudoku[r][c])
sudoku1=sudoku[:k**2]
sudoku2=sudoku[k**2:]

sudoku_solve(k,sudoku1,sudoku2)