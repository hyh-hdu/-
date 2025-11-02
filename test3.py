import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
# 例题
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

G = nx.Graph()
nodes = ['Alice', 'Bob', 'Charlie', 'David', 'Emily', 'Frank']
edges = [
    ('Alice', 'Bob'), ('Alice', 'Charlie'), ('Bob', 'Charlie'),
    ('Charlie', 'David'), ('David', 'Emily'), ('Emily', 'Frank')
]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

centrality_degree = nx.degree_centrality(G)
centrality_betweenness = nx.betweenness_centrality(G, normalized=True)
centrality_closeness = nx.closeness_centrality(G)
centrality_eigenvector = nx.eigenvector_centrality(G, max_iter=1000)

df_centrality = pd.DataFrame({
    'Node': nodes,
    'Degree': [centrality_degree.get(n, 0) for n in nodes],
    'Betweenness': [centrality_betweenness.get(n, 0) for n in nodes],
    'Closeness': [centrality_closeness.get(n, 0) for n in nodes],
    'Eigenvector': [centrality_eigenvector.get(n, 0) for n in nodes]
})

print("--- Project Team Centrality Scores ---")
print(df_centrality.to_string(index=False, float_format="%.4f"))
print("----------------------------------------")


ans_degree = df_centrality.loc[df_centrality['Degree'].idxmax()]['Node']
ans_betweenness = df_centrality.loc[df_centrality['Betweenness'].idxmax()]['Node']
ans_closeness = df_centrality.loc[df_centrality['Closeness'].idxmax()]['Node']
ans_eigenvector = df_centrality.loc[df_centrality['Eigenvector'].idxmax()]['Node']

print("\n--- Exercise Answers ---")
print(f"1. Most Active (Degree):       {ans_degree} (Score: {centrality_degree[ans_degree]:.4f})")
print(f"2. Most Critical Bridge (Betweenness): {ans_betweenness} (Score: {centrality_betweenness[ans_betweenness]:.4f})")
print(f"3. Most Efficient (Closeness): {ans_closeness} (Score: {centrality_closeness[ans_closeness]:.4f})")
print(f"4. Most Influential (Eigenvector): {ans_eigenvector} (Score: {centrality_eigenvector[ans_eigenvector]:.4f})")

plt.figure(figsize=(10, 7), facecolor='white')
pos = nx.spring_layout(G, seed=42)

node_sizes = [v * 3000 + 500 for v in centrality_degree.values()]
node_colors = list(centrality_betweenness.values())
cmap = plt.get_cmap('Oranges')

nx.draw_networkx(G, pos,
                 with_labels=True,
                 node_color=node_colors,
                 node_size=node_sizes,
                 font_size=10,
                 font_weight='bold',
                 font_family='Times New Roman',
                 cmap=cmap,
                 edge_color='#AAAAAA')

sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label('Betweenness Centrality', rotation=270, labelpad=15)

plt.title('Project Team Communication Network', fontsize=16, fontweight='bold')
plt.axis('off')

plt.savefig('SNA_Exercise_Solution.pdf', format='pdf', bbox_inches='tight', dpi=300)
print("\nVisualization saved to SNA_Exercise_Solution.pdf")
plt.show()