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
  1: 6 simplices


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
  0: 24 simplices
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


>>> K=simplicial_sphere([ "A","B","C" ] )
>>> L=simplicial_sphere([ "a","b","c" ])
>>> f=SimplicialMap({"A":"a","B":"c","C":"b"},K,L)
>>> g=SimplicialMap({"a":"A","b":"B","c":"B"},L,K)
>>> print(f)
SimplicialMap{'A': 'a', 'B': 'c', 'C': 'b'}
>>> print("is_simplicial f:", f.is_simplicial())
is_simplicial f: True
>>> print("is_simplicial_g:", g.is_simplicial())
is_simplicial_g: True
>>> print(f(["A","B"]) )
['a', 'c']
>>> print(f["C"] )
b
>>> print(f*g)
SimplicialMap{'a': 'a', 'b': 'c', 'c': 'c'}
>>> print(f*g*f)
SimplicialMap{'A': 'a', 'B': 'c', 'C': 'c'}
>>> print(homology_of_map(f))
[Matrix([[1]]), Matrix([[-1]])]
>>> print(homology_of_map(g))
[Matrix([[1]]), Matrix([[0]])]
>>> f=SimplicialMap({"A":"b","B":"b","C":"b"},K,L)
>>> print(f)
SimplicialMap{'A': 'b', 'B': 'b', 'C': 'b'}
>>> print(homology_of_map(f))
[Matrix([[1]]), Matrix([[0]])]
>>> K0=SimplicialComplex([0,1,2,3])
>>> K1=SimplicialComplex([0,1,2,3],maximal_simplices={1:[[0,1]],0:[[2],[3]]} )
>>> K2=SimplicialComplex([0,1,2,3],maximal_simplices={1:[[0,1],[0,2]],0: [ [3] ] } )
>>> K3=SimplicialComplex([0,1,2,3], maximal_simplices={1:[[0,1],[0,2],[1,2]], 0:[[3]] } )
>>> K4=SimplicialComplex([0,1,2,3],maximal_simplices={2:[[0,1,2]],0:[[3]] } )
>>> K5=K4
>>> filtration=[K0,K1,K2,K3,K4,K5]
>>> id_map={0:0,1:1,2:2,3:3}
>>> list_of_maps=[ SimplicialMap(id_map,filtration[j],filtration[j+1]) for j in range(len(filtration)-1)]
>>> for f in list_of_maps:
...     print("H:", homology_of_map(f))
H: [Matrix([
[1, 1, 0, 0],
[0, 0, 1, 0],
[0, 0, 0, 1]])]
H: [Matrix([
[1, 1, 0],
[0, 0, 1]]), Matrix(0, 0, [])]
H: [Matrix([
[1, 0],
[0, 1]]), Matrix(1, 0, [])]
H: [Matrix([
[1, 0],
[0, 1]]), Matrix(0, 1, [])]
H: [Matrix([
[1, 0],
[0, 1]]), Matrix(0, 0, []), Matrix(0, 0, [])]
>>> PH=persistent_homology(list_of_maps)
>>> print("PH:", PH)
PH: {0: [(0, 5), (0, 1), (0, 2), (0, 5)], 1: [(3, 4)], 2: []}
"""

#------------------------------------------------------------
import time
import numpy as np
import itertools
from sympy.matrices import * 
from sympy import pprint
from sympy import combinatorics
import sys
#------------------------------------------------------------
# just the decoration... 
MAX_NUMBER=3
MAX_OUTPUT_LENGTH=120
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
class Point:
    """Just a point of a euclidean space of dimension 2 or 3 or more. 
    It may have a label.

EXAMPLES:
---------

