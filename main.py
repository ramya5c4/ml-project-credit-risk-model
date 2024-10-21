import streamlit as st
from prediction_helper import predict
st.title("Louki Finance:Credit risk modeling")


row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)


with row1[0]:
    age = st.number_input("Age",min_value=18,max_value=100,step=1)
with row1[1]:
    income = st.number_input("Income",min_value=0,value=120000)
with row1[2]:
    loan_amount = st.number_input("Loan amount",min_value=0, value=250000)


with row2[0]:
    if income > 0:
        loan_to_income_ratio = loan_amount / income
    else:
        loan_to_income_ratio = 0.0

    st.text(f"Loan-to-Income Ratio:{loan_to_income_ratio:.2f}")
with row2[1]:
    loan_tenure_months = st.number_input("Loan Tenure (Months)", min_value=0,max_value=100, value=36, step=1)

with row2[2]:
    deliquent_loan_months = st.number_input("Delinquent Loan Months", min_value=0, max_value=100, value=30)



with row3[0]:
    Average_DPD = st.number_input("Average Days Past Due", min_value=0, step=1,value=20)

with row3[1]:
    credit_utilization_ratio = st.number_input("Credit Utilization Ratio", min_value=0, max_value=100,value=30, step=1)

with row3[2]:
    number_of_open_accounts = st.number_input("Number of Open Accounts", min_value=1,max_value=4, step=1,value=2)


with row4[0]:
    residence_type = st.selectbox("Residence Type", ['Owned', 'Mortgage', 'Rented'])

with row4[1]:
    loan_purpose = st.selectbox("Loan Purpose", ['Home', 'Education', 'Personal', 'Auto'])

with row4[2]:
    loan_type = st.selectbox("Loan Type", ['Secured', 'Unsecured'])


if st.button("Caluculate Risk"):
    default_probability,credit_score,rating = predict(age,income,loan_amount,loan_tenure_months,deliquent_loan_months,
                                                Average_DPD,credit_utilization_ratio,number_of_open_accounts,
                                                residence_type,loan_purpose,loan_type)
    st.write(f"Default probability: {default_probability:.2%}")
    st.write(f"Credit_score: {credit_score}")
    st.write(f"Rating:{rating}")
