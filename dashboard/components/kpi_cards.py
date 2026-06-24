import streamlit as st

def render_kpi_cards(results: dict):
    """Renders the top-level system metrics."""
    st.markdown("### System Telemetry")
    
    col1, col2, col3, col4 = st.columns(4)
    
    max_pv = max(results['pv_generation_kw']) if results['pv_generation_kw'] else 0
    total_import = sum(results['grid_import_kw'])
    total_export = sum(results['grid_export_kw'])
    end_soc = results['battery_soc'][-1] if results['battery_soc'] else 0
    
    col1.metric("Peak PV Yield", f"{max_pv:.2f} kW")
    col2.metric("Grid Import (Total)", f"{total_import:.2f} kWh")
    col3.metric("Grid Export (Total)", f"{total_export:.2f} kWh")
    col4.metric("Ending ESS SOC", f"{end_soc:.1f} %")
    
    st.markdown("---")
