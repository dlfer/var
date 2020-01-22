#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# class of simplicial complex (abstract). 
"""
This is a simple module, maybe to explain simplicial complexes and simplicial homology.

USAGE:
------

From jupyter/python console, then import it

    >>> from simplicial import *

EXAMPLES:
---------

>>> X=simplicial_sphere(['a','b'])
>>> print(X)
Simplicial Complex of dim 0:
 vertices: ['a', 'b']
 simplices:
  0: [['a'], ['b']]
>>> betti_numbers(X)
[2]


Join of simplices

>>> s0=simplicial_sphere(["A","B"])
>>> t0=simplicial_sphere([0,1,2])
>>> print(s0+t0)
They must be surfaces!
None
>>> print(s0*t0)
Simplicial Complex of dim 2:
 vertices: [0, 1, 2, 3, 4]
 simplices:
  0: [[0], [1], [2], [3], [4]]
  1: [[2, 3], [2, 4], [3, 4], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4]]
  2: [[0, 2, 3], [0, 2, 4], [0, 3, 4], [1, 2, 3], [1, 2, 4], [1, 3, 4]]

Cartesian product 

>>> print(s0 % t0)
Simplicial Complex of dim 1:
 vertices: [('A', 0), ('A', 1), ('A', 2), ('B', 0), ('B', 1), ('B', 2)]
 simplices:
  0: [[('A', 0)], [('A', 1)], [('A', 2)], [('B', 0)], [('B', 1)], [('B', 2)]]
  1: [[('A', 0), ('A', 1)], [('A', 0), ('A', 2)], [('A', 1), ('A', 2)], [('B', 0), ('B', 1)], [('B', 0), ('B', 2)], [('B', 1), ('B', 2)]]


>>> K= simplicial_sphere(1)
>>> print(K)
Simplicial Complex of dim 1:
 vertices: [0, 1, 2]
 simplices:
  0: [[0], [1], [2]]
  1: [[0, 1], [0, 2], [1, 2]]


>>> K=SimplicialComplex( ["A","B"], maximal_simplices={1: [["A","B"]] } , must_reindex=True)
>>> print(K)
Simplicial Complex of dim 1:
 vertices: ['A', 'B']
 simplices:
  0: [['A'], ['B']]
  1: [['A', 'B']]

>>> EPchar(K)
1

>>> s1=simplicial_sphere(1)
>>> T=s1 % s1 
>>> K= ( T + T + T ) * s1
>>> print(K)
Simplicial Complex of dim 4:
 vertices: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
 simplices:
  0: [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]]
  1: 141 simplices
  2: 338 simplices
  3: 375 simplices
  4: 150 simplices

>>> dims_c(K)
[24, 141, 338, 375, 150]

>>> betti_numbers(K)
****[1, 0, 0, 6, 1]

Connected sum.

>>> s1=simplicial_sphere(1)
>>> T=s1 % s1
>>> betti_numbers(T)
**[1, 2, 1]

>>> K=T+T+T
>>> betti_numbers(K)
**[1, 6, 1]

>>> K= (  ( s1 % s1 ) + simplicial_sphere(2) ) * s1
>>> betti_numbers(K)
****[1, 0, 0, 2, 1]

>>> K= disjoint_union(T,T)
>>> print(K)
Simplicial Complex of dim 2:
 vertices: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), '(0, 0)+', '(0, 1)+', '(0, 2)+', '(1, 0)+', '(1, 1)+', '(1, 2)+', '(2, 0)+', '(2, 1)+', '(2, 2)+']
 simplices:
  0: 18 simplices
  1: 54 simplices
  2: 36 simplices
>>> betti_numbers(K)
**[2, 4, 2]
>>> EPchar(K)
0
>>> dims_c(K)
[18, 54, 36]

"""
#------------------------------------------------------------
import time
import numpy as np
import itertools
from sympy.matrices import * 
from sympy import pprint
import sys
#------------------------------------------------------------
# just the decoration... 
MAX_NUMBER=3

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000) )
        return result
    return timed

#------------------------------------------------------------
def subsets(seq,k):
    "funzione ricorsiva/generatore per restituire i sottoinsiemi di k elementi della lista seq."
    N=len(seq)
    if k==0 or k > N:
        yield []
    else:
        for i in range(N-k+1):
            for rest in subsets(seq[i+1:],k-1):
                yield [ seq[i],] + rest

