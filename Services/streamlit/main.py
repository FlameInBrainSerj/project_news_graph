import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.spatial import ConvexHull
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st
import text_messages
from utils import (
    create_date_series,
    create_news_by_date,
    node_classes_new,
    plot_news,
    spectral_clusterization,
)

s, weekend, working_days = create_date_series()

df_eda = st.cache_data(pd.read_parquet)("Services/streamlit/Data/data_eda_graphs.parquet")
df_comp = st.cache_data(pd.read_parquet)("Services/streamlit/Data/data_comp_graphs.parquet")
df_industry = st.cache_data(pd.read_parquet)("Services/streamlit/Data/data_ind_graphs.parquet")
df_glob = st.cache_data(pd.read_parquet)("Services/streamlit/Data/data_glob_graphs.parquet")


@st.cache_data
def create_df_no_duplicates(df):
    return df.drop_duplicates(subset=["url"])


@st.cache_data
def plot_website_graph(df, title):
    fig = px.histogram(df["website"], x="website")
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_sections_graphs(df):
    sections = df["section"].str.lower().value_counts().head(5)
    fig = px.bar(x=sections.index,
                 y=sections,
                 labels={"x": "Section", "y": "News"})
    fig.update_layout(title="Most common sections")
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_header_graphs(df_without_duplicates):
    fig = px.histogram(
        df_without_duplicates["header"].astype(str).map(len),
        x="header",
        nbins=20,
        labels={"header": "header length"},
    )
    fig.update_layout(
        title="Distribution of header length",
        xaxis_title="Length of text",
        yaxis_title="Number of texts",
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_body_length_distribution(df_without_duplicates):
    colors = {
        "Interfax": "#1b9e77",
        "Ria": "#d95f02",
        "Smart_Lab": "#7570b3",
        "Kommersant": "#e7298a",
    }
    fig = go.Figure()
    for portal in ["Interfax", "Ria", "Smart_Lab", "Kommersant"]:
        fig.add_trace(
            go.Histogram(
                x=df_without_duplicates[
                    df_without_duplicates["website"] == portal
                ].body_length,
                name=portal,
                marker_color=colors[portal],
            )
        )

    # Overlay both histograms
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(maxallowed=10000)
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    fig.update_layout(
        title="Distribution of body length per website",
        xaxis_title="Length of text",
        yaxis_title="Number of texts",
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_body_length_by_date(df_without_duplicates):
    average_len_by_date = (
        df_without_duplicates["body_length"]
        .groupby([df_without_duplicates["datetime"].dt.date])
        .mean()
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(average_len_by_date.index),
            y=list(average_len_by_date.values)
        )
    )
    fig.update_layout(
        title="Average length of selected news per trading day",
        width=1200,
        height=450,
        xaxis=dict(
            title="Date",
            rangeselector=dict(),
            rangeslider=dict(visible=True),
            type="date",
        ),
        yaxis_title="Average length",
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_key_words_graphs(df_without_duplicates):
    tags = []
    for i in df_without_duplicates["key_words"]:
        if np.any(i):
            tags.extend(i)
    tags = pd.DataFrame(tags, columns=["key_words"])
    tags = tags["key_words"].value_counts().head(20)
    fig = px.bar(x=tags.index, y=tags, labels={"x": "Key Words", "y": "News"})
    fig.update_layout(title="Key words histogram")
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_instrument_graph(df, instrument_name):
    companies = df[instrument_name].value_counts().head(20)
    fig = px.bar(
        x=companies.index,
        y=companies,
        labels={"x": instrument_name, "y": "News"}
    )
    fig.update_layout(title=f"News per {instrument_name}")
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_dates_graphs(df_without_duplicates):
    news_by_date = (
        df_without_duplicates["header"]
        .groupby([df_without_duplicates["datetime"].dt.date])
        .count()
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(news_by_date.index),
                             y=list(news_by_date.values)))
    fig.update_layout(
        title="News per market day",
        width=1200,
        height=450,
        xaxis=dict(
            title="Date",
            rangeselector=dict(),
            rangeslider=dict(visible=True),
            type="date",
        ),
        yaxis_title="News released",
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def plot_trading_data_graph(df_without_duplicates, feature_to_plot):
    average_by_date = (
        df_without_duplicates[feature_to_plot]
        .groupby([df_without_duplicates["datetime"].dt.date])
        .mean()
    )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(average_by_date.index),
                   y=list(average_by_date.values))
    )
    fig.update_layout(
        title="Average {} per market day".format(feature_to_plot),
        width=1200,
        height=450,
        xaxis=dict(
            title="Date",
            rangeselector=dict(),
            rangeslider=dict(visible=True),
            type="date",
        ),
        yaxis_title=f"Average {feature_to_plot}",
    )
    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def build_graph(edges, title, k=9):
    G = nx.Graph()
    G.add_nodes_from(df_comp["company"].unique())
    G.add_weighted_edges_from(edges)
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)

    node_classes = node_classes_new

    class_colors = {
        "MOEXOG": "rgba(51,51,51,1)",
        "MOEXEU": "rgba(255,255,0,1)",
        "MOEXTL": "rgba(102,0,153,1)",
        "MOEXMM": "rgba(204,204,204,1)",
        "MOEXFN": "rgba(0,153,0,1)",
        "MOEXCN": "rgba(204,0,0,1)",
        "MOEXCH": "rgba(204,255,0,1)",
        "MOEXTN": "rgba(0,153,255,1)",
        "MOEXIT": "rgba(0,51,204,1)",
        "MOEXRE": "rgba(102,51,0,1)",
    }

    partition = spectral_clusterization(G, k)

    pos = nx.kamada_kawai_layout(G)

    edge_x = []
    edge_y = []
    weights = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        weights.append(edge[2]["weight"])

    weights = np.array(weights)
    norm_weights = (weights - weights.min()) / (weights.max() - weights.min())

    fig = go.Figure()

    for i in range(len(edge_x) // 3):
        fig.add_trace(
            go.Scatter(
                x=edge_x[i * 3: (i + 1) * 3],
                y=edge_y[i * 3: (i + 1) * 3],
                line=dict(width=2, color=f"rgba(0,0,255,{norm_weights[i]})"),
                hoverinfo="none",
                mode="lines",
                showlegend=False,
            )
        )

    clusters = list(set(partition.values()))
    cluster_colors = {
        cluster: (f"rgba({np.random.randint(0, 255)},"
                  f" {np.random.randint(0, 255)},"
                  f" {np.random.randint(0, 255)}, 0.3)")
        for cluster in clusters
    }

    for cluster in clusters:
        cluster_nodes = [node for node in G.nodes
                         if partition[node] == cluster]
        if len(cluster_nodes) > 2:
            cluster_pos = np.array([pos[node] for node in cluster_nodes])
            hull = ConvexHull(cluster_pos)
            hull_pts = cluster_pos[hull.vertices]
            hull_x = hull_pts[:, 0]
            hull_y = hull_pts[:, 1]
            fig.add_trace(
                go.Scatter(
                    x=hull_x.tolist() + [hull_x[0]],
                    y=hull_y.tolist() + [hull_y[0]],
                    fill="toself",
                    fillcolor=cluster_colors[cluster],
                    line=dict(color="rgba(255,255,255,0)"),
                    hoverinfo="none",
                    mode="lines",
                    showlegend=False,
                )
            )

    node_x = []
    node_y = []
    node_sizes = []
    node_colors = []
    node_texts = []
    for node in pos:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_sizes.append(
            10 + (G.degree(node))
        )  # базовый размер 10, плюс 5 за каждую связь
        node_colors.append(class_colors[node_classes[node]])
        node_texts.append(
            f"Node {node}: Degree {G.degree(node)}, Class {node_classes[node]}"
        )

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=[f"{node}" for node in G.nodes],
            textposition="top center",
            marker=dict(size=node_sizes, color=node_colors),
            hoverinfo="text",
            name="Nodes",
            showlegend=False,
        )
    )

    for node_class, color in class_colors.items():
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(size=10, color=color),
                legendgroup=node_class,
                showlegend=True,
                name=f"{node_class}",
            )
        )

    colorbar_trace = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(
            size=10,
            color=[weights.min(), weights.max()],
            colorscale=[
                f"rgba(0,0,255,{sorted(norm_weights)[i]})"
                for i in range(len(edge_x) // 3)
            ],
            colorbar=dict(
                title="Cosine Similarity",
                titleside="right",
                tickvals=[weights.min(), weights.max()],
                ticktext=[round(weights.min(), 3), round(weights.max(), 3)],
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.1,
                yanchor="top",
            ),
        ),
        showlegend=False,
        hoverinfo="none",
    )

    fig.add_trace(colorbar_trace)

    fig.update_layout(
        showlegend=True,
        autosize=False,
        width=1200,
        height=750,
        title_text=title,
        legend_title_text="Industrial Indexes",
    )
    st.plotly_chart(fig, use_container_width=True)


