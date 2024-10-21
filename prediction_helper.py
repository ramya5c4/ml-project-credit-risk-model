import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

model_path = "D:\\ML\\project\\credit_modeling.joblib"
model_data = joblib.load(model_path)

# Extract the model and scaler
model = model_data['model']
scaler = model_data['scaler']
col_to_scale = model_data['col_to_scale']
features = model_data['features']

def prepare_df(age,income,loan_amount,loan_tenure_months,deliquent_loan_months,
                                                Average_DPD,credit_utilization_ratio,number_of_open_accounts,
                                                residence_type,loan_purpose,loan_type):
    input_data = {
        "number_of_open_accounts": number_of_open_accounts,
        "credit_utilization_ratio": credit_utilization_ratio,
        "age": age,
        "loan_tenure_months": loan_tenure_months,
        "deliquent_loan_months": deliquent_loan_months,
        "Average_DPD": Average_DPD,
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,
        "number_of_closed_accounts":1,
        "enquiry_count":1,
        "years_at_current_address":1,
        "zipcode":1,
        "sanction_amount":1,
        "processing_fee":1,
        "gst":1,
        "net_disbursement":1,
        "principal_outstanding":1,
        "bank_balance_at_application":1,
        "credit_utilization_per_income":1,
        'number_of_dependants': 1,
        'loan_to_income': loan_amount / income if income > 0 else 0

    }

    input_df = pd.DataFrame([input_data],index=[0])
    input_df[col_to_scale] = scaler.transform(input_df[col_to_scale])
    df=input_df[features]


    return df


def calculate_credit_score(input_df,base_score=300,scale_length=600):
     x=np.dot(input_df.values,model.coef_.T)+model.intercept_
     default_probability = 1 / (1 + np.exp(-x))

     non_default_probability = 1 - default_probability

     # Convert the probability to a credit score, scaled to fit within 300 to 900
     credit_score = base_score + non_default_probability.flatten() * scale_length

     # Determine the rating category based on the credit score
     def get_rating(score):
         if 300 <= score < 500:
             return 'Poor'
         elif 500 <= score < 650:
             return 'Average'
         elif 650 <= score < 750:
             return 'Good'
         elif 750 <= score <= 900:
             return 'Excellent'
         else:
             return 'Undefined'  # in case of any unexpected score
     rating = get_rating(credit_score[0])

     return default_probability.flatten()[0], int(credit_score[0]), rating

def predict(age, income, loan_amount, loan_tenure_months, deliquent_loan_months,
                Average_DPD, credit_utilization_ratio, number_of_open_accounts,
                residence_type, loan_purpose, loan_type):
    input_df=prepare_df(age, income, loan_amount, loan_tenure_months, deliquent_loan_months,
                Average_DPD, credit_utilization_ratio, number_of_open_accounts,
                residence_type, loan_purpose, loan_type)

    default_probability,credit_score,rating=calculate_credit_score(input_df)


    return default_probability,credit_score,rating
