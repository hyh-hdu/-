import networkx as nx
import matplotlib.pyplot as plt
# 网络可视化
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

Nodes = list(range(1, 13))
EdgeList = [
    (1, 2, 3), (1, 3, 4), (2, 3, 5), (2, 4, 1),
    (3, 4, 2), (3, 1, 3), (4, 5, 4), (4, 6, 5),
    (5, 6, 1), (5, 7, 2), (6, 7, 3), (6, 8, 4),
    (7, 8, 5), (7, 9, 1), (8, 9, 2), (8, 10, 3),
    (9, 10, 4), (9, 11, 5), (10, 11, 1), (10, 12, 2),
    (11, 12, 3), (11, 1, 4), (12, 2, 5)
]
G = nx.Graph()
G.add_nodes_from(Nodes)
for u, v, w in EdgeList:
    G.add_edge(u, v, weight=w)

ColorBlue = '#377EB8'
ColorOrange = '#FF9933'
ColorGreen = '#4DAF4A'
ColorRed = '#E41A1C'
ColorGray = '#888888'

CommunityA = list(range(1, 7))
CommunityB = list(range(7, 13))
ClusteringNodes = [1, 2, 3]
P = nx.dijkstra_path(G, source=1, target=10, weight='weight')
D = nx.dijkstra_path_length(G, source=1, target=10, weight='weight')


node_colors = {}
for node in G.nodes():
    node_colors[node] = ColorBlue if node in CommunityA else ColorOrange
    if node in ClusteringNodes:
        node_colors[node] = ColorGreen
    if node in P:
        node_colors[node] = ColorRed

node_degrees = dict(G.degree())
node_size = [v * 300 + 400 for v in node_degrees.values()]
edge_widths = [d['weight'] * 0.5 for (u, v, d) in G.edges(data=True)]
edge_colors = [ColorGray] * len(G.edges())
edge_labels = nx.get_edge_attributes(G, 'weight')

path_edges = list(zip(P[:-1], P[1:]))
for i, (u, v, d) in enumerate(G.edges(data=True)):
    if (u, v) in path_edges or (v, u) in path_edges:
        edge_colors[i] = ColorRed
        edge_widths[i] = d['weight'] * 2.0

plt.figure(figsize=(12, 9), facecolor='white')

pos = nx.spring_layout(G, k=0.4, iterations=100, seed=42)

nx.draw_networkx_nodes(G, pos,
                       node_color=list(node_colors.values()),
                       node_size=node_size,
                       edgecolors='k',
                       linewidths=0.5)

nx.draw_networkx_edges(G, pos,
                       width=edge_widths,
                       alpha=0.8,
                       edge_color=edge_colors)

nx.draw_networkx_labels(G, pos,
                        font_size=12,
                        font_color='w',
                        font_weight='bold')

nx.draw_networkx_edge_labels(G, pos,
                             edge_labels=edge_labels,
                             font_color=ColorGray,
                             font_size=9,
                             bbox={'facecolor':'white', 'alpha':0.8, 'edgecolor':'none'},
                             label_pos=0.5)


plt.title(f'Social Network Structure Features', fontsize=18, fontweight='bold', pad=15)
plt.figtext(0.5, 0.05, 'Visualization of Nodes, Edges, Weights, Communities, Clusters, and Paths', ha='center', fontsize=12)

# 6. Custom Legend (English)
legend_handles = []

legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label='Community A (Blue)',
                                 markerfacecolor=ColorBlue, markersize=10, markeredgecolor='k'))
legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label='Community B (Orange)',
                                 markerfacecolor=ColorOrange, markersize=10, markeredgecolor='k'))
legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', label='Cluster (Green)',
                                 markerfacecolor=ColorGreen, markersize=10, markeredgecolor='k'))
legend_handles.append(plt.Line2D([0], [0], color=ColorRed, linestyle='-', linewidth=3,
                                 label=f'Shortest Path (D={D}, Red)'))

plt.legend(handles=legend_handles, loc='lower left', bbox_to_anchor=(0.0, 0.1),
           frameon=True,
           fontsize=10, title='Network Structure Elements', title_fontsize=11) # 🌟 英文图例标题 🌟

plt.axis('off')


output_filename = 'SNA_Structure_Academic_EN.pdf'
plt.savefig(output_filename, format='pdf', bbox_inches='tight', dpi=300)

print(f"Chart saved to high-quality file: {output_filename}") # 🌟 英文打印信息 🌟
plt.show()