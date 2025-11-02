import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
# 结构洞可视化

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

G = nx.Graph()

marketing_cluster = ['A', 'B', 'C']
engineering_cluster = ['D', 'E', 'F']
sales_cluster = ['G', 'H', 'I']
broker_node = 'M'

G.add_edges_from([('A', 'B'), ('B', 'C'), ('A', 'C')])
G.add_edges_from([('D', 'E'), ('E', 'F'), ('D', 'F')])
G.add_edges_from([('G', 'H'), ('H', 'I'), ('G', 'I')])

G.add_edges_from([
    (broker_node, 'B'), # M connects to Marketing
    (broker_node, 'E'), # M connects to Engineering
    (broker_node, 'H')  # M connects to Sales
])

pos = {
    # Marketing Cluster (Left)
    'A': [0, 1], 'B': [0, 0], 'C': [0, -1],
    # Engineering Cluster (Right)
    'D': [4, 1], 'E': [4, 0], 'F': [4, -1],
    # Sales Cluster (Bottom)
    'G': [1.5, -2], 'H': [2, -3], 'I': [2.5, -2],
    # Broker 'M' (Center)
    broker_node: [2, 0]
}

node_colors = []
node_sizes = []
for node in G.nodes():
    if node == broker_node:
        node_colors.append('#E41A1C')
        node_sizes.append(2500)
    elif node in marketing_cluster:
        node_colors.append('#377EB8')
        node_sizes.append(1000)
    elif node in engineering_cluster:
        node_colors.append('#4DAF4A')
        node_sizes.append(1000)
    else: # Sales
        node_colors.append('#FF9933')
        node_sizes.append(1000)


betweenness = nx.betweenness_centrality(G, normalized=True)

print("--- Betweenness Centrality Scores ---")
# Print sorted scores to show M is on top
sorted_betweenness = sorted(betweenness.items(), key=lambda item: item[1], reverse=True)
for node, score in sorted_betweenness:
    print(f"{node}: {score:.4f}")
print("-------------------------------------")


plt.figure(figsize=(10, 8), facecolor='white')
nx.draw_networkx(
    G,
    pos=pos,
    with_labels=True,
    node_color=node_colors,
    node_size=node_sizes,
    font_color='k',
    font_weight='bold',
    font_family='Times New Roman',
    edge_color='#AAAAAA'
)
plt.title('Visualizing Structural Holes', fontsize=18, fontweight='bold')
plt.text(2, 0.5, 'Manager "M"\n(The Broker)', ha='center', fontsize=12, style='italic', color='#E41A1C')
plt.text(0, 1.5, 'Marketing Cluster', ha='center', fontsize=12, color='#377EB8')
plt.text(4, 1.5, 'Engineering Cluster', ha='center', fontsize=12, color='#4DAF4A')
plt.text(2, -1.5, 'Sales Cluster', ha='center', fontsize=12, color='#FF9933')
plt.axis('off')

plt.savefig('SNA_Structural_Holes.pdf', format='pdf', bbox_inches='tight', dpi=300)
print("\nVisualization saved to SNA_Structural_Holes.pdf")
plt.show()