def all_subsets(seq):
    for k in range(1,len(seq)+1):
        for x in subsets(seq,k):
            yield x
   
#------------------------------------------------------------
def seq_remove(j,seq):
    return seq[:j] + seq[j+1:]

#------------------------------------------------------------
def _populate_the_simplices(maximal_simplices):
    """maximal_simplices is a dict of maximal simplices, given by integers."""
    result={}
    for k in range(max(maximal_simplices.keys())+1):
        result[k]=[]
    for k in maximal_simplices.keys():
        for sigma in maximal_simplices[k]:
            if sigma in result[k]:
                continue
            else:
                result[k] += [sigma] 
                for face in all_subsets(sigma) :
                    if face != [] and face not in result[len(face)-1]:
                        result[len(face)-1] += [face]
    return result 

#------------------------------------------------------------
class SimplicialComplex:
    """If just the set of verties: 0-dim simplicial complex. 
       Otherwise, simplices, which is a dictionary of integer indices i.e. simplices.
       Otherwise, just maximal_simplices, and simplices are populated.
       if must_reindex=True, simplices in terms of symbols will be converted
       to simplices in terms of integer indices
       
       operations: 
       connected_sum     +
       join              *
       cartesian_product %



EXAMPLES:
---------

>>> K=SimplicialComplex(list(range(7)),maximal_simplices={1:[ sorted([x % 7, (x+1)% 7]) for x in range(7)] } )
>>> print(K)
Simplicial Complex of dim 1:
 vertices: [0, 1, 2, 3, 4, 5, 6]
 simplices:
  0: [[0], [1], [2], [3], [4], [5], [6]]
  1: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [0, 6]]
"""
    def __init__(self,vertices,simplices=None,maximal_simplices=None,must_reindex=False):
        """ arguments: 
>>> K=SimplicialComplex([0,1,2],must_reindex=True,maximal_simplices={2: [[0,1,2]] })
"""
        #first a little bit of input checking  
        self.is_euclidean=False #__TODO__  
        if not isinstance(vertices,list) or len(vertices)==0:
            raise Exception("vertices should be a non-empty list!")
        self.vertices=vertices
        self.number_of_vertices=len(vertices)
        if simplices is not None and not isinstance(simplices,dict):
            raise Exception("simplices should be a dict!")
        if maximal_simplices is not None and not isinstance(maximal_simplices,dict):
            raise Exception("maximal_simplices should be a dict!")
        self.maximal_simplices=maximal_simplices
        self.simplices=simplices
        if simplices is not None:
            self.dimension=max(self.simplices.keys())
        else:
            self.dimension=0
        if simplices is not None and must_reindex:
            new_simplessi={}
            for k in range(self.dimension+1):
                new_simplessi[k]=[ [vertices.index(x) for x in s]  for s in simplices[k] ]
            self.simplices=new_simplessi
        elif simplices is not None:
            self.simplices=simplices
        elif maximal_simplices is not None:
            if must_reindex:
                new_simplessi={}
                for k in maximal_simplices.keys():
                    # print("k=",k,"maximal_simplices[k]=",maximal_simplices[k])
                    new_simplessi[k]=[ [vertices.index(x) for x in s]  for s in maximal_simplices[k] ]
            else:
                new_simplessi=maximal_simplices
            self.simplices=_populate_the_simplices(new_simplessi)
            self.dimension=max(self.simplices.keys())
        else:
            self.simplices=dict( [ (0, [[x] for x in range(len(vertices))] ) ] ) 
        
    def __repr__(self):
        return str(self)

    def __str__(self):
        str_list=[]
        for k in self.simplices.keys():
            tmpstr=("{}: {}".format(k, [ 
            [ self.vertices[j] for j in ind_simplex ] 
            for  ind_simplex in self.simplices[k] ])) 
            if len(tmpstr)>200:
                tmpstr="{}: {} simplices".format(k,len(self.simplices[k]))
            str_list += [tmpstr]
        str_simplices="\n  ".join(str_list)
        str_simplices_old=("\n  ".join( [("{}: {}".format(k, [ 
            [ self.vertices[j] for j in ind_simplex ] 
            for  ind_simplex in self.simplices[k] 
                                              ]  )   ) for k in self.simplices ] ))
        return "Simplicial Complex of dim {}:\n vertices: {}\n simplices:\n  {}".format(\
                self.dimension,self.vertices,str_simplices)
    def check(self):
        "check if it is really a simplicial complex"
        pass
    def __mul__(self,other):
        "cartesian product of simplicial complexes"
        return join_of_complexes(self,other,change_vertices=True)
    def __add__(self,other):
        return connected_sum(self,other)
    def __mod__(self,other):
        """ K % L is the cartesian product K x L$"""
        return cartesian_product(self,other)
    def rename_vertices(self,other):
        "append the string *other* to the names of the vertices"  
        new_vertices = ["{}{}".format(x,other) for x in self.vertices]
        return SimplicialComplex(new_vertices,simplices=self.simplices,maximal_simplices=self.maximal_simplices)