st.title("News analysis project's dashboard")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["EDA", "Companies", "Industries", "Global", "Graph"]
)

with tab1:
    st.header("General statistics")
    with st.container():
        st.write("First 5 rows of data:")
        st.write(df_eda.head())
        st.write("Let's explore main statistics.")

    st.header("Dates")
    with st.container():
        status = st.selectbox(
            "Select News Provider: ",
            ("Interfax", "Ria", "Smart_Lab", "Kommersant", "Total"),
        )

        if status == "Interfax":
            news_by_date_eda = create_news_by_date(
                df_eda[df_eda["website"] == "Interfax"]
            )
            st.plotly_chart(
                plot_news("Interfax",
                          news_by_date_eda), use_container_width=True
            )
            with st.expander("See Interim Conclusions"):
                st.write(text_messages.TAB1_INTERFAX)
        elif status == "Ria":
            news_by_date_eda = create_news_by_date(
                df_eda[df_eda["website"] == "Ria"])
            st.plotly_chart(
                plot_news("RIA",
                          news_by_date_eda), use_container_width=True
            )
            with st.expander("See Interim Conclusions"):
                st.write(text_messages.TAB1_RIA)
        elif status == "Smart_Lab":
            news_by_date_eda = create_news_by_date(
                df_eda[df_eda["website"] == "Smart_Lab"]
            )
            st.plotly_chart(
                plot_news("Smart-lab",
                          news_by_date_eda), use_container_width=True
            )
            with st.expander("See Interim Conclusions"):
                st.write(text_messages.TAB1_SMART_LAB)
        elif status == "Kommersant":
            news_by_date_eda = create_news_by_date(
                df_eda[df_eda["website"] == "Kommersant"]
            )
            st.plotly_chart(
                plot_news("Kommersant",
                          news_by_date_eda), use_container_width=True
            )
            with st.expander("See Interim Conclusions"):
                st.write(text_messages.TAB1_KOMMERSANT)
        else:
            news_by_date_eda = create_news_by_date(df_eda)
            st.plotly_chart(
                plot_news("Total", news_by_date_eda), use_container_width=True
            )
            with st.expander("See Interim Conclusions"):
                st.write(text_messages.TAB1_TOTAL)

    with st.container():
        plot_body_length_distribution(df_eda)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB1_LENGTH)