>>> P=Point((1,0),label="A")
>>> print(P)
A=(1, 0)
>>> Q=Point((2,3),label="Q")
>>> print(Q)
Q=(2, 3)
>>> Z=Point((1,13,3))
>>> print(Z)
(1, 13, 3)
"""
    def __init__(self,coords, label=None):
        self.label=label
        self.coords=coords
        self.dim=len(coords)
        if not isinstance (coords,tuple):
            raise Exception("Missing coordinates tuple!")
        return
    def __str__(self):
        if self.label:
            return "%s=%s" % (self.label,self.coords)
        else:
            return "%s" % (self.coords,)
    def __repr__(self):
        if self.label:
            return self.label
        else:
            return "%s" % (self.coords,)


#------------------------------------------------------------

def display_2d(K,show_labels=False):
  """
  display_2d a 1-dimensional simplicial complex (in the plane). 
  if vertices are points. Better in jupyter. 
  """
  import matplotlib.pyplot as plt
  from matplotlib.collections import LineCollection
  if not isinstance(K.vertices[0] ,Point):
    raise Exception("Can display only Point-class vertices of dim 2!!!")
  dim=K.vertices[0].dim
  if dim != 2:
    sys.stderr.write("Not yet implemented display in dim = %s\n" % dim ) 
    return None
  vertices =  K.vertices
  if 1 in K.simplices:
      edges = [ [vertices[i].coords,vertices[j].coords] for (i,j) in K.simplices[1] ]
  else:
      edges = []

  fig = plt.figure(figsize=(10.0,10.0))
  ax = fig.gca()
  ax.set_aspect('equal', adjustable='datalim')
  ax.set_axis_off()
  fig.set_facecolor('white')

  lc = LineCollection(edges, color="black", lw=2)
  ax.add_collection(lc)

  for P in vertices:
      ax.add_patch(plt.Circle(P.coords, 0.005, edgecolor='black',
                        linewidth=2, rasterized=False, antialiased=True,facecolor='w',
                        zorder=1000) )
      if show_labels and P.label is not None:
          Px,Py = P.coords
          ax.annotate("$%s$" % repr(P), P.coords , (Px+0.03,Py+0.01),fontsize=24, color='blue')

  ax.plot()   #autoscale update.
  plt.show()

#------------------------------------------------------------

def display_3d(K,show_labels=False):
    """display a 3d simplicial complex using k3d, in jupyter

    to install it: 
    sudo pip install k3d
    sudo jupyter nbextension install --py k3d
    sudo jupyter nbextension enable --py k3d
    """
    import k3d
    if not isinstance(K.vertices[0] ,Point):
        raise Exception("Can display only Point-class vertices of dim 3!!!")
    dim=K.vertices[0].dim
    if dim != 3:
        sys.stderr.write("Not yet implemented display in dim = %s\n" % dim ) 
        return None
    vertices =  [v.coords for v in K.vertices] 
    edges = [ s for s in K.simplices[1] ]
    faces = []
    if 2 in K.simplices:
        faces = [ s for s in K.simplices[2] ]
    plt=k3d.plot(name='points')
    plt_points = k3d.points( positions=vertices , point_size=0.05)
    plt_points.shader ='3dSpecular'
    plt_points.color = 14
    plt += plt_points

    # now lines:
    for s in edges:
        plt_line = k3d.line([vertices[s[0]],vertices[s[1]] ],shader='mesh', width=0.01, 
                            color=0xff0000)
        plt += plt_line 

    # now convert all faces to a mesh
    plt_mesh = k3d.mesh(vertices,faces,color=0xff, wireframe=False, opacity=0.7, name="Simplicial Complex")
    plt += plt_mesh

    # now add the text
    for P in K.vertices:
        if show_labels and P.label is not None:
            plt_text = k3d.text("%s" % repr(P), position = P.coords, color=0x7700,size=1)
            plt += plt_text 
      
    #finally display
    plt.display()
   

#------------------------------------------------------------
class SimplicialComplex:
    """If just the set of verties: 0-dim simplicial complex. 
Otherwise, simplices, which is a dictionary of integer indices i.e. simplices.
Otherwise, just maximal_simplices, and simplices are populated.
if must_reindex=True, simplices in terms of symbols will be converted
to simplices in terms of integer indices
       