def dim(K):
    "dimension of the simplicial complex K"
    return K.dimension

def EPchar(K):
    """Euler-Poincaré characteristic
    
>>> K=simplicial_sphere(3)
>>> EPchar(K)
0
>>> K=simplicial_sphere(2)
>>> EPchar(K)
2
"""
    return sum([(-1)**k * len(K.simplices[k]) for k in range(K.dimension + 1) ] )

def dims_c(K):
    "list of the numbers of simplices in each dimension"
    return [len(K.simplices[k]) for k in range(dim(K)+1) ]

#------------------------------------------------------------
def simplicial_sphere(vertici):
    "sfera simpliciale: il bordo di un simplesso standard di dimension n con vertici la lista vertici"
    if isinstance(vertici,int):
        vertici=list(range(vertici+2))
    N=len(vertici) #dim + 1
    ind_seq=range(N)
    simplessi={}
    for k in range(N-1):
        simplessi[k] = [s for s in subsets(ind_seq,k+1)]
    return SimplicialComplex(vertici, simplices=simplessi)

#------------------------------------------------------------
def join_of_complexes(K,L,change_vertices=False):
    """make sure they do not have overlapping names..."""
    if change_vertices:
        vertici=list(range(len(K.vertices) + len(L.vertices)))
    else:    
        vertici=K.vertices + L.vertices
    offset=len(K.vertices)
    simplessi={}
    for k in range(dim(K) + dim(L) + 2):
        simplessi[k]=[]
    for i in K.simplices.keys():
        simplessi[i] += K.simplices[i]
    for j in L.simplices.keys():
        for tau in L.simplices[j]:
            simplessi[j] += [ [ (x + offset) for x in tau  ] ]
    for i in K.simplices.keys():
        for j in L.simplices.keys():
            for sigma in K.simplices[i]:
                for tau in L.simplices[j]:
                    simplessi[i+j+1] += [ sigma + [ (x + offset) for x in tau ]  ] 
    return SimplicialComplex(vertici,simplices=simplessi)


#--------------------------------------------------------------------------------
def disjoint_union(K,L):
    offset=len(K.vertices)
    try:
        vertici=K.vertices + [ x+offset for x in L.vertices ]
    except:
        vertici=K.vertices + [ "{}{}".format(x,"+") for x in L.vertices ]
    simplessi={}
    for k in range(dim(K)+1):
        simplessi[k]=K.simplices[k]
    for k in range(dim(L)+1):
        if k not in simplessi:
            simplessi[k]=[]
        simplessi[k] += [ [x+offset for x in sigma] for sigma in L.simplices[k] ]
    return SimplicialComplex(vertici,simplices=simplessi)

#--------------------------------------------------------------------------------
def connected_sum(K,L):
    """assume both have dim=2 and indices are ranges 0... n """
    K_vertices=list(range(len(K.vertices)))
    L_vertices=list(range(len(L.vertices)))
    if dim(K) !=2 or dim(L) != 2:
        print("They must be surfaces!")
        return None
    K_simplex=K.simplices[2][0]
    L_simplex=L.simplices[2][0] # take the first 2-simplex in both, and identify the indices... 
    offset=len(K_vertices)
    vertici=K_vertices + [ x+offset for x in L_vertices if x not in L_simplex ] 
    def identify(t):
        if isinstance(t,list):
            return [identify(x) for x in t]
        else:
            if not t in L_simplex:
                return vertici.index(t+offset)
            else:
                return K_simplex[L_simplex.index(t)]
    simplessi={}
    for k in range(3):
        simplessi[k] = [ x for x in K.simplices[k] if k<2 or x != K_simplex ]
        for tau in L.simplices[k]:
            itau=identify(tau)
            if itau not in simplessi[k] and itau != K_simplex :
                simplessi[k] += [ itau ]
    # simplessi[2] = [sigma for sigma in K.simplices[2] if sigma != [0,1,2]] +\
    #             [identify(tau) for tau in L.simplices[2] if tau != [0,1,2]  ]
    return SimplicialComplex(vertici,simplices=simplessi)                    

