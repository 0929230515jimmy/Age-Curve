import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Baseball Stats Dashboard")

batting_data = pd.read_csv("https://github.com/0929230515jimmy/Age-Curve/blob/main/batting_final.csv?raw=True")
pitching_data = pd.read_csv("https://github.com/0929230515jimmy/Age-Curve/blob/main/pitching_final.csvraw=True")

if 'Oppo%' in batting_data.columns:
    batting_data['Oppo%'] = pd.to_numeric(batting_data['Oppo%'], errors='coerce')

batting_data.columns = batting_data.columns.str.strip()
pitching_data.columns = pitching_data.columns.str.strip()

st.sidebar.title("Baseball Stats Analysis")
player_type = st.sidebar.radio("Select Player Type", ["Batter", "Pitcher", "Old VS Modern"])

st.title(f"Baseball {player_type} Statistics")

if player_type == "Batter":
    st.subheader("Age Distribution")
    age_counts = batting_data['Age'].value_counts().sort_index()
    fig_age = go.Figure()
    fig_age.add_trace(go.Scatter(
        x=age_counts.index,
        y=age_counts.values,
        mode='lines+markers',
        name='Count',
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age.update_layout(
        template='plotly_white',
        yaxis_title='Number of Players',
        xaxis_title='Age'
    )
    st.plotly_chart(fig_age, use_container_width=True)

    metrics = ['PA', 'rOBA', 'BAbip', 'ISO', 'HardH%', 'LD%', 'GB%', 'FB%', 'Pull%', 'Cent%', 'Oppo%', 'BB%', 'SO%']
    batting_grouped = batting_data.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in metrics}
    }).reset_index()

    col1, col2 = st.columns(2)
    
    # Graph 1: Age vs PA
    with col1:
        st.subheader("Age vs Plate Appearances")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=batting_grouped['Age'],
            y=batting_grouped[('PA', 'mean')],
            mode='lines+markers',
            name='PA',
            hovertemplate="Age: %{x}<br>PA: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=batting_grouped[('PA', 'count')]
        ))
        fig1.update_layout(template='plotly_white', yaxis_title='Plate Appearances')
        st.plotly_chart(fig1, use_container_width=True)

    # Graph 2: Age vs Batting Metrics
    with col2:
        st.subheader("Age vs Batting Metrics")
        fig2 = go.Figure()
        metrics = ['rOBA', 'BAbip', 'ISO']
        for metric in metrics:
            fig2.add_trace(go.Scatter(
                x=batting_grouped['Age'],
                y=batting_grouped[(metric, 'mean')],
                name=metric,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=batting_grouped[(metric, 'count')]
            ))
        fig2.update_layout(template='plotly_white', yaxis_title='Value')
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    # Graph 3: Age vs Hit Types
    with col3:
        st.subheader("Age vs Hit Types")
        fig3 = go.Figure()
        hit_types = ['HardH%', 'LD%', 'GB%', 'FB%']
        for hit_type in hit_types:
            fig3.add_trace(go.Scatter(
                x=batting_grouped['Age'],
                y=batting_grouped[(hit_type, 'mean')],
                name=hit_type,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{hit_type}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=batting_grouped[(hit_type, 'count')]
            ))
        fig3.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig3, use_container_width=True)

    # Graph 4: Age vs Hit Direction
    with col4:
        st.subheader("Age vs Hit Direction")
        fig4 = go.Figure()
        directions = ['Pull%', 'Cent%', 'Oppo%']
        for direction in directions:
            fig4.add_trace(go.Scatter(
                x=batting_grouped['Age'],
                y=batting_grouped[(direction, 'mean')],
                name=direction,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{direction}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=batting_grouped[(direction, 'count')]
            ))
        fig4.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig4, use_container_width=True)

    # Graph 5: Age vs BB% and SO%
    st.subheader("Age vs Walk and Strikeout Rates")
    fig5 = go.Figure()
    rates = ['BB%', 'SO%']
    for rate in rates:
        fig5.add_trace(go.Scatter(
            x=batting_grouped['Age'],
            y=batting_grouped[(rate, 'mean')],
            name=rate,
            mode='lines+markers',
            hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
            customdata=batting_grouped[(rate, 'count')]
        ))
    fig5.update_layout(template='plotly_white', yaxis_title='Percentage')
    st.plotly_chart(fig5, use_container_width=True)
    
