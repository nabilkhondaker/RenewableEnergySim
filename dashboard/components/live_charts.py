import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_main_dashboard(results: dict):
    """Renders the interactive dual-axis power dispatch chart."""
    if not results["time"]:
        st.warning("No data available to plot.")
        return

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # PV Generation Fill
    fig.add_trace(
        go.Scatter(x=results["time"], y=results["pv_generation_kw"], 
                   name="PV Output (kW)", fill='tozeroy', 
                   marker_color='rgba(255, 165, 0, 0.6)', line=dict(color='orange', width=2)),
        secondary_y=False
    )
    
    # Load Profile
    fig.add_trace(
        go.Scatter(x=results["time"], y=results["load_kw"], 
                   name="Load Demand (kW)", line=dict(color='#ff3333', dash='dash', width=2)),
        secondary_y=False
    )
    
    # Battery SOC Line
    fig.add_trace(
        go.Scatter(x=results["time"], y=results["battery_soc"], 
                   name="Battery SOC (%)", line=dict(color='#00ff88', width=3)),
        secondary_y=True
    )

    fig.update_layout(
        title="24-Hour Dispatch & Storage Optimization",
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_yaxes(title_text="Power (kW)", secondary_y=False, showgrid=True, gridcolor='#333')
    fig.update_yaxes(title_text="State of Charge (%)", secondary_y=True, range=[0, 100], showgrid=False)

    st.plotly_chart(fig, use_container_width=True)
