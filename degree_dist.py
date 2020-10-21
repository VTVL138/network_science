from collections import Counter
from collections import OrderedDict
import numpy as np
import networkx as nx
import math as math

def degree_dist(graph,direction=None):
    ''' Return the degree distribution of graph.

        Parameters
        ----------
        graph : networkx object
        
        direction: None or string (in, out)
        
        By default the degree of a node equals to the number of undirected
        edges of a the node.
        
        If direction = in : We use the number of incoming degrees, as degree.
        
        If direction = out : We use the number of outgoing degrees, as degree.
        
        Returns
        -------
        degdist : dictionary, keys are degree, values are the possibilities of a given degree.
            
    '''
    nr_nodes=graph.number_of_nodes()
    
    if direction == None:
        degdist = Counter(sorted([d for n,d in graph.degree()],reverse=False))
    elif direction == 'out':
        degdist = Counter(sorted([d for n,d in graph.out_degree()],reverse=False))
    elif direction == 'in':
        degdist = Counter(sorted([d for n,d in graph.in_degree()],reverse=False))
    else:
        print('Direction format is not correct.')
    
    degdist = {k: v / nr_nodes  for k, v in degdist.items()}
    return degdist
    

def cum_degree_dist(graph,direction=None):
    ''' Return the cumulative degree distribution of graph. 
        At k value, the probability = 1-P(K < k)
        Parameters
        ----------
        graph : networkx object
        
        direction: None or string
        
        The default is all degree of a node.
        
        If direction = in : We use the number of incoming degrees, as degree.
        
        If direction = out : We use the number of outgoing degrees, as degree.
        
        Returns
        -------
        degdist : dictionary, degree as key, cumulative probabilities of a given degree as values.
            
    '''
    
    degdist = degree_dist(graph,direction)
    #sorted by degree values
    degdist = OrderedDict(sorted(degdist.items()))
    
    k_vals = list(degdist.keys())
    p_probs = list(degdist.values())
    
    cum_probs = []
    sub_list = []
    
    for i in range(len(k_vals)):
        sub_list.clear()
        sub_list = [x for x in p_probs[:i+1]]
        cum_probs.append(1-sum(sub_list))
    
    return dict(zip(k_vals,cum_probs))


def degree_dist_logbinned(graph,base=2,direction=None):
    ''' Return the degree distribution of graph with logarithmic binning. 
        The logartihmic binning could solve the issue of the non-equeal sampling.
        
        Parameters
        ----------
        graph : networkx object
        
        base : the base of exponentialy growing bin sizes, must be integer
        
        direction: None or string
        
            The default is all degree of a node.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.

        Returns
        -------
        degdist : dictionary, degree as key, cumulative probabilities of a given degree as values.
            
    '''
    degdist = degree_dist(graph,direction)
    degdist = OrderedDict(sorted(degdist.items()))#sorted by degree values:

    
    boundarys=[[base**(i-1),base**i] for i in range(1,int(math.log(max(degdist.keys()),base))+2)]
    
    k_vals_log=[]
    k_probs_log=[]
    
    for i in range(len(boundarys)):
        s=0 #for sum node probabilities in a bin
        tmp_degrees=[]
        tmp_degrees.clear()
        
        for j in range(boundarys[i][0],boundarys[i][1]):
            if j in degdist.keys():
                s+=degdist[j]
                tmp_degrees.append(j)
        k_vals_log.append(np.average(tmp_degrees))
        k_probs_log.append(s/(boundarys[i][1]-boundarys[i][0]))

    
    return dict(zip(k_vals_log,k_probs_log))
    
    

def degree_correlation(graph,direction=None):
    '''
    Degree correlation function, with the degree values.
    
    For a given k degree, k_nn(k) degree-correlation function gives the average
    value of the average degree of neighbours of node with k degree. 
    
    Parameters
    ----------
    graph : networkx object

    direction: None or string("in"|"out")

    If direction = None : All degrees are taken.
    If direction = in : The node's neighbours are at the end of in-degree and 
                        degree of a node is the in-degree.
    If direction = out : The node's neighbours are at the end of out-degree and 
                        degree of a node is the out-degree.

    
    
    Return:
    ------
    k_nn: dict(k,k_nn)
    '''
    
    
    d_dist = degree_dist(graph,direction=direction)
    nr_nodes = graph.number_of_nodes()
    d_dist = {k:v*nr_nodes for k,v in d_dist.items()}# we need the number of nodes , not the possibility
    
    k_nn=dict.fromkeys(list(d_dist.keys()),0)

    
    if direction == None:
        graph=graph.copy()
        graph=graph.to_undirected()
        avg_neighboursdeg = nx.average_neighbor_degree(graph)
        for n in graph.nodes():
            k_nn[graph.degree(n)]+=avg_neighboursdeg[n]
        
        
    elif direction == 'in':
        avg_neighboursdeg = nx.average_neighbor_degree(graph,source='in',target='in' )
        for n in graph.nodes():
            k_nn[graph.in_degree(n)]+=avg_neighboursdeg[n]
    
    elif direction == 'out':
        avg_neighboursdeg = nx.average_neighbor_degree(graph,source='out', target='out')
        for n in graph.nodes():
            k_nn[graph.out_degree(n)]+=avg_neighboursdeg[n]
    
    else:
        print('Direction format is not correct.')
    
    
    for k,v in k_nn.items():
        if d_dist[k]!=0:
            k_nn[k] /= d_dist[k] 
    
    return k_nn