with tab2:
    df_no_dup = create_df_no_duplicates(df_comp)
    st.header("General statistics")
    with st.container():
        st.write("First 5 rows of data:")
        st.write(df_comp.head())
        st.write("Let's explore main statistics.")
        st.write(
            df_comp.drop(["datetime",
                          "key_words"], axis=1).describe(include="all")
        )
    with st.container():
        st.header("Website")
        plot_website_graph(df_comp, "News per website (with duplicates)")
        plot_website_graph(df_no_dup, "News per website (without duplicates)")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_WEBSITE)
    with st.container():
        st.header("Section")
        plot_sections_graphs(df_comp)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_SECTION)
    with st.container():
        st.header("Header")
        st.write(
            "There is not much sense in measuring duplicated news,"
            " so we will show statistics without them"
        )
        plot_header_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_HEADER)
    with st.container():
        st.header("Body")
        plot_body_length_distribution(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_BODY)
        plot_body_length_by_date(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_BODY_DATE)
    with st.container():
        st.header("Key Words")
        plot_key_words_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_KEY_WORDS)
    with st.container():
        st.header("Company")
        plot_instrument_graph(df_comp, "company")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_COMPANY)
    with st.container():
        st.header("Date")
        plot_dates_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_DATE)
    with st.container():
        st.header("Trading Data")
        plot_trading_data_graph(df_no_dup, "price_diff_percent")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB2_TRADING)