#--------------------------------------------------------------------------------
 
def _cartesian_product(lsts):
    return list(itertools.product(*lsts))

# @timeit
def cartesian_product(K,L):
    """Cartesian product of two Simplicial Complexes"""
    vertici=_cartesian_product([K.vertices , L.vertices ] )
    dim_K=K.dimension
    dim_L=L.dimension
    simplices={}
    simplices[0]=[ [( K.vertices.index(v) , L.vertices.index(w) ) ] for v,w in vertici  ] 
    for k in range(1,dim_K+dim_L+1):
        simplices[k]=[]
        for simpl in simplices[k-1]:
            i,j=simpl[-1]
            K_seq=list( { x[0] for x in simpl } ); K_seq.sort()
            len_K_seq=len(K_seq)
            L_seq=list( { x[1] for x in simpl } ); L_seq.sort()
            len_L_seq=len(L_seq)
            for x in range(i,len(K.vertices)):
                if (x == i) or  ( len_K_seq <= dim_K and (K_seq + [x] ) in K.simplices[len_K_seq]):
                    for y in range(j,len(L.vertices)):
                        if (y==j) or ( len_L_seq <= dim_L and (L_seq + [y] ) in L.simplices[len_L_seq]):
                            if  x!=i or y!=j:
                                simplices[k] += [ simpl + [(x,y)]] 
    new_simplices={}
    for k in range(dim_K+dim_L+1):
        new_simplices[k]=[[ (K.vertices[x],L.vertices[y]) for x,y in simpl ] for simpl in simplices[k] ] 
    return SimplicialComplex(vertici, simplices=new_simplices , must_reindex=True )


#--------------------------------------------------------------------------------

def faces_operators(K):
    """K is a simplicial complex. it returns the faces operators 
    dict with faces_operator[k] = [d_0,  ... d_j, ... d_k] 
    which send the dimplex at index x to the simplex at index d[j][x]"""
    result={}
    for k in range(1,dim(K)+1):
        result[k]=[ [K.simplices[k-1].index(seq_remove(j,sigma)) for sigma in K.simplices[k] ]  for j in range(k+1)]
    return result

#--------------------------------------------------------------------------------

def boundary_operators(K):
    """gives the list list of boundary operators \partial_k"""
    faces_ops=faces_operators(K)
    c=[len(K.simplices[k]) for k in range(dim(K)+1) ]
    result={}
    for k in  faces_ops.keys():
        if k==0:
            dk=zeros(1,c[0])
        else:    
            dk=zeros(c[k-1],c[k])
            for ncol in range(c[k]):
                for j in range(k+1):
                    dk[faces_ops[k][j][ncol],ncol]=(-1)**j 
        result[k]=dk 
    return result

#--------------------------------------------------------------------------------

def betti_numbers(K):
    """betti numbers: b[k] dim of boundaries; c[k] dim of chains; z[k] dim of cycles"""
    # c[k] = b[k-1] +z[k]  
    # h[k] = z[k] - b[k] 
    c=dims_c(K) # [len(K.simplices[k]) for k in range(dim(K)+1) ]
    d=boundary_operators(K)
    b=[]
    for k in range(dim(K)):
        sys.stdout.write("*")
        b += [ d[k+1].rank() ]
    b += [0]     
    z=[c[0] ] + [c[k] - b[k-1] for k in range(1,dim(K)+1) ]
    h= [ z[k] - b[k]  for k in range(dim(K)+1) ] 
    return h 

#--------------------------------------------------------------------------------
def row_echelon_form(M):
    nrows,ncols=M.shape
    tmpM=Matrix.hstack(M.copy(),eye(nrows))
    _row_echelon_form(tmpM)
    return (tmpM[:,:ncols] , tmpM[:,ncols:] )