**operations**:

 -  connected_sum     +  
 -  join              *  
 -  cartesian_product %  
 -  disjoint_union   


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
    def __init__(self,vertices,simplices=None,maximal_simplices=None,must_reindex=False,must_sort=True):
        """Class init arguments: 
>>> K=SimplicialComplex([0,1,2],must_reindex=True,maximal_simplices={2: [[0,1,2]] })
"""
        if not isinstance(vertices,list) or len(vertices)==0:
            raise Exception("vertices should be a non-empty list!")
        #first a little bit of input checking 
        if isinstance(vertices[0],Point):
            self.is_euclidean=True
            self.euclidean_dim=vertices[0].dim
            self.str_is_euclidean="%s-Euclidean " % self.euclidean_dim
        else:
            self.is_euclidean=False 
            self.str_is_euclidean=""
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
                new_simplessi[k]=[ sorted( [vertices.index(x) for x in s] )  for s in simplices[k] ]
            self.simplices=new_simplessi
        elif simplices is not None:
            self.simplices=simplices
        elif maximal_simplices is not None:
            if must_reindex:
                new_simplessi={}
                for k in maximal_simplices.keys():
                    # print("k=",k,"maximal_simplices[k]=",maximal_simplices[k])
                    new_simplessi[k]=[ sorted( [vertices.index(x) for x in s]  ) for s in maximal_simplices[k] ]
            else:
                new_simplessi=maximal_simplices
            self.simplices=_populate_the_simplices(new_simplessi)
            for iv in range(len(self.vertices)):
                if [iv] not in self.simplices[0]:
                    self.simplices[0] += [ [iv] ] ## add the vertices, if not already there
            self.dimension=max(self.simplices.keys())
        else:
            self.simplices=dict( [ (0, [[x] for x in range(len(vertices))] ) ] ) 
        self.dims_c=[len(self.simplices[k]) for k in range(self.dimension+1) ] 
    def __repr__(self):
        return str(self)
    def __str__(self):
        str_list=[]
        for k in self.simplices.keys():
            tmpstr=("{}: {}".format(k, [ 
            [ (self.vertices[j]) for j in ind_simplex ] 
            for  ind_simplex in self.simplices[k] ])) 
            if len(tmpstr)>MAX_OUTPUT_LENGTH:
                tmpstr="{}: {} simplices".format(k,len(self.simplices[k]))
            str_list += [tmpstr]
        str_simplices="\n  ".join(str_list)
        return "{}Simplicial Complex of dim {}:\n vertices: {}\n simplices:\n  {}".format(\
                self.str_is_euclidean, self.dimension, self.vertices,str_simplices)
    def simplex_vertices(self,ind_simplex):
        """return the list of vertices of a index_simplex (i.e. a list of indices of vertices)"""
        return [self.vertices[j] for j in ind_simplex]
    def simplex_indices(self,list_of_vertices):
        """return the list of vertices corresponding to a list of indices"""
        return [self.vertices.index(x) for x in list_of_vertices]
    def check(self):
        r"""check if it is really a simplicial complex

>>> K=SimplicialComplex(["a","b",2,3,4],maximal_simplices={1: [[0,1]]})
>>> print("K:", K)
K: Simplicial Complex of dim 1:
 vertices: ['a', 'b', 2, 3, 4]
 simplices:
  0: [['a'], ['b'], [2], [3], [4]]
  1: [['a', 'b']]
>>> print("check:", K.check() ) 
check: True
"""
        for k in range(self.dimension,0,-1):
            for simpl in self.simplices[k]:
                for j in range(k+1):
                    if seq_remove(j,simpl) not in self.simplices[k-1]:
                        return False
        return True            
    def __mul__(self,other):
        "join of two simplicial complexes: K * L"
        return join_of_complexes(self,other,change_vertices=True)
    def __add__(self,other):
        "K + L : connected sum of two triangulated surfaces K and L"
        return connected_sum(self,other)
    def __mod__(self,other):
        """ K % L is the cartesian product K x L"""
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
    return K.dims_c 

#------------------------------------------------------------
class SimplicialMap:
    """ simple class to store the data of a simplicial map f : K -> L"""
    def __init__(self,f,K,L):
        """ f is a dict { x : f(x) } for x in vertices of K, 
K is the domain,
L is the codomain"""
        self.f=f #dict
        self.K=K #simpl complex
        self.L=L #simpl complex
    def __str__(self):
        tmpstr="SimplicialMap{}".format(self.f)
        if len(tmpstr)>MAX_OUTPUT_LENGTH:
            tmpstr=tmpstring[:(MAX_OUTPUT_LENGTH-3)]+"..."
        return tmpstr
    def is_simplicial(self):
        "check if it is really a simplicial map" 
        for x in self.K.vertices:
            if x not in self.f: #a vertex does not have image
                print("{} not a key".format(x))
                return False
            if self.f[x] not in self.L.vertices:
                print("{} not in L.vertices".format(x))
                return False   #image not defined
        for k in range(dim(self.K)+1):
            for s in self.K.simplices[k]:
                tmps=sorted(list({ self.L.vertices.index(self.f[x]) for x in  self.K.simplex_vertices(s) } ) )
                if tmps not in self.L.simplices[len(tmps)-1]:
                    print("{} not in L.simplices".format(tmps))
                    return False
        return True
    def __mul__(self,other):
        "f * g : composition: assume img (g) = dom (f) "
        return SimplicialMap( { x : self [ other [x] ]  for x in other.K.vertices } , other.K,self.L)
    def __call__(self,other):
        "evaluate the function on simplices: f([v1,v2]), applied on simplices"
        return [ self.f[x] for x in other]
    def __getitem__(self,other):
        "evaluate the function on vertices: f[v] applied on vertices"
        return self.f[other]
    def in_chains(self):
        "chain map induced by f, represented as matrix, for each k = 0... dim K"
        result={}
        for k in range(dim(self.K)+1):
            mat=zeros(self.K.dims_c[k],self.L.dims_c[k])
            for ind_s in range(len(self.K.simplices[k])):
                sign,indices= sign_ordered(  self.L.simplex_indices( 
                 self(self.K.simplex_vertices(self.K.simplices[k][ind_s]))) )
                if indices is not None: #and sign != 0! 
                    mat[self.L.simplices[k].index(indices),ind_s] = sign
            result[k]= mat
        return  result

