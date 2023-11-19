import math

def calculate_monthly_installment(principal, interest_rate, loan_term):
    monthly_interest_rate = interest_rate / (12 * 100)
    number_of_payments = loan_term * 12
    monthly_installment = (principal * monthly_interest_rate) * (
        (1 + monthly_interest_rate) ** number_of_payments
    ) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    return monthly_installment

def calculate_total_payment(monthly_installment, number_of_payments):
    total_payment = monthly_installment * number_of_payments
    return total_payment

def calculate_debt_service_ratio(monthly_installment, other_commitments, monthly_income):
    total_debt_commitments = monthly_installment + other_commitments
    debt_service_ratio = total_debt_commitments / monthly_income
    return debt_service_ratio

def calculate_loan():
    principal = float(input("Enter the principal loan amount: "))
    annual_interest_rate = float(input("Enter the annual interest rate: "))
    loan_term = int(input("Enter the loan term in years: "))
    monthly_income = float(input("Enter your monthly income: "))
    other_commitments = float(input("Enter your total monthly financial commitments (excluding housing loan): "))

    # Calculate monthly installment
    monthly_installment = calculate_monthly_installment(principal, annual_interest_rate, loan_term)

    # Calculate total payment over loan term
    total_payment = calculate_total_payment(monthly_installment, loan_term * 12)

    # Calculate Debt Service Ratio (DSR)
    debt_service_ratio = calculate_debt_service_ratio(monthly_installment, other_commitments, monthly_income)

    # Check eligibility based on DSR
    if debt_service_ratio <= 0.7:
        eligibility = "Eligible"
    else:
        eligibility = "Not Eligible"

    # Display loan calculation results
    print("\nLoan Calculation Summary:")
    print("----------------------------")
    print("Principal:", principal)
    print("Annual Interest Rate:", annual_interest_rate, "%")
    print("Loan Term (Years):", loan_term)
    print("Monthly Installment:", monthly_installment, ":")
    print("Total Payment:", total_payment, ":")
    print("Debt Service Ratio:", debt_service_ratio)
    print("Eligibility:", eligibility)
    print("----------------------------")
