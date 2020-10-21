import networkx as nx
import numpy as np
def m_reaching_centrality(graph,m=None,direction=None):
    '''
    The network must be connected.
    The local reaching centrality (LRC) of a node is 
    the proportion of the nodes that could be reached from a given node 
    and the number of nodes in the network minus 1.
    The m-LRC is a cutoff after the n-th step from the given node.
    
    Parameters:
    ----------
    graph: networkx object, must be connected
    
    m : cutoff after n step distance
    
    direction: (None|"in"|"out") A node could reach another one only through in- or out-edge,
                or both of them, if the network is undirected.
    
    
    
    Returns:
    -------
    reaches: Dict of nodes with LRC values.

    
    '''
#    if not nx.is_connected(graph):# it works only on undirected graphs
#        print('Graph must be connected.')
#        return {}


    nr_nodes=graph.number_of_nodes()
    
    if direction == None:
        graph = graph.copy()
        graph = graph.to_undirected()
        reaches = [(len(nx.single_source_shortest_path(graph,n,cutoff=m))-1)/(nr_nodes-1) for n in graph.nodes()]

    elif direction == 'in':
        graph = graph.copy()
        graph = graph.reverse()
        reaches = [(len(nx.single_source_shortest_path(graph,n,cutoff=m))-1)/(nr_nodes-1) for n in graph.nodes()]
    
    elif direction == 'out':
        reaches = [(len(nx.single_source_shortest_path(graph,n,cutoff=m))-1)/(nr_nodes-1) for n in graph.nodes()]
        
    else:
        print('Direction format is not correct.')
    
    return dict(zip(graph.nodes(),reaches))

def global_reaching_centrality(graph,m=None,direction=None):
    '''
    The network must be connected.
    The global reaching centrality (GRC) with m cutoff,
    and the options for used links (in/out/both)
    
    
    Parameters:
    ----------
    graph: networkx object, must be connected
    
    m : cutoff after n step distance
    
    direction: (None|"in"|"out") A node could reach another through in- or out-edge,
                or both of them, if the network is undirected.
    
    
    
    Returns:
    -------
    The sum of the average difference of LRC values from the maximum LRC value.
    '''
#    if not nx.is_connected(graph):# it works only on undirected graphs
#        print('Graph must be connected.')
#        return {}


    nr_nodes=graph.number_of_nodes()
    LRC_s = m_reaching_centrality(graph=graph,m=m,direction=direction)
    reaches = list(LRC_s.values())

    MAX_lrc = np.max(reaches)
    
    return sum([MAX_lrc-item for item in reaches])/(nr_nodes-1)


def hierarchy_lvls_of_node_LRCs(node_LRCs,STD_coef):
    '''
    This funtion will sort the nodes in hierarchy levels based on their local reaching centrality values(LRC).
    The standard deviation of LRC value in one hierarchy level must be less than the standard deviation of all nodes times the STD_coef.
    With this STD_coef we can tune size of the levels, if STD_coef is too big, every nodes are in the same level.
    If it's too small, we get one level for every different LRC value.
    Of course this method works with any nueric value a node can have.
    
    Parameters:
    ----------
    node_LRCs: dict of LRC values, keys are the node names, values are the LRC values.
    
    STD_coef:  The standard deviation of LRC value in one hierarchy level must be less than the standard deviation of all nodes times the STD_coef.
               With this STD_coef we can tune size of the levels, if STD_coef is too big, every nodes are in the same level.
               If it's too small, we get one level for every different LRC value.
    
    Returns:
    -------
    lvl_names,lvl_LRC_s
    lvl_names : list of lists of nodenames that are in the same hierarchy level.
    lvl_LRC : list of average LRC values of nodes in the same hierarchy level.
    '''
    #sort dict by LRC_s
    node_LRCs = [[k,v] for k, v in sorted(node_LRCs.items(), key=lambda item: item[1],reverse=True)]
    
    lvl_names = []
    lvl_LRC_s = []
    
    #standard deviation of LRC values:
    std_all_LRCs=np.std([n[1] for n in node_LRCs])

    i=0
    tmp_node_LRCs = []

    while i<len(node_LRCs):
        tmp_node_LRCs.append(node_LRCs[i])
        i+=1
        while i<len(node_LRCs) and np.std([n[1] for n in tmp_node_LRCs])<STD_coef*std_all_LRCs:
            tmp_node_LRCs.append(node_LRCs[i])
            i+=1
        if np.std([n[1] for n in tmp_node_LRCs])>STD_coef*std_all_LRCs:
            del tmp_node_LRCs[-1]
            i-=1
            
        lvl_names.append([n[0] for n in tmp_node_LRCs])
        lvl_LRC_s.append(np.average([n[1] for n in tmp_node_LRCs]))

        tmp_node_LRCs.clear()
        
    return lvl_names,lvl_LRC_s

def get_coordinates_of_lvls_avgLRCs(lvl_names,lvl_avg_LRC):
    '''
    This funtion returns coordinates for a hierarchy levels plot.
    The y coordinate is the average LRC value of the level.
    The x coordinate is element of [0,1] interval, centralized, so the levels look like a christmas tree.
    
    Parameters:
    ----------
    lvl_names : list of lists of nodenames that are in the same hierarchy level.

    lvl_LRC : list of average LRC values of nodes in the same hierarchy level.
    
    Returns:
    -------
    list_of_coordinates: list of coordinate pairs for every node.
    '''
    list_of_coordinates=[]
    maximum_len=max([len(lvl) for lvl in lvl_names])
    for i in range(len(lvl_names)):
        for j in range(len(lvl_names[i])):
            
            list_of_coordinates.append([(j-len(lvl_names[i])/2)/maximum_len+0.5,lvl_avg_LRC[i]])
            
    return list_of_coordinates
























