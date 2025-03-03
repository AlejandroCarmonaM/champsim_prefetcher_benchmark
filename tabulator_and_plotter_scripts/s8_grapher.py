import pandas as pd
import plotly.graph_objects as go

def output_acc_cov_plots():

    # Read CSV file
    df = pd.read_csv('all_trace_data_s8.csv')

    # Get unique applications and prefetchers
    applications = ['602.gcc_s-2226B', '623.xalancbmk_s-202B', '654.roms_s-1390B', '649.fotonik3d_s-1176B']
    prefetchers = df['Prefetcher'].unique()
    prefetchers = prefetchers[prefetchers != 'baseline']  # Remove baseline

    # Calculate averages for each prefetcher
    df_avg = df.groupby('Prefetcher')[['Accuracy', 'Coverage']].mean()

    # Colors for different prefetchers
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Create Accuracy plot
    fig_accuracy = go.Figure()

    for idx, prefetcher in enumerate(prefetchers):
        data = df[df['Prefetcher'] == prefetcher]
        y_data = list(data.set_index('Application').loc[applications, 'Accuracy'])
        y_data.append(df_avg.loc[prefetcher, 'Accuracy'])
        
        fig_accuracy.add_trace(
            go.Bar(name=prefetcher,
                x=applications + ['Average'],
                y=y_data,
                marker_color=colors[idx])
        )

    fig_accuracy.update_layout(
        height=600,
        barmode='group',
        title_text="Prefetcher Accuracy Analysis",
        yaxis_title="Accuracy",
        showlegend=True,
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Create Coverage plot
    fig_coverage = go.Figure()

    for idx, prefetcher in enumerate(prefetchers):
        data = df[df['Prefetcher'] == prefetcher]
        y_data = list(data.set_index('Application').loc[applications, 'Coverage'])
        y_data.append(df_avg.loc[prefetcher, 'Coverage'])
        
        fig_coverage.add_trace(
            go.Bar(name=prefetcher,
                x=applications + ['Average'],
                y=y_data,
                marker_color=colors[idx])
        )

    fig_coverage.update_layout(
        height=600,
        barmode='group',
        title_text="Prefetcher Coverage Analysis",
        yaxis_title="Coverage",
        showlegend=True,
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Save plots to image files
    fig_accuracy.write_image("prefetcher_accuracy.png")
    fig_coverage.write_image("prefetcher_coverage.png")

    print("Plots saved to prefetcher_accuracy.png and prefetcher_coverage.png")

def output_norm_speedup_plot():
    # Read CSV file
    df = pd.read_csv('all_trace_data_s8.csv')
    
    # Filter out baseline
    df = df[df['Prefetcher'] != 'baseline']
    
    # Get unique applications and prefetchers
    applications = ['602.gcc_s-2226B', '623.xalancbmk_s-202B', '654.roms_s-1390B', '649.fotonik3d_s-1176B']
    prefetchers = df['Prefetcher'].unique()
    
    # Calculate geometric mean for each prefetcher
    geomean = df.groupby('Prefetcher')['Normalized_IPC'].apply(lambda x: x.prod() ** (1/len(x)))
    
    # Colors for different prefetchers
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for each prefetcher
    for idx, prefetcher in enumerate(prefetchers):
        data = df[df['Prefetcher'] == prefetcher]
        y_data = list(data.set_index('Application').loc[applications, 'Normalized_IPC'])
        y_data.append(geomean[prefetcher])
        
        fig.add_trace(
            go.Bar(name=prefetcher,
                  x=applications + ['Geomean'],
                  y=y_data,
                  marker_color=colors[idx])
        )
    
    # Update layout
    fig.update_layout(
        height=600,
        barmode='group',
        title_text="Normalized Speedup Analysis",
        yaxis_title="Normalized Speedup",
        yaxis=dict(
            tickformat='.2f',
            range=[0.9, max(df['Normalized_IPC'].max() * 1.1, 1.9)]
        ),
        showlegend=True,
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Save plot
    fig.write_image("normalized_speedup.png")
    print("Plot saved to normalized_speedup.png")

if __name__ == "__main__":
    output_acc_cov_plots()
    output_norm_speedup_plot()