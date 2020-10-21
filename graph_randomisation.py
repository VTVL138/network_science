import numpy as np

def degree_preserving_randomisation(graph,nr_rewirings):
    ''' 
    Return a randomised version of the graph, while preserving its edge-distribution.
    The graph must be undirected.
    Nr_rewirings is the number of edge swaps. Only the successful swaps count.
    We select 4 different nodes, after a swap new edge could not exist before, so it doesn't duplicate.

    Parameters
    ----------
    graph : networkx graph object

    nr_rewirings : number of successful edge swapping.

    Returns
    ------
    graph_copy : a new graph object, randomised, its edges are swapped nr_rewirings times randomly.
    '''
    graph_copy=graph.copy()
    count_rewirings=int(0)
    
    while count_rewirings < nr_rewirings:
        
        rand_edge_ids=np.random.randint(0,graph.number_of_edges(),2) # randomly select two edges
        
        if rand_edge_ids[0] != rand_edge_ids[1]:#different edges
            
            link_list=list(graph_copy.edges())
            
            s1,t1=link_list[rand_edge_ids[0]][0],link_list[rand_edge_ids[0]][1]# source, target of first edge
            
            s2,t2=link_list[rand_edge_ids[1]][0],link_list[rand_edge_ids[1]][1]# source, target of second edge

            if len(set([s1,t1,s2,t2])) == 4 and not graph_copy.has_edge(s1,t2) and not graph_copy.has_edge(s2,t1): # 4 different nodes, swapping them doesn'duplicate edges

                graph_copy.remove_edge(s1,t1)
                graph_copy.remove_edge(s2,t2)
                
                graph_copy.add_edge(s1,t2)
                graph_copy.add_edge(s2,t1)
                
                count_rewirings += 1
    
    return graph_copy