# Pitcher graphs
elif player_type == "Pitcher":  
    st.subheader("Age Distribution")
    age_counts = pitching_data['Age'].value_counts().sort_index()
    fig_age = go.Figure()
    fig_age.add_trace(go.Scatter(
        x=age_counts.index,
        y=age_counts.values,
        mode='lines+markers',
        name='Count',
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age.update_layout(
        template='plotly_white',
        yaxis_title='Number of Players',
        xaxis_title='Age'
    )
    st.plotly_chart(fig_age, use_container_width=True)

    metrics = ['IP', 'BA', 'OBP', 'SLG', 'OPS', 'BAbip', 'HardH%', 'LD%', 'GB%', 'FB%', 'BB%', 'K%']
    pitching_grouped = pitching_data.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in metrics}
    }).reset_index()

    col1, col2 = st.columns(2)
    
    # Graph 1: Age vs IP
    with col1:
        st.subheader("Age vs Innings Pitched")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=pitching_grouped['Age'],
            y=pitching_grouped[('IP', 'mean')],
            mode='lines+markers',
            name='IP',
            hovertemplate="Age: %{x}<br>IP: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=pitching_grouped[('IP', 'count')]
        ))
        fig1.update_layout(template='plotly_white', yaxis_title='Innings Pitched')
        st.plotly_chart(fig1, use_container_width=True)

    # Graph 2: Age vs Batting Metrics
    with col2:
        st.subheader("Age vs Batting Metrics Against")
        fig2 = go.Figure()
        batting_metrics = ['BA', 'OBP', 'SLG', 'OPS', 'BAbip']
        for metric in batting_metrics:
            fig2.add_trace(go.Scatter(
                x=pitching_grouped['Age'],
                y=pitching_grouped[(metric, 'mean')],
                name=metric,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=pitching_grouped[(metric, 'count')]
            ))
        fig2.update_layout(template='plotly_white', yaxis_title='Value')
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    
    # Graph 3: Age vs Hit Types
    with col3:
        st.subheader("Age vs Hit Types Against")
        fig3 = go.Figure()
        hit_types = ['HardH%', 'LD%', 'GB%', 'FB%']
        for hit_type in hit_types:
            fig3.add_trace(go.Scatter(
                x=pitching_grouped['Age'],
                y=pitching_grouped[(hit_type, 'mean')],
                name=hit_type,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{hit_type}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=pitching_grouped[(hit_type, 'count')]
            ))
        fig3.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig3, use_container_width=True)

    # Graph 4: Age vs BB% and K%
    with col4:
        st.subheader("Age vs Walk and Strikeout Rates")
        fig4 = go.Figure()
        rates = ['BB%', 'K%']
        for rate in rates:
            fig4.add_trace(go.Scatter(
                x=pitching_grouped['Age'],
                y=pitching_grouped[(rate, 'mean')],
                name=rate,
                mode='lines+markers',
                hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=pitching_grouped[(rate, 'count')]
            ))
        fig4.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig4, use_container_width=True)

