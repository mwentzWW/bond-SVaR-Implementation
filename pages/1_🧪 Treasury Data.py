import streamlit as st

import utils
import charts

st.set_page_config(
    page_title="Treasury Data",
    page_icon="🧪",
    layout='wide'
)

st.title("🧪 Treasury Data")

df_hist = utils.create_dataframe()

st.session_state['df_hist'] = df_hist

df_abs_diff = utils.generate_abs_diffs(df_hist)

st.session_state['df_abs_diff'] = df_abs_diff

df_rel_diff = utils.generate_rel_diffs(df_hist)

st.session_state['df_rel_diff'] = df_rel_diff

st.write_stream(utils.data_message)

data_col, chart_col = st.columns(2)

with open('utils.py', 'r') as f:

    code: list = f.readlines()

with data_col:

    st.write("## Historical Treasury Data")

    st.dataframe(df_hist)

    st.write("## Absolute 1-Day Rate Changes in Basis Points (bp)")

    st.markdown("**Python Source Code**")

    st.code(" ".join(code[33:48]), language='python')

    st.dataframe(df_abs_diff)

    st.write("### Stats")

    st.dataframe(df_abs_diff.describe(percentiles=[0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]))

    st.divider()

    st.write("## Relative 1-Day Rate Changes in decimal")

    st.markdown("**Python Source Code**")

    st.code(" ".join(code[61:73]), language='python')

    st.dataframe(df_rel_diff)

    st.write("### Stats")

    st.dataframe(df_rel_diff.describe(percentiles=[0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]))

with chart_col:

    #st.plotly_chart(charts.rates_curve_chart(df=df_hist), use_container_width=True)

    with st.form("treasury_selection"):

        option = st.selectbox(
            "Which Treasury do you want to view?",
            st.session_state.df_hist.columns,
            index=None,
            placeholder="Select a Treasury...",
            )
        
       # rel_toggle = st.toggle("Switch to relative charts (Defaults to absolute changes)")

        submitted = st.form_submit_button("Submit")

    if submitted:

        st.write("You selected:", option)

        # if rel_toggle:

        #     df_diff = df_rel_diff

        # else:

        #     df_diff = df_abs_diff

        df_diff = df_abs_diff

        st.dataframe(df_diff[option].describe(percentiles=[0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).transpose())

        st.plotly_chart(charts.rate_line_chart(df=df_hist, y=option), use_container_width=True)

        st.plotly_chart(charts.rate_line_chart(df=df_diff, y=option), use_container_width=True)

        st.plotly_chart(charts.histogram_chart(df=df_diff, x=option), use_container_width=True)

        st.plotly_chart(charts.cumulative_dist_chart(df=df_diff, x=option), use_container_width=True)