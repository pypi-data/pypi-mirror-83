
from short_text_tagger.edgelist import EdgeList
import graph_tool.all as gt
import pandas as pd
from collections import defaultdict

class NSBM:

    def __init__(self, edgelist: EdgeList, block_level: int = 2):
        # assigning node names to unique integer identifiers
        node_names = edgelist.edgelist[["source","target"]].stack().reset_index(name="node_name")
        unique_node_names = node_names["node_name"].unique()

        # edgelist metadata
        self.node_name_to_node_index = {unique_node_names[i]:i for i in range(len(unique_node_names))}
        self.node_index_to_node_name = {index:name for name,index in self.node_name_to_node_index.items()}
        self.directed = edgelist.directed
        self.edgelist = edgelist.edgelist
        self.edgelist['source_index'] = self.edgelist['source'].apply(lambda name:self.node_name_to_node_index[name])
        self.edgelist['target_index'] = self.edgelist['target'].apply(lambda name:self.node_name_to_node_index[name])

        # graph
        self.g = self.__graph_from_edgelist() 
        
        # NSBM
        self.state = None 
        self.levels = None 
        self.block_level = block_level
        self.block_index_to_vertex_list_dict = defaultdict(list)
        self.block_index_to_block_name_dict = dict()
    


    def __graph_from_edgelist(self) -> gt.Graph:
        """ given edgelist, generate graph-tool graph """ 

        print("Generating graph from edgelist")
        g = gt.Graph(directed = self.directed)

        # initialize edge property
        weight_prop = g.new_edge_property("int")
        g.edge_properties['weight'] = weight_prop

        # initialize node property
        node_name_property = g.new_vertex_property("string")
        g.vertex_properties['node_name'] = node_name_property

        # create graph from edgelist
        g.add_edge_list(edge_list = self.edgelist[['source_index','target_index']].values,
                        eprops = [weight_prop])

        print("Number of vertices: ",len(g.get_vertices()))
        print("Number of edges", len(g.get_edges()))
        
        # add names to each node
        for v in g.vertices():
            node_name_property[v] = self.node_index_to_node_name[int(v)]

        # add weight to each edge 
        for i,e in enumerate(g.edges()):
            weight_prop[e] = self.edgelist['weight'][i]
        print("Graph created")
        return g



    def fit(self) -> None:
        """ given graph, fits NSBM and writes to state and block instance variables """
        
        print("Fitting NSBM")
        state = gt.minimize_nested_blockmodel_dl(self.g, deg_corr=True)
        self.state = state
        self.levels = self.state.get_levels()
        self.block_level = min(self.block_level,len(self.levels))
        self.__get_block_metadata()

        print("NSBM hierarchy summary:")
        state.print_summary()



    def get_block_from_node(self, node:int) -> int:
        """ given node, returns block index at self.block_level """

        block = node
        for i in range(self.block_level):
            block = self.levels[i].get_blocks()[block]
        return block 


    def __get_block_metadata(self) -> None:
        """ writes to block_index_to_vertex_list_dict & block_index_to_block_name_dict"""

        for v in self.g.vertices():
            block = self.get_block_from_node(int(v))
            self.block_index_to_vertex_list_dict[block].append(v)
  
        for block, vertices in self.block_index_to_vertex_list_dict.items():
            highest_degree_names = []
            degree = 0
            for vertex in vertices:
                if vertex.out_degree() > degree:
                    degree = vertex.out_degree()
            for vertex in vertices:
                if vertex.out_degree() == degree:
                    highest_degree_names.append(self.node_index_to_node_name[int(vertex)])
            self.block_index_to_block_name_dict[block] = sorted(highest_degree_names)[0] # always guarantee same node
