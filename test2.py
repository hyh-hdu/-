import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
# 指标计算可视化

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


centrality_degree = dict(G.degree(weight='weight'))

centrality_betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True)

centrality_closeness = nx.closeness_centrality(G, distance='weight')

centrality_eigenvector = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)

df_centrality = pd.DataFrame({
    'Node': Nodes,
    'Degree (Weighted)': [centrality_degree.get(n, 0) for n in Nodes],
    'Betweenness': [centrality_betweenness.get(n, 0) for n in Nodes],
    'Closeness': [centrality_closeness.get(n, 0) for n in Nodes],
    'Eigenvector': [centrality_eigenvector.get(n, 0) for n in Nodes]
})

print("--- Core Centrality Measure Calculation Results ---")
print(df_centrality.to_string(index=False, float_format="%.4f"))
print("---------------------------------------------------")



def normalize_size(scores_dict, min_size=200, max_size=2000):
    scores = list(scores_dict.values())
    min_val = min(scores)
    max_val = max(scores)
    if min_val == max_val:
        return [min_size] * len(scores)
    return [((score - min_val) / (max_val - min_val)) * (max_size - min_size) + min_size for score in scores]


def normalize_colors(scores_dict, cmap_name='viridis'):
    scores = list(scores_dict.values())
    min_val = min(scores)
    max_val = max(scores)
    cmap = plt.get_cmap(cmap_name)
    if min_val == max_val:
        return [cmap(0.5)] * len(scores)

    normalized_scores = [(score - min_val) / (max_val - min_val) for score in scores]
    return [cmap(score) for score in normalized_scores]


# Setup plot
pos = nx.spring_layout(G, k=0.4, iterations=100, seed=42)
plt.figure(figsize=(15, 12), facecolor='white')

plot_info = [
    ('Degree Centrality (Activity/Strength)', centrality_degree, 'Reds'),
    ('Betweenness Centrality (Control/Brokerage)', centrality_betweenness, 'Greens'),
    ('Closeness Centrality (Efficiency)', centrality_closeness, 'Blues'),
    ('Eigenvector Centrality (Influence)', centrality_eigenvector, 'Purples')
]

for i, (title, data_dict, cmap_name) in enumerate(plot_info):
    ax = plt.subplot(2, 2, i + 1)

    node_size = normalize_size(data_dict, 400, 2500)
    node_color = normalize_colors(data_dict, cmap_name)


    nx.draw_networkx_edges(G, pos, ax=ax, width=1.0, alpha=0.3, edge_color='#AAAAAA')


    nodes = nx.draw_networkx_nodes(G, pos, ax=ax,
                                   node_color=node_color,
                                   node_size=node_size,
                                   edgecolors='k',
                                   linewidths=0.5)


    nx.draw_networkx_labels(G, pos, ax=ax,
                            font_size=10,
                            font_color='k')

    ax.set_title(title, fontsize=16, fontweight='bold', color='#333333')
    ax.axis('off')

plt.suptitle('Core Centrality Measures Visualization', fontsize=20, fontweight='bold', y=1.0)


output_filename_centrality = 'SNA_Centrality_Measures_EN.pdf'
plt.tight_layout(rect=[0, 0, 1, 0.98])  # Adjust layout for suptitle
plt.savefig(output_filename_centrality, format='pdf', bbox_inches='tight', dpi=300)

print(f"Centrality measures chart saved to high-quality file: {output_filename_centrality}")
plt.show()