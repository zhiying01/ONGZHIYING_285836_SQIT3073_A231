def validate_input(input_value, input_type):
    while True:
        try:
            value = input_type(input_value)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Invalid input. Please enter a positive value.")
            input_value = input()

def calculate_monthly_instalment(principal_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    loan_term_months = loan_term_years * 12
    monthly_payment = principal_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    return monthly_payment

def calculate_total_payment(monthly_payment, loan_term_months):
    total_payment = monthly_payment * loan_term_months
    return total_payment

def calculate_debt_service_ratio(monthly_income, monthly_instalment, other_monthly_commitments):
    total_monthly_debt = monthly_instalment + other_monthly_commitments
    debt_service_ratio = total_monthly_debt / monthly_income * 100
    return debt_service_ratio

def calculate_new_loan():
    # Get user inputs
    principal_amount = validate_input(input("Enter principal amount: "), float)
    annual_interest_rate = validate_input(input("Enter annual interest rate (percentage): "), float)
    loan_term_years = validate_input(input("Enter loan term (years): "), int)
    monthly_income = validate_input(input("Enter monthly income: "), float)
    other_monthly_commitments = validate_input(input("Enter other monthly financial commitments: "), float)

    # Calculate monthly instalment and total payment
    monthly_instalment = calculate_monthly_instalment(principal_amount, annual_interest_rate, loan_term_years)
    total_payment = calculate_total_payment(monthly_instalment, loan_term_years)

    # Calculate debt service ratio
    debt_service_ratio = calculate_debt_service_ratio(monthly_income, monthly_instalment, other_monthly_commitments)

    # Check eligibility
    eligible = debt_service_ratio <= 70

    # Display results
    print("---------------------------------------")
    print("Monthly instalment: RM {:.2f}".format(monthly_instalment))
    print("Total payment over loan term RM {:.2f}:".format(total_payment))
    print("Debt Service Ratio (DSR) {:.2f}:".format(debt_service_ratio),"%")

    if eligible:
        print("You are eligible for the loan.")
    else:
        print("You are not eligible for the loan. Your DSR exceeds the 70% threshold.")

    # Return loan calculation details
    loan_calculation_details = {
        "principal_amount": principal_amount,
        "annual_interest_rate": annual_interest_rate,
        "loan_term_years": loan_term_years,
        "monthly_income": monthly_income,
        "other_monthly_commitments": other_monthly_commitments,
        "monthly_instalment": monthly_instalment,
        "total_payment": total_payment,
        "debt_service_ratio": debt_service_ratio,
        "eligible": eligible
    }

    return loan_calculation_details

def view_previous_calculations(loan_calculations):
    if len(loan_calculations) == 0:
        print("No previous calculations found.")
        return

    print("Previous Loan Calculations:")
    print("---------------------------------------")
    for calculation in loan_calculations:
        print("Principal Amount:", calculation['principal_amount'])
        print("Annual Interest Rate:", calculation['annual_interest_rate'])
        print("Loan Term (Years):", calculation['loan_term_years'])
        print("Monthly Income:", calculation['monthly_income'])
        print("Other Monthly Commitments:", calculation['other_monthly_commitments'])
        print("Monthly Instalment:", calculation['monthly_instalment'])
        print("Total Payment:", calculation['total_payment'])
        print("Debt Service Ratio (DSR):", calculation['debt_service_ratio'])
        print("Eligible:", calculation['eligible'])
        print("---------------------------------------")

def modify_dsr_threshold():
    global dsr_threshold

    current_dsr_threshold = dsr_threshold
    new_dsr_threshold = validate_input(input(f"Current DSR threshold is {current_dsr_threshold}. Enter a new threshold (percentage): "), float)

    if new_dsr_threshold != current_dsr_threshold: #edit the new dsr
        dsr_threshold = new_dsr_threshold
        print(f"DSR threshold successfully updated to {new_dsr_threshold}.")
    else:
        print("DSR threshold remains unchanged.")

def delete_previous_calculations(loan_calculations):
    if len(loan_calculations) == 0:
        print("No previous calculations found.")
        return

    print("Delete Previous Calculations:")
    print("---------------------------------------")
    for i, calculation in enumerate(loan_calculations):
        print("Principal Amount:", calculation['principal_amount'])
        print("Annual Interest Rate:", calculation['annual_interest_rate'])
        print("Loan Term (Years):", calculation['loan_term_years'])
        print("Monthly Income:", calculation['monthly_income'])
        print("Other Monthly Commitments:", calculation['other_monthly_commitments'])
        print("Monthly Instalment:", calculation['monthly_instalment'])
        print("Total Payment:", calculation['total_payment'])
        print("Debt Service Ratio (DSR):", calculation['debt_service_ratio'])
        print("Eligible:", calculation['eligible'])
        print("---------------------------------------")

    delete_choice = input("Enter the loan ID of the calculation you want to delete: ")
    try:
        delete_index = int(delete_choice)
        del loan_calculations[delete_index]
        print("Loan calculation successfully deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid loan ID.")