#------------------------------------------------------------

def sign_ordered(seq):
    "0 (zero) if it is not injective, otherwise sign of the permutation of the sequence seq of integers"
    # seq is a sequence of (not necessarily distinct) integers: first sort it
    # 1,5,4 -> 1,4 5 => permutation [0,2,1] 
    n=len(seq)
    nseq=len(list(set(seq)))
    if nseq < n :
        return (0, None)
    sorted_seq=sorted(seq)
    p=combinatorics.Permutation([sorted_seq.index(seq[x]) for x in range(len(seq)) ])
    sign=(-1)**p.parity()
    return (sign,sorted(seq))


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
    if K.is_euclidean and L.is_euclidean:
        vertici= [ Point( v.coords + ((0,)*L.euclidean_dim), label=v.label ) for v in K.vertices ] + \
                 [ Point( ( (0,) * K.euclidean_dim )  + w.coords, label=w.label)   for w in L.vertices ] 
    elif change_vertices:
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
    "disjoint union of K and L" 
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
    """Connected sum of K and L : assume both have dim=2 and indices are ranges 0... n """
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

# --------------------------------------------------------------------------------

def _cartesian_product(lsts,both_euclidean=False):
    if len(lsts)==2 and both_euclidean:
        vertici= [ Point( (v.coords + w.coords ), label="(%s,%s)" % (v.label,w.label) )
                for v,w in itertools.product(*lsts) ]
        return vertici
    return list(itertools.product(*lsts))

# @timeit
def cartesian_product(K,L):
    """Cartesian product of two Simplicial Complexes"""
    if K.is_euclidean and L.is_euclidean:
        both_euclidean=True
    else:
        both_euclidean=False
    eucl_vertici=_cartesian_product([K.vertices , L.vertices ] ,both_euclidean=both_euclidean)
    vertici=_cartesian_product([K.vertices , L.vertices ] ,both_euclidean=False)
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
    tmp_result =  SimplicialComplex(vertici, simplices=new_simplices , must_reindex=True)
    return SimplicialComplex(eucl_vertici,simplices=tmp_result.simplices, must_reindex=False)


# --------------------------------------------------------------------------------

def faces_operators(K):
    """K is a simplicial complex. it returns the faces operators 
    dict with faces_operator[k] = [d_0,  ... d_j, ... d_k] 
    which send the dimplex at index x to the simplex at index d[j][x]"""
    result={}
    for k in range(1,dim(K)+1):
        result[k]=[ [K.simplices[k-1].index(seq_remove(j,sigma)) for sigma in K.simplices[k] ]  for j in range(k+1)]
    return result

# --------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------

def betti_numbers(K):
    """Betti numbers: b[k] dim of boundaries; c[k] dim of chains; z[k] dim of cycles"""
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
def row_echelon_form(M,get_pivots=False):
    """return the row echelon form E (almost reduced) of matrix A, together
    with an invertible matrix L such that LM=E; if get_spivots is True, 
    output the list of pivots as well.

>>> K=simplicial_sphere(2)
>>> print(row_echelon_form(boundary_operators(K)[1] ))
(Matrix([
[1, 1, 1, 0, 0, 0],
[0, 1, 1, 1, 1, 0],
[0, 0, 1, 0, 1, 1],
[0, 0, 0, 0, 0, 0]]), Matrix([
[-1,  0,  0, 0],
[-1, -1,  0, 0],
[-1, -1, -1, 0],
[ 1,  1,  1, 1]]))
"""
    nrows,ncols=M.shape
    tmpM=Matrix.hstack(M.copy(),eye(nrows))
    pivots=_row_echelon_form(tmpM)
    if nrows == 0 or ncols==0:
        pivots=[] #strange...
    if get_pivots:
        return (tmpM[:,:ncols] , tmpM[:,ncols:] ,pivots)
    else:    
        return (tmpM[:,:ncols] , tmpM[:,ncols:] )