with tab3:
    df_no_dup = create_df_no_duplicates(df_industry)
    st.header("General statistics")
    with st.container():
        st.write("First 5 rows of data:")
        st.write(df_industry.head())
        st.write("Let's explore main statistics.")
        st.write(
            df_industry.drop(["datetime",
                              "key_words"], axis=1).describe(include="all")
        )
    with st.container():
        st.header("Website")
        plot_website_graph(df_industry, "News per website (with duplicates)")
        plot_website_graph(df_no_dup, "News per website (without duplicates)")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_WEBSITE)
    with st.container():
        st.header("Section")
        plot_sections_graphs(df_industry)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_SECTION)
    with st.container():
        st.header("Header")
        st.write(
            "There is not much sense in measuring duplicated news,"
            " so we will show statistics without them"
        )
        plot_header_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_HEADER)
    with st.container():
        st.header("Body")
        plot_body_length_distribution(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_BODY)
        plot_body_length_by_date(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_BODY_DATE)
    with st.container():
        st.header("Key Words")
        plot_key_words_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_KEY_WORDS)
    with st.container():
        st.header("Industry")
        plot_instrument_graph(df_industry, "industry")
        st.write(
            {
                "MOEXOG": "oil and gas ",
                "MOEXEU": "the electric power",
                "MOEXTL": "telecom",
                "MOEXMM": "metals and mining",
                "MOEXFN": "finance",
                "MOEXCN": "consumer sector",
                "MOEXCH": "chemistry and petrochemistry",
                "MOEXTN": "transport",
                "MOEXIT": "IT",
                "MOEXRE": "real estate",
            }
        )
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_INDUSTRY)
    with st.container():
        st.header("Date")
        plot_dates_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_DATE)
    with st.container():
        st.header("Trading Data")
        plot_trading_data_graph(df_no_dup, "price_diff_percent")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB3_TRADING)

with tab4:
    df_no_dup = create_df_no_duplicates(df_glob)
    st.header("General statistics")
    with st.container():
        st.write("First 5 rows of data:")
        st.write(df_glob.head())
        st.write("Let's explore main statistics.")
        st.write(
            df_glob.drop(["datetime",
                          "key_words"], axis=1).describe(include="all")
        )
        st.write("Don't worry, we will show datetime and key_words further.")
    with st.container():
        st.header("Website")
        plot_website_graph(df_glob, "News per website")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_WEBSITE)
    with st.container():
        st.header("Section")
        plot_sections_graphs(df_glob)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_SECTION)
    with st.container():
        st.header("Header")
        st.write(
            "There is not much sense in measuring duplicated news,"
            " so we will show statistics without them"
        )
        plot_header_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_HEADER)
    with st.container():
        st.header("Body")
        plot_body_length_distribution(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_BODY)
        plot_body_length_by_date(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_BODY_DATE)
    with st.container():
        st.header("Key Words")
        plot_key_words_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_KEY_WORDS)
    with st.container():
        st.header("Date")
        plot_dates_graphs(df_no_dup)
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_DATE)
    with st.container():
        st.header("Trading Data")
        plot_trading_data_graph(df_no_dup, "imoex_price_diff_percent")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_TRADING_IMOEX)
        plot_trading_data_graph(df_no_dup, "rvi_price_diff_percent")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_TRADING_RVI)
        plot_trading_data_graph(df_no_dup, "usd_price_diff_percent")
        with st.expander("See Interim Conclusions"):
            st.markdown(text_messages.TAB4_TRADING_USD)
with tab5:
    embeddings = np.load("Data/embeddings.npy")
    st.header("Graph of companies")
    entities = sorted(df_comp["company"].unique())
    edges = []
    similarity_mat = cosine_similarity(embeddings)
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            similarity = similarity_mat[i][j]
            if similarity > 0.985:
                edges.append((entities[i], entities[j], similarity))
    with st.container():
        build_graph(edges, "GloVe Embeddings, Spectral Clusterization k=9")
    with st.expander("See Interim Conclusions"):
        st.markdown(text_messages.TAB5)
