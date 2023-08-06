r"""This module contains 3 functions
   <rank_list> attributes to each node a rank according to its death date
   <same_rank_subgraph> matches the nodes of the subgraph, i.e the dates, with the corresponding node of the main graph, i.e. the transmitters
   <a_timeline> creates the a subgraph with the dates
"""
import pandas as pd
from graphviz import Digraph


def rank_list(date:str, rank:int, df:pd.DataFrame.astype) -> list:
    """
    Return a list with the date and all the node 
    ids that should be placed at the same rank.
    """
    same_rank = df[df.Ranking==rank].Transmitters.values
    l = [date]
    if len(same_rank) == 0:
        same_rank = ['placeholder']
    l.extend(same_rank)

    return l


def same_rank_subgraph(G:Digraph, rank_lst:list) -> None:
    """ Return subgraph of nodes from same-rank ids. """
    with G.subgraph() as s:
        s.attr(rank='same')
        for node_id in rank_lst:
            if node_id != 'placeholder':
                s.node(node_id)


def a_timeline(G:Digraph, minimum:int, maximum:int, step:int, n_attr:dict, e_attr:dict) -> None:
    """
    creates a timeline in the form of a subgraph
    G = the original graph
    s = G's subgraph
    minimum = start of the timeline
    maximum = end of the timeline
    step = years' slice
    n_attr = dict with the attribute of the subgraph's nodes
    e_attr = dict with the attribute of the subgraph's edges
    """
    with G.subgraph(name='cluster') as s:
        s.attr(color='white', K='0.3')
        for j in range(minimum, maximum, step):
            s.node_attr.update(**n_attr)  
            s.edge(str(j), str(j+step), **e_attr)