def _row_echelon_form(A,starting_pivots=[(0,0)],do_nothing=False):
    """In-place Row Echelon Form of matrix M, with the list of pivots. If
    do_nothing is True (for example, if A is already echelon) it just returns
    the pivots"""
    spx,spy=starting_pivots[-1]
    nrows,ncols=A.shape
    if spx >= nrows or spy >= ncols:
        return starting_pivots[:-1]
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
        return starting_pivots[:-1] 
    starting_pivots[-1]=(spx,found_y)
    x=found_x
    y=found_y
    # exchange rows
    if do_nothing: #it means that A is already in row echelon form
        return _row_echelon_form(A,starting_pivots=starting_pivots + [(spx+1, y+1)], do_nothing=True )
    if spx != x: 
        A[spx,y:],A[x,y:] = A[x,y:],A[spx,y:] # swap the rows
    # normalize 
    A[spx,y:] = A[spx,y:] / A[spx,y] 
    # nullify the elements below (spx,spy)
    for xx in range(spx+1,nrows):
        A[xx,y:] += - A[spx,y:] * A[xx,y] 
    return _row_echelon_form(A,starting_pivots=starting_pivots + [(spx+1, y+1)]  )


#--------------------------------------------------------------------------------
def LDR(M):
    """return a diagonal matrix D with 1 on the diagonal, and 0 later,
    such that LMR = D, with L and R invertible"""
    row_E,L  = row_echelon_form(M) 
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
def is_pivot(j,mat):
    """ return true if j is a pivot of a row-echelon-form matrix"""
    return j in [ x[1] for x in all_pivots(mat)]

def all_pivots(mat):
    """ return all the pivot of a row-echelon-form matrix"""
    nrows,ncols=mat.shape
    if nrows == 0 or ncols==0:
        return [] #strange...
    return _row_echelon_form(mat,starting_pivots=[(0,0)],do_nothing=True)

#--------------------------------------------------------------------------------
def homology(K):
    r"""generators and projectors of each homology group
it returns the 5-tuple L,shifted(D),R,r,H  where

L,D,R are sequences of matrices, for k=0 .. dim(K),
such that such that for each k the matrix D[k] is diagonal and

    L[k] * boundary_operator[k] * R[k] = D[k] 

r is the list of ranks of boundary_operator[:] 

H is a list of `dicts`  
Each H[k] is a `dict` with two keys: `gens` and `hcm`. 

    H[k]['gens'] is the list of generators of the k-th homology
    H[k]['hcm'] is the homology class matrix. It is the
    projection from cycles to homology in base given by generators. 

>>> S=simplicial_sphere(2)
>>> L,D,R,r,H = homology(S)
>>> for k in range(dim(S)+1):
...     print("k=", k, "\nL,D,R = ", L[k],D[k],R[k],"\nrank: ", r[k],"\n", H[k])
k= 0 
L,D,R =  None None Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) 
rank:  0 
 {'gens': [Matrix([
[0],
[0],
[0],
[1]])], 'hcm': Matrix([[1, 1, 1, 1]])}
k= 1 
L,D,R =  Matrix([[-1, 0, 0, 0], [-1, -1, 0, 0], [-1, -1, -1, 0], [1, 1, 1, 1]]) Matrix([[0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]) Matrix([[1, 0, 0, 1, -1, 0], [-1, 1, 0, 0, 1, -1], [0, -1, 0, 0, 0, 1], [1, -1, 1, 0, 0, 0], [0, 1, -1, 0, 0, 0], [0, 0, 1, 0, 0, 0]]) 
rank:  3 
 {'gens': [], 'hcm': Matrix(0, 6, [])}
k= 2 
L,D,R =  Matrix([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]) Matrix([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]) Matrix([[1, 1, -1, 1], [-1, 0, 1, -1], [1, 0, 0, 1], [-1, 0, 0, 0]]) 
rank:  3 
 {'gens': [Matrix([
[ 1],
[-1],
[ 1],
[-1]])], 'hcm': Matrix([[0, 0, 0, -1]])}
"""
    d=boundary_operators(K)
    D=[None for x in range(dim(K)+1)] 
    L=[None for x in range(dim(K)+2)] 
    R=[None for x in range(dim(K)+1)] 
    H=[None for x in range(dim(K)+1)] 
    r=[0 for x in range(dim(K)+2)] 
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
        r[k]=rank_of_diagonal(D[k]) ## TODO: just take it from the pivot list
        shift_matrix=shift_Z(c[k],r[k]) 
        D[k] = D[k] * shift_matrix  
        R[k] = R[k] * shift_matrix
    for k in range(dim(K)+1):    
        gens_of_H = [(R[k]*L[k+1].inv())[:,x]  for x in range(r[k+1],c[k]-r[k])]
        hk=len(gens_of_H)
        homology_class_matrix= Matrix.hstack( zeros(hk,r[k+1]), 
                eye(hk), zeros(hk,r[k]) ) * L[k+1] * R[k].inv() 
        H[k]={'gens': gens_of_H,'hcm':homology_class_matrix} #matrix of the projection C_k -> H_k
    return (L,D,R,r,H)
