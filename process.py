import pandas as pd
import itertools
import re
file_name = "管理科学.xlsx "
try:
    df = pd.read_excel(file_name)

    #处理作者数据
    author_series = df['Author-作者'].dropna()
    edge_list = []
    separator = ';'

    for author_string in author_series:
        authors = author_string.split(separator)
        cleaned_authors = [name.strip() for name in authors if name.strip()]
        if len(cleaned_authors) > 1:
            # 获取所有唯一的两两组合
            pairs = list(itertools.combinations(cleaned_authors, 2))
            edge_list.extend(pairs)
    if not edge_list:
        df_weighted_edges = pd.DataFrame(columns=['Source', 'Target', 'Weight'])
    else:
        df_edges = pd.DataFrame(edge_list, columns=['Author1', 'Author2'])
        # 标准化和聚合
        standardized_pairs = df_edges.apply(lambda x: tuple(sorted(x)), axis=1)
        df_standardized = pd.DataFrame(standardized_pairs.tolist(), columns=['Source', 'Target'])
        df_weighted_edges = df_standardized.groupby(['Source', 'Target']).size().reset_index(name='Weight')
        # 按次数降序排列
        df_weighted_edges = df_weighted_edges.sort_values(by='Weight', ascending=False)
        print("合作最紧密的前10对作者:")
        print(df_weighted_edges.head(10))
    output_filename = "preprocess.xlsx"
    df_weighted_edges.to_excel(output_filename, index=False)

except FileNotFoundError:
    print(f"错误：文件 '{file_name}' 未找到。")
except Exception as e:
    print(f"处理过程中发生错误: {e}")