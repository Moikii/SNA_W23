import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm


def filter_users(df: pd.DataFrame, channels: list, min_articles=5):
    df = df[df['ArticleChannel'].isin(channels)]

    # Get unique articles per user
    articles_per_user = df.groupby('ID_CommunityIdentity')[
        'ID_Article'].agg(set)

    articles_per_user = articles_per_user[articles_per_user.apply(
        len) > min_articles].apply(list)
    selected_users = articles_per_user.index.to_list()
    df = df[df['ID_CommunityIdentity'].isin(selected_users)]

    return df, articles_per_user, selected_users


def most_common_category_per_user(df: pd.DataFrame):
    df_category_count = df.groupby(['ID_CommunityIdentity', 'ArticleChannel'])[
        'ID_Article'].count().unstack()
    df_category_count = df_category_count.fillna(0)
    df_category_count['most_common'] = df_category_count.idxmax(axis=1)
    return df_category_count


def build_graph(selected_users, edge_weights, threshold):
    graph = nx.Graph()

    for i in range(len(selected_users)):
        for j in range(i+1, len(selected_users)):
            if edge_weights[i, j] > threshold:
                graph.add_edge(
                    selected_users[i],
                    selected_users[j],
                    weight=edge_weights[i, j])
    return graph


def load_data():
    file_path = '../data/Postings_01052019_15052019.csv'
    file_path2 = '../data/Postings_16052019_31052019.csv'

    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    df2 = pd.read_csv(file_path2, sep=';', encoding='utf-8')

    df = pd.concat([df, df2])
    return df


def iou(selected_users, articles_per_user):
    edge_weights = np.zeros((len(selected_users), len(selected_users)))

    for i, user1 in enumerate(tqdm(selected_users)):
        articles_user1 = set(articles_per_user[user1])
        for j, user2 in enumerate(selected_users[i:]):
            j = j+i
            if i != j:
                articles_user2 = set(articles_per_user[user2])
                common_articles = set(articles_user1).intersection(
                    set(articles_user2))
                union_artciels = set(articles_user1).union(set(articles_user2))
                edge_weights[i, j] = len(common_articles)/len(union_artciels)

    return edge_weights


def iom(selected_users, articles_per_user):
    edge_weights = np.zeros((len(selected_users), len(selected_users)))

    for i, user1 in enumerate(tqdm(selected_users)):
        articles_user1 = set(articles_per_user[user1])
        for j, user2 in enumerate(selected_users[i:]):
            j = j+i
            if i != j:
                articles_user2 = set(articles_per_user[user2])
                common_articles = set(articles_user1).intersection(
                    set(articles_user2))
                min_artciels = min(len(articles_user1), len(articles_user2))
                edge_weights[i, j] = len(common_articles)/min_artciels

    return edge_weights



def comments_in_category_per_community(communities, filtered_df, percentage = False, weight_by_category_distribution = False):
    tmp = filtered_df.groupby(['ID_CommunityIdentity','ArticleChannel'])['ID_CommunityIdentity'].size().reset_index(name='counts')
    tmp = tmp.pivot(index = 'ID_CommunityIdentity', columns='ArticleChannel', values='counts')
    tmp = tmp.fillna(0)

    categories = filtered_df['ArticleChannel'].unique()
    total_category_comments_percentage = filtered_df['ArticleChannel'].value_counts().div(len(filtered_df))


    community_dfs = [tmp.loc[tmp.index.isin(community)] for community in communities]
    community_comment_count_dfs = [community_df.sum() for community_df in community_dfs]
    number_of_comments = [df.sum() for df in community_comment_count_dfs]

    community_comment_count_dict = dict()
    for category in categories:
            for df in community_comment_count_dfs:
                if category not in community_comment_count_dict.keys():
                    community_comment_count_dict[category]= list()
                community_comment_count_dict[category].append(df[category])

    if weight_by_category_distribution:
        for category in categories:
                community_comment_count_dict[category] /= total_category_comments_percentage[category]

        for i, community in enumerate(communities):
            total = sum([community_comment_count_dict[category][i] for category in categories])
            for category in categories:
                community_comment_count_dict[category][i] /= total
                community_comment_count_dict[category][i] *= number_of_comments[i]


    if percentage:
        for i, community in enumerate(communities):
            total = sum([community_comment_count_dict[category][i] for category in categories])
            for category in categories:
                community_comment_count_dict[category][i] /=total
 
    community_comment_distribution_df = pd.DataFrame(community_comment_count_dict)
    return community_comment_distribution_df