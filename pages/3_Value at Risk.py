import streamlit as st

st.set_page_config(
    page_title="Value at Risk",
    layout='wide'
)

st.title("Value at Risk")

bond = st.session_state['bond']

with st.form("shocks"):

    yield_shock = st.number_input("Yield Shock (bps)",
                            value=10,
                            min_value=-1_000,
                            max_value=1_000,
                            step=1)

    submitted = st.form_submit_button("Shock")

col1, col2 = st.columns(2)

if submitted:

    price, df = bond.revalue(yield_shock)

    with col1:

        st.write(f"Price at {bond.issue_ytm_percent:.2f}% -> ${bond.issue_price:.3f}")

        st.dataframe(bond.cashflows)

    with col2:

        st.write(f"Price at {(bond.issue_ytm_percent + yield_shock/100):.2f}% -> ${price:.3f}")

        st.dataframe(df)