import streamlit as st

import utils
import charts

df_hist = utils.create_dataframe()

df_diff = utils.generate_abs_diffs(df_hist)

st.title("🧙‍♂️ Stressed Value at Risk")

tab_data, tab_chart = st.tabs(["Data", "Chart"])

tab_data.write_stream(utils.data_message)

tab_data.dataframe(df_hist)

tab_data.dataframe(df_diff)

tab_chart.plotly_chart(charts.rate_line_chart(df=df_hist), use_container_width=True)

tab_chart.write(df_diff.describe(percentiles=[0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]))

tab_chart.plotly_chart(charts.histogram_chart(df=df_diff), use_container_width=True)

tab_chart.plotly_chart(charts.cumulative_dist_chart(df=df_diff), use_container_width=True)
