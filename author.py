import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys


def analyze_author_network(file_name):
    try:
        df_edges = pd.read_excel(file_name)
        print("数据预览:")
        print(df_edges.head().to_markdown(index=False, numalign="left", stralign="left"))
    except Exception as e:
        print(f"加载文件 {file_name} 时出错: {e}")
        return

    # 建立模型
    G = nx.from_pandas_edgelist(df_edges, 'Source', 'Target', edge_attr=['Weight'], create_using=nx.Graph())
    print("\n--- 网络模型构建完成 ---")

    # 计算指标
    print("\n全局网络指标")

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    num_components = nx.number_connected_components(G)

    print(f"总节点数 (作者): {num_nodes}")
    print(f"总边数 (合作关系): {num_edges}")
    print(f"网络密度: {density:.6f}")
    print(f"连通分量数 (独立群组): {num_components}")

    try:
        avg_clustering = nx.average_clustering(G)
        print(f"平均聚类系数: {avg_clustering:.6f}")
    except Exception as e:
        print(f"无法计算平均聚类系数: {e}")

    # 4. 计算节点层面指标
    print("\n节点层面指标")

    # 度中心性
    degree_centrality = nx.degree_centrality(G)
    df_degree = pd.DataFrame(degree_centrality.items(), columns=['Author', 'DegreeCentrality']).sort_values(
        'DegreeCentrality', ascending=False)
    print("\n度中心性 (连接最多的作者) 前十名:")
    print(df_degree.head(10).to_markdown(index=False, numalign="left", stralign="left"))

    # 中介中心性
    try:
        betweenness_centrality = nx.betweenness_centrality(G, weight='Weight', normalized=True)
        df_betweenness = pd.DataFrame(betweenness_centrality.items(),
                                      columns=['Author', 'BetweennessCentrality']).sort_values('BetweennessCentrality',
                                                                                               ascending=False)
        print("\n中介中心性 (关键桥梁) 前十名:")
        print(df_betweenness.head(10).to_markdown(index=False, numalign="left", stralign="left"))
    except Exception as e:
        print(f"计算中介中心性时出错: {e}")

    # 特征向量中心性
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G, weight='Weight', max_iter=1000)
        df_eigenvector = pd.DataFrame(eigenvector_centrality.items(),
                                      columns=['Author', 'EigenvectorCentrality']).sort_values('EigenvectorCentrality',
                                                                                               ascending=False)
        print("\n特征向量中心性 (最具影响力的连接) 前十名:")
        print(df_eigenvector.head(10).to_markdown(index=False, numalign="left", stralign="left"))
    except Exception as e:
        print(f"计算特征向量中心性时出错: {e}")

    # 可视化
    if num_components > 1:
        largest_cc = max(nx.connected_components(G), key=len)
        G_main = G.subgraph(largest_cc).copy()
    else:
        G_main = G.copy()



    fig, ax = plt.subplots(figsize=(20, 20))
    try:
        pos = nx.kamada_kawai_layout(G_main)
    except Exception as e:
        pos = nx.spring_layout(G_main, seed=42)
    degrees_main = dict(G_main.degree())
    node_sizes = [degrees_main[n] * 20 + 10 for n in G_main.nodes()]
    betweenness_main = nx.betweenness_centrality(G_main, normalized=True)
    node_colors = [betweenness_main[n] for n in G_main.nodes()]
    nodes = nx.draw_networkx_nodes(
        G_main,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.viridis,
        alpha=0.8,
        ax=ax
    )

    nx.draw_networkx_edges(
        G_main,
        pos,
        edge_color='grey',
        alpha=0.15,
        ax=ax
    )

    ax.axis('off')

    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm._A = []

    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01)

    cbar.set_label('Node Betweenness Centrality', rotation=270, labelpad=25, fontsize=15)

    output_image_file = "author.png"
    fig.savefig(output_image_file, dpi=300, bbox_inches='tight')

    print(f"\n可视化已保存至 '{output_image_file}'。")


# --- 主程序执行 ---
# 如果文件名不同，请替换为您的预处理文件名
input_file = "preprocess.xlsx"
analyze_author_network(input_file)