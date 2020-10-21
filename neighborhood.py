import networkx as nx
import numpy as np


def neighbors_at_n_step(G, node,cutoff=1 ,direction=None):
    '''
    Returns the nodes at a given range, from a central node.


    Parameters
    ----------
    G : networkx object

    node : name of node in the central

    cutoff : distance from the central node, in default it's 1

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.


    Returns:
    ------
    A list of node names, which are at given distance from the central node.

    '''
    if direction == None:
        G = G.copy()
        G = G.to_undirected()
    elif direction == 'in':
        G = G.copy()
        G = G.reverse()
            
    elif direction == 'out':
        pass
    else:
        'Wrong direction stat. Expected bool.'
    
    path_lengths = nx.single_source_dijkstra_path_length(G,
                                                         source=node,
                                                         cutoff=cutoff)
    
    return [node for node,length in path_lengths.items() if length == cutoff]




def neighbors_within_n_step(G, node,cutoff=1,direction=None):
    '''
    Returns the nodes within a given range, from a central node.
    Incluede the central node too.


    Parameters
    ----------
    G : networkx object

    node : name of node in the central

    cutoff : distance from the central node, in default it's 1

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.


    Returns:
    ------
    A list of node names, which are within a given distance from the central node.

    '''
    if direction == None:
        G = G.copy()
        G = G.to_undirected()
    elif direction == 'in':
        G = G.copy()
        G = G.reverse()
            
    elif direction == 'out':
        pass
    else:
        'Wrong direction stat. Expected bool.'
    
    path_lengths = nx.single_source_dijkstra_path_length(G,source=node,cutoff=cutoff)
    
    return [node for node,length in path_lengths.items()]



def subgraph_within_n_step(G, node,cutoff=1,direction=None,center=True):
    '''
    Returns the subgraphs of nodes within a given range, from a central node.
    
    Parameters
    ----------
    G : networkx object

    node : name of node in the central

    cutoff : distance from the central node, in default it's 1

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.
    
    center : bool, exclueding the central node in the subgraph. Default is True

    Returns:
    ------
    A subgraph (networkx object), its nodes are within a given distance from the central node. 

    '''
    if direction == None:
        G = G.copy()
        G = G.to_undirected()
    elif direction == 'in':
        G = G.copy()
        G = G.reverse()
        return nx.ego_graph(G=G,n=node,radius=cutoff,center=center).reverse()
    
    elif direction == 'out':
        pass
    else:
        'Wrong direction stat. Expected bool.'
    
    return nx.ego_graph(G=G,n=node,radius=cutoff,center=center)





def subgraphs_of_nodes_within_n_steps(G,nodes,cutoff=1,direction=None,center=True):
    '''
    Returns the composed subgraphs of nodes, that are within a given range from given central nodes.
    
    Parameters
    ----------
    G : networkx object, must be MultiGraph 

    nodes : name of nodes in the centrals

    cutoff : distance from the central nodes, in default it's 1

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.
    
    center : bool, exclueding the central node in the subgraph. Default is True

    Returns:
    ------
    A MultiGraph (networkx object)

    '''
    graphs = [] #list of subgraphs
    graph_ret = nx.MultiDiGraph()
    for n in nodes:
        tmp_graph = subgraph_within_n_step(G,
                                           node=n,
                                           cutoff=cutoff,
                                           direction=direction,
                                           center=center)
        graphs.append(tmp_graph)
    
    for g in graphs:
        graph_ret = nx.compose(graph_ret,g)
    
    return graph_ret



def subgraphs_around_nodes_within_cutoff(G,nodelist,cutoff=1,direction=None):
    '''
    Returns a list of subgraphs, that are composed from the seeds in the nodelist.
    Each graph is the subgraph around one of the node in the nodelist.
    
    It uses the neighbors_within_n_step function.

    Parameters
    ----------
    G : networkx object 

    nodelist : name of nodes in the centrals

    cutoff : distance from the central nodes, in default it's 1

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.

    Returns:
    ------
    graphs : A list of networkx objects.

    '''
    environment_of_nodes = []
    graphs = [] 
    
    for i in range(len(nodelist)):
        environment_of_nodes.append(neighbors_within_n_step(G, nodelist[i],cutoff=cutoff,direction=direction))
        
        graphs.append(G.subgraph(environment_of_nodes[i]))
        
    return graphs