def _row_echelon_form(A,starting_pivot=(0,0)):
    """return the row echelon form E (almost reduced) of matrix A, together with an invertible
matrix L such that LM=E

>>> K=simplicial_sphere(2)
>>> print(row_echelon_form(boundary_operators(K)[1] ))
1

"""
    spx,spy=starting_pivot
    nrows,ncols=A.shape[0], A.shape[1]
    if spx > nrows or spy > ncols:
        return "Finished"
    # find the first x for which A[x,0] != 0 
    done=False
    for y in range(spy,ncols):
        if not done:
            for x in range(spx, nrows):
                if A[x,y] != 0:
                    done=True
                    found_x=x
                    found_y=y
                    break
    if not done:
        # no pivots found
        # print("not done:")
        # pprint(A)
        return "Finished - no pivots found"
    x=found_x
    y=found_y
    # exchange rows
    if spx != x:
        A[spx,y:],A[x,y:] = A[x,y:],A[spx,y:]
    # normalize 
    A[spx,y:] = A[spx,y:] / A[spx,y] 
    # nullify the elements below (spx,spy)
    for xx in range(spx+1,nrows):
        A[xx,y:] += - A[spx,y:] * A[xx,y] 
    return _row_echelon_form(A,starting_pivot=(spx+1, y+1))


#--------------------------------------------------------------------------------
def LDR(M):
    """return a diagonal matrix D with 1 on the diagonal, and 0 later,
    such that LMR = D, with L and R invertible"""
    row_E,L = row_echelon_form(M) 
    D,R = row_echelon_form(row_E.T)
    return (L, D.T, R.T)
#--------------------------------------------------------------------------------
def shift_Z(c,r):
    """return the cxc matrix shifting the first r columns at the end, 
    by right matrix multiplication"""
    UL=zeros(r,c-r)
    UR=eye(r)
    LL=eye(c-r)
    LR=zeros(c-r,r)
    return Matrix.vstack( Matrix.hstack(UL,UR), Matrix.hstack(LL,LR) )

#--------------------------------------------------------------------------------
def rank_of_diagonal(D):
    """if D is diagonal with 1-s on the diagonal, return its rank"""
    nrows,ncols=D.shape
    r=0
    for x in range(min(nrows,ncols)):
        if D[x,x]==0:
            break
        else:
            r +=1 
    return r

#--------------------------------------------------------------------------------
def homology_groups(K):
    """generators (which form?) - not yet done"""
    d=boundary_operators(K)
    D=[0 for x in range(dim(K)+1)] 
    L=[0 for x in range(dim(K)+2)] 
    R=[0 for x in range(dim(K)+1)] 
    H=[0 for x in range(dim(K)+1)] 
    r=[0 for x in range(dim(K)+1)] 
    # first: k=0:
    c=dims_c(K)
    # then: compute all D,L,R: 
    # R[1] ... R[dim(K)] , 
    # D[1] ... D[dim(K)]
    # L[1] ... L[dim(K)]
    R[0]=eye(c[0])
    L[dim(K)+1]=eye(c[dim(K)])
    for k in range(1,dim(K)+1):
        ## L d R = D 
        L[k], D[k], R[k] = LDR( R[k-1].inv() * d[k] )
        r[k]=rank_of_diagonal(D[k])
        shift_matrix=shift_Z(c[k],r[k]) 
        D[k] = D[k] * shift_matrix  
        R[k] = R[k] * shift_matrix
    return (L,D,R,r)

    pprint(d[1])
    L, D, R =  LDR(d[1]) 
    r=rank_of_diagonal(D)
    pprint(D)
    Linv=L.inv()
    print("rank={}, c0={}".format(r,c[0]))
    basis_of_H = [Linv[:,x]  for x in range(r,c[0])]
    H[0] = basis_of_H 
    for k in range(1,dim(K)+1):
        sys.stdout.write("*")
        # L[k], D[k], R[k] =  LDR(d[k]) 
    return H
#--------------------------------------------------------------------------------

def main():
    pass



