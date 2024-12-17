from dataclasses import dataclass, field
from datetime import date, datetime
import pandas as pd
from scipy.optimize import minimize_scalar


@dataclass
class Treasury:
    """Class to create a Treasury instrument with the cashflows and valuation methods."""

    # generates after init
    first_pay: str = field(init=False)
    maturity: str = field(init=False)
    cashflows: pd.DataFrame = field(init=False)
    eff_duration: float = field(init=False)
    dv01: float = field(init=False)

    issue_ytm_percent: float = field(init=False)  # yield to maturity given issue price

    cusip: str = 'BCC000000'
    name: str = '10-Year Note'
    term_years: float = 10.0
    issue_date: date = date(2024, 12, 31)
    coupon_rate_percent: float = 6.0

    # monthly payment frequency, 6 for semi-annual, 12 for annual
    coupon_payment_frequency: int = 6
    issue_price: float = 100.0
    position_millions: int = 10  # also face value amount


    def __post_init__(self):

       self.generate_cashflows()

       self.issue_ytm_percent = self.yield_to_maturity()*100

       self.risk_analytics()

    def generate_cashflows(self):
        """Generates cashflow dataframe given initial values"""

         # add one because initial date isn't included in payments
        n_periods = self.term_years*(12/self.coupon_payment_frequency) + 1

        date_range = pd.date_range(
            start=self.issue_date, 
            periods=n_periods, 
            freq=f'{self.coupon_payment_frequency}ME',
            inclusive='right')

        self.first_pay = date_range[0].strftime("%Y-%m-%d")
        self.maturity = date_range[-1].strftime("%Y-%m-%d")

        principal = self.position_millions*1e6

        cpn_payment_per_period = principal * \
            (self.coupon_rate_percent/100) / \
            2  # divide by 2 for 2 payments per year
        
        data = {
            'date': date_range,
            'coupon': cpn_payment_per_period 
        }

        df_cashflows = pd.DataFrame(data)

        df_cashflows['principal'] = 0

        df_cashflows.iloc[-1, df_cashflows.columns.get_loc('principal')] = principal

        df_cashflows['delta_years'] = (df_cashflows['date'] - datetime(year=self.issue_date.year, month=self.issue_date.month, day=self.issue_date.day)).dt.days/365

        df_cashflows['total_payment'] = df_cashflows['coupon'] + df_cashflows['principal']

        self.cashflows = df_cashflows

    def yield_to_maturity(self) -> float:
        """Given price solve for yield to maturity of cashflows"""

        # minimize Price = sum of cashflows discounted

        def obj_fun(ytm_dec: float):
            """Given ytm and cashflows, calculates difference between value given price and calculated net present value"""

            df = self.cashflows

            df['discounted_value'] = df['total_payment'] / ((1 + ytm_dec)**(df['delta_years']))

            npv_price = (df['discounted_value'].sum()/df['principal'].sum())*100

            abs_price_diff = abs(self.issue_price - npv_price)

            return abs_price_diff

        result = minimize_scalar(obj_fun, method='bounded', bounds=(0.001, 0.9))

        if result.success:

            return result.x
        
        else:

            return 0.0

    def revalue(self, ytm_delta: float) -> tuple[float, pd.DataFrame]:
        """Given yield change in basis points, revalue cashflows.
        
            returns: price, dataframe
        """

        delta_decimal = ytm_delta/10_000

        df = self.cashflows.copy(deep=True)

        df['discounted_value'] = df['total_payment'] / ((1 + (self.issue_ytm_percent/100) + delta_decimal)**(df['delta_years']))

        npv_price = (df['discounted_value'].sum()/df['principal'].sum())*100

        return npv_price, df

    def risk_analytics(self, shock_bps: float=10):
        """Computes the initial effective duration and DV01"""

        shock_up_price, _ = self.revalue(shock_bps)

        shock_down_price, _ = self.revalue(-shock_bps)

        self.eff_duration = (shock_down_price - shock_up_price)/(2*(shock_bps/10_000)*self.issue_price)

        self.dv01 = self.eff_duration*(self.position_millions*10**6)*(self.issue_price/100)/10_000

    def price_vs_rates(self):
        # TODO: Input yields and return prices to chart
        pass