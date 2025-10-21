import streamlit as st # type: ignore

st.title("Investment & Valuation Calculator")

# --- User Inputs ---
#TAM = st.number_input("TAM ($M)", min_value=0.0, step=1000.0) * 1000000

NumberConsumers = st.number_input("Number of Potential Users (K)", min_value=0.0, step=1.0) * 1,000
RevPerConsumer = st.number_input("Revenue Per User ($)", min_value=0.0, step=1.0)
Penetration = st.number_input("Penetration (%)", min_value=0.0, max_value=100.0, step=1.0)
ChanceSuccess = st.number_input("Chance of Success (%)", min_value=0.0, max_value=100.0, step=1.0)
DiscountRate = st.number_input("Discount Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
ProposedValuation = st.number_input("Proposed Valuation ($M)", min_value=0.0, step=1000.0) * 1,000,000
InvestmentAmount = st.number_input("Investment Amount ($K)", min_value=0.0, step=1000.0) * 1,000

TAM = RevPerConsumer * NumberConsumers

def ARR(TAM,Penetration):
    return TAM * (Penetration / 100)

def NPV(ARR_value, DiscountRate, years=7):
    npv = 0
    for t in range(1, years + 1):
        npv += ARR_value / ((1 + (DiscountRate / 100)) ** t)
    return npv

def ExpectedValuation(npv, ChanceSuccess):
    return npv * (ChanceSuccess / 100)

def ValuePerDollar(ExpectedValuation, ProposedValuation):
    return (ExpectedValuation / ProposedValuation) - 1

def ProfitTotal(InvestmentAmount, ValuePerDollar):
    return InvestmentAmount * ValuePerDollar

# --- Compute on Button Click ---
if st.button("Calculate"):
    arr_value = ARR(TAM, Penetration)
    npv_value = NPV(arr_value, DiscountRate)
    expected_valuation = ExpectedValuation(npv_value, ChanceSuccess)
    value_per_dollar = ValuePerDollar(expected_valuation, ProposedValuation)
    total_profit = ProfitTotal(InvestmentAmount, value_per_dollar)
    
    st.success("✅ Results")
    st.metric(label="TAM", value=f"${TAM:,.0f}")
    st.metric(label="ARR", value=f"${arr_value:,.0f}")
    st.metric(label="NPV (100 years)", value=f"${npv_value:,.0f}")
    st.metric(label="Expected Valuation", value=f"${expected_valuation:,.0f}")
    st.metric(label="Profit per Dollar", value=f"{value_per_dollar:.2f}")
    st.metric(label="Total Profit of Investment", value=f"${total_profit:,.0f}")