# now the c[k] elements of the basis of Q^(c[k]) are in the following order 
    # b[0] ... b[r[k+1]-1] (image of D[k+1] & \
            # x[0] .... x[h[k]-1] (generators of Homology H[k])
    # b'[0]...b'[r[k]-1] (complemento ortogonale di Ker D[k])

#--------------------------------------------------------------------------------
def _print_gen_array(K_simplices,M):
    "K simplicial complex, M is the matrix (vector) representing the chain in K"
    nrows,ncols=M.shape
    if ncols != 1:
        raise Exception("ncols != 1!!!")
    if nrows != len(K_simplices):
        raise Exception("nrows != len(K_simplices)!")
    result=[]
    for j in range(nrows):
        if M[j,0] != 0:
            result += [ ( M[j,0], K_simplices[j] ) ] 
    return result

#--------------------------------------------------------------------------------
def homology_of_map(f):
    """ f is  SimplicialMap: comput the matrix of its homology

>>> K=simplicial_sphere([ "A","B","C" ] )
>>> L=simplicial_sphere([ "a","b","c" ])
>>> f=SimplicialMap({"A":"a","B":"c","C":"b"},K,L)
>>> print(homology_of_map(f))
[Matrix([[1]]), Matrix([[-1]])]
"""
    LK,DK,RK,rK,HK=homology(f.K)
    LL,DL,RL,rL,HL=homology(f.L)
    F=f.in_chains()
    result=[None for x in range(dim(f.K)+1)]
    for k in range(dim(f.K)+1):
        mat=zeros(len(HL[k]['gens']),len(HK[k]['gens']) )
        for ind_x, x in enumerate(HK[k]['gens']):
            mat[:, ind_x] =  HL[k]['hcm'] * F[k] * x
        result[k]=mat
    return result   

#--------------------------------------------------------------------------------