else:
    # Modern vs Old Batter Analysis
    st.header("Modern vs Old Batter Analysis")

    old_era_batting = batting_data[batting_data['Year'].between(2010, 2014)]
    modern_era_batting = batting_data[batting_data['Year'].between(2015, 2023)]

    metrics = ['PA', 'rOBA', 'BAbip', 'ISO', 'Pull%', 'Cent%', 'Oppo%', 'BB%', 'SO%']
    old_era_grouped = old_era_batting.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in metrics}
    }).reset_index()
    modern_era_grouped = modern_era_batting.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in metrics}
    }).reset_index()

    # Age Distribution Comparison
    st.subheader("Age Distribution by Era")
    fig_age_comp = go.Figure()
    fig_age_comp.add_trace(go.Scatter(
        x=old_era_batting['Age'].value_counts().sort_index().index,
        y=old_era_batting['Age'].value_counts().sort_index().values,
        mode='lines+markers',
        name='2010-2014',
        line=dict(color='royalblue', dash='solid'),
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age_comp.add_trace(go.Scatter(
        x=modern_era_batting['Age'].value_counts().sort_index().index,
        y=modern_era_batting['Age'].value_counts().sort_index().values,
        mode='lines+markers',
        name='2015-2023',
        line=dict(color='royalblue', dash='dash'),
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age_comp.update_layout(
        template='plotly_white',
        yaxis_title='Number of Players',
        xaxis_title='Age'
    )
    st.plotly_chart(fig_age_comp, use_container_width=True)

    col1, col2 = st.columns(2)

    # Age vs Plate Appearances Comparison
    with col1:
        st.subheader("Age vs Plate Appearances by Era")
        fig_pa = go.Figure()
        fig_pa.add_trace(go.Scatter(
            x=old_era_grouped['Age'],
            y=old_era_grouped[('PA', 'mean')],
            mode='lines+markers',
            name='2010-2014',
            line=dict(color='royalblue', dash='solid'),
            hovertemplate="Age: %{x}<br>PA: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=old_era_grouped[('PA', 'count')]
        ))
        fig_pa.add_trace(go.Scatter(
            x=modern_era_grouped['Age'],
            y=modern_era_grouped[('PA', 'mean')],
            mode='lines+markers',
            name='2015-2023',
            line=dict(color='royalblue', dash='dash'),
            hovertemplate="Age: %{x}<br>PA: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=modern_era_grouped[('PA', 'count')]
        ))
        fig_pa.update_layout(template='plotly_white', yaxis_title='Plate Appearances')
        st.plotly_chart(fig_pa, use_container_width=True)

    # Age vs Batting Metrics Comparison
    with col2:
        st.subheader("Age vs Batting Metrics by Era")
        fig_metrics = go.Figure()
        metrics = ['rOBA', 'BAbip', 'ISO']
        colors = {'rOBA': 'royalblue', 'BAbip': 'green', 'ISO': 'purple'}
        for metric in metrics:
            fig_metrics.add_trace(go.Scatter(
                x=old_era_grouped['Age'],
                y=old_era_grouped[(metric, 'mean')],
                name=f'{metric} (2010-2014)',
                mode='lines+markers',
                line=dict(color=colors[metric], dash='solid'),
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=old_era_grouped[(metric, 'count')]
            ))
            fig_metrics.add_trace(go.Scatter(
                x=modern_era_grouped['Age'],
                y=modern_era_grouped[(metric, 'mean')],
                name=f'{metric} (2015-2023)',
                mode='lines+markers',
                line=dict(color=colors[metric], dash='dash'),
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=modern_era_grouped[(metric, 'count')]
            ))
        fig_metrics.update_layout(template='plotly_white', yaxis_title='Value')
        st.plotly_chart(fig_metrics, use_container_width=True)

    col3, col4 = st.columns(2)

    # Age vs Hit Direction Comparison
    with col3:
        st.subheader("Age vs Hit Direction by Era")
        fig_direction = go.Figure()
        directions = ['Pull%', 'Cent%', 'Oppo%']
        colors = {'Pull%': 'royalblue', 'Cent%': 'green', 'Oppo%': 'purple'}
        for direction in directions:
            fig_direction.add_trace(go.Scatter(
                x=old_era_grouped['Age'],
                y=old_era_grouped[(direction, 'mean')],
                name=f'{direction} (2010-2014)',
                mode='lines+markers',
                line=dict(color=colors[direction], dash='solid'),
                hovertemplate=f"Age: %{{x}}<br>{direction}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=old_era_grouped[(direction, 'count')]
            ))
            fig_direction.add_trace(go.Scatter(
                x=modern_era_grouped['Age'],
                y=modern_era_grouped[(direction, 'mean')],
                name=f'{direction} (2015-2023)',
                mode='lines+markers',
                line=dict(color=colors[direction], dash='dash'),
                hovertemplate=f"Age: %{{x}}<br>{direction}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=modern_era_grouped[(direction, 'count')]
            ))
        fig_direction.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig_direction, use_container_width=True)

    # Age vs BB% and SO% Comparison
    with col4:
        st.subheader("Age vs Walk and Strikeout Rates by Era")
        fig_rates = go.Figure()
        rates = ['BB%', 'SO%']
        colors = {'BB%': 'royalblue', 'SO%': 'green'}
        for rate in rates:
            fig_rates.add_trace(go.Scatter(
                x=old_era_grouped['Age'],
                y=old_era_grouped[(rate, 'mean')],
                name=f'{rate} (2010-2014)',
                mode='lines+markers',
                line=dict(color=colors[rate], dash='solid'),
                hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=old_era_grouped[(rate, 'count')]
            ))
            fig_rates.add_trace(go.Scatter(
                x=modern_era_grouped['Age'],
                y=modern_era_grouped[(rate, 'mean')],
                name=f'{rate} (2015-2023)',
                mode='lines+markers',
                line=dict(color=colors[rate], dash='dash'),
                hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
                customdata=modern_era_grouped[(rate, 'count')]
            ))
        fig_rates.update_layout(template='plotly_white', yaxis_title='Percentage')
        st.plotly_chart(fig_rates, use_container_width=True)

    # Modern vs Old Pitcher Analysis
    st.header("Modern vs Old Pitcher Analysis")

    old_era_pitching = pitching_data[pitching_data['Year'].between(2010, 2014)]
    modern_era_pitching = pitching_data[pitching_data['Year'].between(2015, 2023)]

    pitching_metrics = ['IP', 'SLG', 'OBP', 'BAbip', 'BB%', 'K%']
    old_era_pitching_grouped = old_era_pitching.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in pitching_metrics}
    }).reset_index()
    modern_era_pitching_grouped = modern_era_pitching.groupby('Age').agg({
        **{metric: ['mean', 'count'] for metric in pitching_metrics}
    }).reset_index()

    # Age Distribution Comparison
    st.subheader("Age Distribution by Era")
    fig_age_comp_p = go.Figure()
    fig_age_comp_p.add_trace(go.Scatter(
        x=old_era_pitching['Age'].value_counts().sort_index().index,
        y=old_era_pitching['Age'].value_counts().sort_index().values,
        mode='lines+markers',
        name='2010-2014',
        line=dict(color='royalblue', dash='solid'),
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age_comp_p.add_trace(go.Scatter(
        x=modern_era_pitching['Age'].value_counts().sort_index().index,
        y=modern_era_pitching['Age'].value_counts().sort_index().values,
        mode='lines+markers',
        name='2015-2023',
        line=dict(color='royalblue', dash='dash'),
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>"
    ))
    fig_age_comp_p.update_layout(
        template='plotly_white',
        yaxis_title='Number of Players',
        xaxis_title='Age'
    )
    st.plotly_chart(fig_age_comp_p, use_container_width=True)

    col5, col6 = st.columns(2)

    # Age vs IP Comparison
    with col5:
        st.subheader("Age vs Innings Pitched by Era")
        fig_ip = go.Figure()
        fig_ip.add_trace(go.Scatter(
            x=old_era_pitching_grouped['Age'],
            y=old_era_pitching_grouped[('IP', 'mean')],
            mode='lines+markers',
            name='2010-2014',
            line=dict(color='royalblue', dash='solid'),
            hovertemplate="Age: %{x}<br>IP: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=old_era_pitching_grouped[('IP', 'count')]
        ))
        fig_ip.add_trace(go.Scatter(
            x=modern_era_pitching_grouped['Age'],
            y=modern_era_pitching_grouped[('IP', 'mean')],
            mode='lines+markers',
            name='2015-2023',
            line=dict(color='royalblue', dash='dash'),
            hovertemplate="Age: %{x}<br>IP: %{y:.1f}<br>Count: %{customdata}<extra></extra>",
            customdata=modern_era_pitching_grouped[('IP', 'count')]
        ))
        fig_ip.update_layout(template='plotly_white', yaxis_title='Innings Pitched')
        st.plotly_chart(fig_ip, use_container_width=True)

    # Age vs Batting Metrics Comparison
    with col6:
        st.subheader("Age vs Batting Metrics Against by Era")
        fig_p_metrics = go.Figure()
        p_metrics = ['SLG', 'OBP', 'BAbip']
        colors = {'SLG': 'royalblue', 'OBP': 'green', 'BAbip': 'purple'}
        for metric in p_metrics:
            fig_p_metrics.add_trace(go.Scatter(
                x=old_era_pitching_grouped['Age'],
                y=old_era_pitching_grouped[(metric, 'mean')],
                name=f'{metric} (2010-2014)',
                mode='lines+markers',
                line=dict(color=colors[metric], dash='solid'),
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=old_era_pitching_grouped[(metric, 'count')]
            ))
            fig_p_metrics.add_trace(go.Scatter(
                x=modern_era_pitching_grouped['Age'],
                y=modern_era_pitching_grouped[(metric, 'mean')],
                name=f'{metric} (2015-2023)',
                mode='lines+markers',
                line=dict(color=colors[metric], dash='dash'),
                hovertemplate=f"Age: %{{x}}<br>{metric}: %{{y:.3f}}<br>Count: %{{customdata}}<extra></extra>",
                customdata=modern_era_pitching_grouped[(metric, 'count')]
            ))
        fig_p_metrics.update_layout(template='plotly_white', yaxis_title='Value')
        st.plotly_chart(fig_p_metrics, use_container_width=True)

    # Age vs BB% and K% Comparison
    st.subheader("Age vs Walk and Strikeout Rates by Era")
    fig_p_rates = go.Figure()
    p_rates = ['BB%', 'K%']
    colors = {'BB%': 'royalblue', 'K%': 'green'}
    for rate in p_rates:
        fig_p_rates.add_trace(go.Scatter(
            x=old_era_pitching_grouped['Age'],
            y=old_era_pitching_grouped[(rate, 'mean')],
            name=f'{rate} (2010-2014)',
            mode='lines+markers',
            line=dict(color=colors[rate], dash='solid'),
            hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
            customdata=old_era_pitching_grouped[(rate, 'count')]
        ))
        fig_p_rates.add_trace(go.Scatter(
            x=modern_era_pitching_grouped['Age'],
            y=modern_era_pitching_grouped[(rate, 'mean')],
            name=f'{rate} (2015-2023)',
            mode='lines+markers',
            line=dict(color=colors[rate], dash='dash'),
            hovertemplate=f"Age: %{{x}}<br>{rate}: %{{y:.1f}}%<br>Count: %{{customdata}}<extra></extra>",
            customdata=modern_era_pitching_grouped[(rate, 'count')]
        ))
    fig_p_rates.update_layout(template='plotly_white', yaxis_title='Percentage')
    st.plotly_chart(fig_p_rates, use_container_width=True)