def neighbors_first_order(G,basenode,direction = None):
    '''
    Returns the first order neighbors of the basenode. G must be a directed graph.
    From the first order neighbors the basenode must be reachable with directed edges. 
    The neighbors can point at each other, but cannot point at any node, which cannot reach the basenode.
    
    Parameters:
    ----------
    G : networkx object 

    basenode : name of a node in the graph

    direction: None or string
        
            The default is undirected.

            If direction = in : We use the number of incoming degrees, as degree.

            If direction = out : We use the number of outgoing degrees, as degree.

    Returns:
    ------
    star_nodes : A list of the first order neighbors and the basenode.

    '''

    if G.is_directed():
        pass
    else:
        print('Graph must be directed.')
        return []

    #copy:
    G = G.copy()
    
    # remove out edges of basenode
    G.remove_edges_from(list(G.edges(basenode)))
    
    
    star_nodes = neighbors_within_n_step(G,
                                         node=basenode,
                                         cutoff=np.infty,
                                         direction=direction)
    
    # filter out: nodes with neighbor, that can't reach basenode, only through out edges:
    nodes_reach_basenode = list(nx.single_target_shortest_path(G,basenode,cutoff=None).keys())
    
    for node in star_nodes:
        
        neighs = list(G.neighbors(node))#by out edges
        
        for n in neighs:
            # if basenode can't be reached from node's outneighbors
            if n not in nodes_reach_basenode:
                #remove edges of node:
                G.remove_edges_from(list(G.out_edges(node)))
                G.remove_edges_from(list(G.in_edges(node)))
        #update reachable nodes
        nodes_reach_basenode = list(nx.single_target_shortest_path(G,basenode,cutoff=None).keys())
    
    # only valid nodes remained:
    star_nodes = neighbors_within_n_step(G,
                                         node=basenode,
                                         cutoff=np.infty,
                                         direction=direction)
    
    return star_nodes


def nr_components_linked_by_element(G,element, components):
    '''
    Returns the number of components, that have nodes with incoming edges from  the element node
    
    Parameters:
    ----------
    G : networkx object 
    
    element : node of G

    components : list of networkx graphs

    Returns:
    ------
    occurrence : the number components, that have nodes with incoming edges from  the element node
    '''
    occurrence = 0
    cited_nodes = list(nx.neighbors(G,element))
    
    
    for c in components:
        tmp = 0
        for neigh in cited_nodes:
            if neigh in c:
                tmp+=1
        if tmp > 0:
            occurrence +=1
    
    return occurrence


def env_of_nodes_first_order(G,basic_nodes):
    '''
    Returns the first order components of the basic_nodes, and the binding nodes between them.
    
    It uses the nr_components_linked_by_element function.

    Parameters:
    ----------
    G : networkx object 

    basic_nodes : list of node names

    Returns:
    ------
    component_nodes : list of nodes in a component, around a basic_nodes, arranged in a list which follows the order of basic_nodes
    
    binding_nodes: the nodes that connects the components.
    '''



    G = G.copy()
    
    binding_nodes = []
    component_nodes = []
    
    #iterate:
    for n in basic_nodes:
        c = neighbors_first_order(G=G,basenode=n,direction='in')
        component_nodes.append(c)
    
    # binding nodes:
    for n in G.nodes():
        occur = nr_components_linked_by_element(G=G,element=n,components=component_nodes)
        if occur >=2:
            binding_nodes.append(n)
    
#     #add basic node back its component NEM KELL:
#     for i in range(len(basic_nodes)):
#         component_nodes[i].append(basic_nodes[i])
    
    return component_nodes,binding_nodes










