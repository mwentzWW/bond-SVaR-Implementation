import streamlit as st
import streamlit.components.v1 as components

import utils

st.set_page_config(
    page_title="Home",
    page_icon="🧙‍♂️",
    layout='wide'
)

st.sidebar.success("Select a page above to get started.")

st.write("# Welcome to my app 🧙‍♂️")

st.write_stream(utils.home_message())

st.markdown(
    """

    ## App Introduction

    [Streamlit](https://streamlit.io) is an open-source app framework built specifically for
    Machine Learning and Data Science projects.

    This is my first app built using streamlit.

    My goal for this project is to learn the basics of streamlit apps and deployment. I'll create a simple historical value at risk (VaR) tool for treasury bond analysis based on public data.

    For this project, we are calling the historical VaR the Stressed VaR (SVaR) since it includes stress periods in the past.

    ## VaR Methodology (Fixed Income Assets)

    Model workflow:

        1. We will generate the absolute and relative changes in treasury par rates in the dataset.

        2. The user will submit information about their instrument and it will be mapped to a treasury benchmark.

        3. Based on the mapping and size of the position, the VaR measure will be estimated.

    $$\mathbb{N} = \{ a \in \mathbb{Z} : a > 0 \}$$

    ## VaR Resources

    * [2010 IMF Conference On Operationalizing Systemic Risk Monitoring](https://www.imf.org/external/np/seminars/eng/2010/mcm/pdf/RBerner.pdf)
    * Ken Abbott's MIT Lecture on Value at Risk (VAR) Models 
        * [Video Link](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/lecture-7-value-at-risk-var-models/)
        * [Lecture Notes](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_lecnote7/)
    * [CME Calculate Dollar Value of Basis Point (DVBP or DV01)](https://www.cmegroup.com/trading/interest-rates/files/Calculating_the_Dollar_Value_of_a_Basis_Point.pdf)
    * [Corporate Finance Institute (CFI) Site](https://corporatefinanceinstitute.com/)
        * [Matrix Pricing](https://corporatefinanceinstitute.com/resources/career-map/sell-side/capital-markets/matrix-pricing/)
        * [Corporate Bond Valuation](https://corporatefinanceinstitute.com/resources/valuation/corporate-bond-valuation/)
        * [Duration](https://corporatefinanceinstitute.com/resources/fixed-income/duration/)
    * [openstax Principles of Finance 10.2 Bond Valuation](https://openstax.org/books/principles-finance/pages/10-2-bond-valuation)
    
    ## Data Source

    [Treasury Interest Rates Par Yield Curve](https://home.treasury.gov/interest-rates-data-csv-archive)


"""
)