def persistent_homology(list_of_maps):
    """**very** simple computation of persistent homology of a sequence of induced chain maps,
using a naive row-echelon-form reduction of each homology morphism. It returns a list of pairs
corresponding to time-of-birth and time-of-death, one for each generator of the homology.

>>> filtration=[
... SimplicialComplex([0,1,2]),
... SimplicialComplex([0,1,2],maximal_simplices={1:[[0,1]] } ),
... SimplicialComplex([0,1,2],maximal_simplices={1:[[0,1],[0,2]] } ) ,
... simplicial_sphere([0,1,2]) ,
... SimplicialComplex([0,1,2], maximal_simplices={2:[[0,1,2]] }) ,
... ]
>>> id_map={0:0,1:1,2:2}
>>> list_of_maps=[ SimplicialMap(id_map,filtration[j],filtration[j+1]) for j in
... range(len(filtration)-1)]
>>> PH=persistent_homology(list_of_maps)
>>> print("PH:", PH)
PH: {0: [(0, 4), (0, 1), (0, 2)], 1: [(3, 4)]}


It means that for the 0-th homology there are 3 generators, one survives all times,
one dies soon, the other after two steps. 
In degree 1, there is just one generator, born at k=3 and dead in k=4.
"""
    nmaps=len(list_of_maps)
    mats_arrays =[ homology_of_map(f) for f in list_of_maps ]
    max_k= max( len(Hs) for Hs in  mats_arrays )
    result= {}
    generators={}
    birth_death_pairs={}
    for k in range(max_k):
        result[k] = [None for x in range(nmaps)]
        generators[k]=[]
        birth_death_pairs[k]=[]
        for j in range(nmaps):
            if k < len( mats_arrays[j]):
                result[k][j]=mats_arrays[j][k]
        for j in range(nmaps):
            if result[k][j] is not None:
                if j>0 and result[k][j-1] is not None:
                    Lp=L; rankp=len(pivots); # print(pivots)
                    M,L,pivots = row_echelon_form(result[k][j] * Lp.inv() ,get_pivots=True)
                else:
                    M,L,pivots = row_echelon_form(result[k][j] ,get_pivots=True)
                result[k][j] = M    
                # now: generators born at j are the generators of 0-th hom, and those *not*
                # belonging to the image (given by pivots). 
                if j==0:
                    generators[k] += [ (j, x) for x in range( M.shape[1] ) ] 
                elif result[k][j-1] is not None:
                    generators[k] += [ (j,x) for x in range(M.shape[1]) if x >= rankp ] 
                else:
                    generators[k] += [ (j, x) for x in range( M.shape[1] ) ] 
        #now get their deaths...
        # first: array of compositions matrices (fixed k): H_i -> H_j, for i<j.
        # and i,j = 0 .. nmaps
        composed=[ [None for i in range(nmaps+1)] for j in range(nmaps+1) ] 
        for j in range(nmaps):
            composed[j][j+1] = result[k][j]
            for i in range(j+2,nmaps+1):
                if result[k][i-1] is not None and composed[j][i-1] is not None:
                    composed[j][i] = result[k][i-1] * composed[j][i-1]
        for j,g in generators[k]:
            # g is a generator in the domain of f_j, the index of the basis element
            is_alive=True
            here=j
            while is_alive:
                if here < nmaps: 
                    here += 1
                    Hjhere_mat=composed[j][here] 
                    if Hjhere_mat is None: 
                        is_alive=False
                    else:
                        # if img_of_g is a pivot, it is alive. otherwise, dead. 
                        if not is_pivot(g,Hjhere_mat):
                            is_alive=False
                else:
                    is_alive=False
            birth_death_pairs[k] += [ (j,here) ]
    return birth_death_pairs

#--------------------------------------------------------------------------------

def sq_euc_norm(P):
    result=0.0
    for j in range(len(P)):
        result += P[j] * P[j]
    return result

def euc_norm(P):
    sq_result = sq_euc_norm(P)
    return sq_result ** (0.5)

def distance(P, Q):
    result = euc_norm(P-Q)
    return result

def vector_product(P,Q):
    vector_product=np.zeros(3)
    vector_product[0] = P[1] * Q[2] - Q[1] * P[2]
    vector_product[1] = Q[0] * P[2] - P[0] * Q[2]
    vector_product[2] = P[0] * Q[1] - Q[0] * P[1]
    return vector_product

def dot_product(P,Q):
    return np.dot(P,Q)

