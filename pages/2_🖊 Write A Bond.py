import streamlit as st
from dataclasses import fields

from valuation import Treasury

st.set_page_config(
    page_title="Write A Bond",
    page_icon="🖊",
    layout='wide'
)

st.title("🖊 Write A Bond")

col1, col2 = st.columns(2)

input_defualts = dict()

for field in fields(Treasury):

    if field.default != field.default_factory:

        record = {
            f"{field.name}": field.default
        }

        input_defualts.update(record)

with col1:

    with st.form("write_bond"):

        cusip = st.text_input("CUSIP", input_defualts["cusip"])
        name = st.text_input("Security Name", input_defualts["name"])
        term_years = st.number_input("Term (Yrs)", 
                                    value=input_defualts["term_years"],
                                    min_value=0.1,
                                    max_value=100.0)
        issue_date = st.date_input("Issue Date", input_defualts["issue_date"])
        coupon_rate_percent = st.number_input("Coupon Rate (%)", 
                                            value=input_defualts["coupon_rate_percent"],
                                            min_value=0.01,
                                            max_value=100.0,
                                            step=0.25)
        coupon_payment_frequency = st.number_input("Coupon Payment Frequency (Months)", 
                                                value=input_defualts["coupon_payment_frequency"],
                                                min_value=1,
                                                max_value=12,
                                                step=1)
        issue_price = st.number_input("Issue Price ($/100)", 
                                    value=input_defualts["issue_price"],
                                    min_value=0.01,
                                    max_value=200.0,
                                    step=0.001)
        position_millions = st.number_input("Position Size ($ Million)", 
                                            value=input_defualts["position_millions"],
                                            min_value=1)

        submitted = st.form_submit_button("Write")

if submitted:

    bond = Treasury(
        cusip=cusip,
        name=name,
        term_years=term_years,
        issue_date=issue_date,
        coupon_rate_percent=coupon_rate_percent,
        coupon_payment_frequency=coupon_payment_frequency,
        issue_price=issue_price,
        position_millions=position_millions
    )

    st.session_state['bond'] = bond

    with col2:

        st.write("Bond Spec")

        st.write(bond)

    df = bond.cashflows

    st.dataframe(df)

    bar_cols = ["principal", "coupon"]

    st.bar_chart(df, x="date", y=bar_cols)