#--------------------------------------------------------------------------------
def old1_test():
    s0=( ["A","B"], [["A"],["B"]] ) 
    t0=( [0,1], [[0],[1]] )
    X=simplicial_sphere(['a','b'])
    Y=simplicial_sphere([0,1])
    print(X)
    print(Y)
    print("JOIN:")
    print(join_of_complexes(X,X.rename_vertices('+')) )
    print("last try")
    s0=simplicial_sphere(["A","B"])
    t0=simplicial_sphere([0,1,2])
    print("s0=", s0)
    print("t0=",t0)
    print(join_of_complexes(s0,t0))

    print("renamed:", X.rename_vertices('+'))
    # next: 
    # how to embed it? 
    # how to visualize it? 
    print("CARTESIAN PRODUCT")
    print(cartesian_product(s0,t0))

    s0=simplicial_sphere(3)
    t0=simplicial_sphere(1)
    print(cartesian_product(s0,t0))

    print("=" * 80 ) 
    print(len( [x for x in all_subsets([0,1,2,3]) ] ) )
    print()
    delta=SimplicialComplex([0,1,2],maximal_simplices={1:[[0,1],[1,2],[0,2]]})
    print(delta)
    print()
    delta=SimplicialComplex(["A","B","C",0],maximal_simplices={2:[["A","B","C"]],1:[[0,"A"]]},must_reindex=True)
    print(delta)
    maximal_simplices=[ sorted([x % 7, (x+1) % 7]) for x in range(7)]
    print(maximal_simplices)

    K=SimplicialComplex(list(range(7)),maximal_simplices={1:[ sorted([x % 7, (x+1)% 7]) for x in range(7)] } )
    print(K)
    print("faces_operators: ",faces_operators(K))
    
    K=simplicial_sphere(2)
    print(K)
    print("faces_operators: ",faces_operators(K))
    print("boundary_operators: ",boundary_operators(K))
    print("betti_numbers: ", betti_numbers(K) )

    for d,k in boundary_operators(K).items():
        print( d,k.rank() )

    s1=simplicial_sphere(1)
    s2=simplicial_sphere(1)
    K=cartesian_product(s1,s2)
    print(K)
    print("betti_numbers: ", betti_numbers(K) )

    s1=simplicial_sphere(1)
    s2=simplicial_sphere(1)
    K=disjoint_union(s1,s2)
    print("disjoint union:", K)
    print("betti_numbers: ", betti_numbers(K) )

    s1=simplicial_sphere(1)
    s2=simplicial_sphere(1)
    S=simplicial_sphere(2)
    T=s1 % s2
    print("T=", T)
    print("betti_numbers of T: ", betti_numbers(T) )
    T.vertices=list(range(len(T.vertices)))
    print("T=", T)
    print("dims_c:", dims_c(T))
    print("betti_numbers of T: ", betti_numbers(T) )
    print("EPchar: ", EPchar(T))

    K=T+T+T
    # print("vertici: ", K.vertices)
    # print("simplessi: ", K.simplices)
    print("connected_sum: ", K)
    print("dims_c:", dims_c(K))
    print("betti_numbers of T#S: ", betti_numbers(K) )
    print("EPchar(K): ", EPchar(K))

    s1=simplicial_sphere(1)
    s2=simplicial_sphere(1)
    K=s1 * s2 
    print("K ", K)
    print("dims_c:", dims_c(K))
    print("betti_numbers of K: ", betti_numbers(K) )
    print("EPchar(K): ", EPchar(K))

    K= (simplicial_sphere(1) % simplicial_sphere(0) )  * simplicial_sphere(0) + T
    print("K ", K)
    print("dims_c:", dims_c(K))
    print("betti_numbers of K: ", betti_numbers(K) )
    print("EPchar(K): ", EPchar(K))
    
#--------------------------------------------------------------------------------
def test():
    K=disjoint_union(simplicial_sphere(2), simplicial_sphere(1))
    T=simplicial_sphere(1) % simplicial_sphere(1)
    K=T
    print(K)
    print(betti_numbers(K))
    d=boundary_operators(K)
    M=d[1]
    # pprint(M)
    row_E,L = row_echelon_form(M) 
    # pprint(row_E)
    L,D,R,DD= homology_groups(K)
    for k in range(1,dim(K)+1):
        print("k=", k)
        # print( max( D[k] - D[k]*L[k+1].inv() ) ) 
        pprint(D[k])
        # good they are equal... 
        # R[k] * L[k+1].inv() are the matrices of the good bases of C[k] (chains):
        # first the z_k cycles, then the rest.
        # in the z_k cycles_ first b_k, then h_k. 
        # so: 0... r[k]-1, Homology[ r[k] ... z[k-1]]  z[k] ... 
    





#--------------------------------------------------------------------------------

if __name__=='__main__':
    test()