# Try to embed a simplicial complex... 
class Embed:
    """ Class for finding a suitable euclidean embedding of simplicial complexes"""
    import scipy.optimize as optimize
    def __init__(self,elastic_constant=1.0):
        self.elastic_constant=elastic_constant
        return

    def Uij(self,P,Q,are_endpoints=False):
        """interaction of P and Q: edges elastic attract, all repulsive"""
        if are_endpoints:
            return self.elastic_constant * sq_euc_norm(P-Q) + 1. / euc_norm(P-Q)
        else:
            return 1. / euc_norm(P-Q)

    def grad_Uij(self,P,Q,are_endpoints=False):
        """grad of interaction of P and Q, wrt P"""
        if are_endpoints:
            return 2.0 * self.elastic_constant * (P-Q) - (P-Q) * euc_norm(P-Q)**(-3.)
        else:
            return - (P-Q) * euc_norm(P-Q)**(-3.)

    def potential(self,conf,is_edge):
        energy = 0.0
        number_of_vertices,eucl_dim=conf.shape
        for i in range(number_of_vertices-1):
            for j in range(i + 1, number_of_vertices ):
                if is_edge[i,j]:
                    energy += self.Uij( conf[i,:],conf[j,:], are_endpoints=True )
                else:
                    energy += self.Uij( conf[i,:],conf[j,:], are_endpoints=False)
        return energy

    def grad_potential(self,conf,is_edge):
        number_of_vertices,eucl_dim=conf.shape
        grad = np.zeros((number_of_vertices,eucl_dim))
        for i in range(number_of_vertices-1):
            for j in range(i + 1, number_of_vertices ):
                if is_edge[i,j]:
                    grad[i,:] += self.grad_Uij( conf[i,:],conf[j,:], are_endpoints=True )
                    grad[j,:] += self.grad_Uij( conf[j,:],conf[i,:], are_endpoints=True )
                else:
                    grad[i,:] += self.grad_Uij( conf[i,:],conf[j,:], are_endpoints=False )
                    grad[j,:] += self.grad_Uij( conf[j,:],conf[i,:], are_endpoints=False )
        return grad

    def euclidean_embedding(self,K, dim=2):
        """return the Euclidean Embedding of the abstract complex K, 
        using suitable interaction potentials (vertices and edges).
        it needs to import scipy.optimize. 
        """
        vertices = K.vertices
        edges = []
        if 1 in K.simplices:
            edges = K.simplices[1]
        number_of_vertices=len(vertices)
        eucl_dim=dim

        is_edge=np.zeros( (number_of_vertices,)*2 , dtype=bool)
        for (i,j) in edges:
            is_edge[i,j]=True

        def opt_fun(x):
            conf=x.reshape(number_of_vertices,eucl_dim)
            result = self.potential(conf,is_edge)
            return result
        
        def opt_jac(x):
            conf=x.reshape(number_of_vertices,eucl_dim)
            result = self.grad_potential(conf,is_edge)
            return result.reshape(number_of_vertices*eucl_dim)

        X0=np.random.rand( number_of_vertices,eucl_dim )
        result = self.optimize.minimize(opt_fun,X0,method='CG',jac=opt_jac)
        
        outconf=result.x.reshape(number_of_vertices,eucl_dim)
        howsol=euc_norm(result.jac)
        print("howsol: {}".format(howsol))
        eucl_vertices= [ Point( tuple( outconf[i,:] ), label=str(i) )  
                for i in range(number_of_vertices) ]
        return SimplicialComplex(eucl_vertices,simplices=K.simplices)

#--------------------------------------------------------------------------------

def view(K,show_labels=False):
    """Display a euclidean simplicial complex"""
    if not K.is_euclidean:
        print("Sorry: cannot view a non-euclidean complex:\n {}".format(str(K)))
        return 
    if K.euclidean_dim==2:
        display_2d(K,show_labels=show_labels)
    elif K.euclidean_dim==3:
        display_3d(K,show_labels=show_labels)
    else:
        print("Sorry: cannot view a euclidean complex of dim {}".format(K.euclidean.dim) )
    return     

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
def old2_test():
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
    L,D,R,DD= homology(K)
    for k in range(1,dim(K)+1):
        print("k=", k)
        # print( max( D[k] - D[k]*L[k+1].inv() ) ) 
        pprint(D[k])
        # good they are equal... 
        # R[k] * L[k+1].inv() are the matrices of the good bases of C[k] (chains):
        # first the z_k cycles, then the rest.
        # in the z_k cycles_ first b_k, then h_k. 
        # so: 0... r[k]-1, Homology[ r[k] ... z[k-1]]  z[k] ... 

# --------------------------------------------------------------------------------


def test():
    # S1=simplicial_sphere(['A','B','C']) 
    S1=simplicial_sphere(1)
    T=S1 % S1 %S1
    K=S1
    L,D,R,r,H = homology(K)
    for k in range(dim(K)+1):
        # print("k=",k)
        # print(H[k])
        gens=H[k]['gens']
        print("len gens:", len(gens) ) 
        homology_class_matrix=H[k]['hcm']
        for x in gens:
            print(_print_gen_array([K.simplex_vertices(s) for s in K.simplices[k]],x))
    L=S1
    f=SimplicialMap({0:0,1:1,2:2}, K, L)
    print( f * f )
    S=simplicial_sphere(1)
    print(S)
    Emb=Embed()
    ES=Emb.euclidean_embedding(S,dim=3)
    print(ES)
    view(ES,show_labels=True)

# --------------------------------------------------------------------------------

if __name__=='__main__':
    test()
