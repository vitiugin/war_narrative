import pandas as pd
import networkx as nx

import community as community_louvain

lang = 'uk' # en, ru, uk

# loading all tweets
data_file = pd.read_csv('tweets.csv', usecols=['in_reply_to_screen_name', 'user', 'lang'])

# shape of the loaded dataframe
print('DataFrame shape:', data_file.shape)

# choose tweets in requested language
lang_df = data_file[data_file['lang'] == lang]

# Creating dataframe with future edge weights
new_df = lang_df.groupby(by=['user', 'in_reply_to_screen_name'],
                          as_index=False).size()

# Renaming of columns for exporting in gephi format
new_df = new_df.rename(columns={"user": "Source", 
                                "in_reply_to_screen_name": "Target",
                                "size": "Weight"})

# Filtering edges (wi'll use only edges with weight > 1)
new_df = new_df[new_df.Weight > 1]

# Creating of graph
G = nx.Graph()

# Filling the graph with data from dataframe
G = nx.from_pandas_edgelist(new_df, 'Source', 'Target', edge_attr=True)

# Removing selfloops (user retweets themself)
G.remove_edges_from(list(nx.selfloop_edges(G)))

# Giant Connected Component
Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])

# return partition as a dict
partition = community_louvain.best_partition(G0, weight='Weight', random_state=123)

# Calculation of modularity of returned partition
modularity_value = community_louvain.modularity(partition, G0, weight='Weight')

print('Modularity:', modularity_value)

# Set partition attribute to graph nodes
nx.set_node_attributes(G0, partition, name="Community")

nx.write_gml(G0, lang + "_G0.gml")