loan_id_counter = 1 #so can modify, delete

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

def calculate_debt_service_ratio(monthly_income, monthly_instalment, other_monthly_commitments): #dsr
    total_monthly_debt = monthly_instalment + other_monthly_commitments
    debt_service_ratio = total_monthly_debt / monthly_income * 100
    return debt_service_ratio

def calculate_new_loan(): # Get user inputs
    global loan_id_counter
    loan_id_counter += 1
    loan_id = loan_id_counter
    principal_amount = validate_input(input("Enter principal amount: "), float)
    annual_interest_rate = validate_input(input("Enter annual interest rate (in percentage): "), float)
    loan_term_years = validate_input(input("Enter loan term (years): "), int)
    monthly_income = validate_input(input("Enter monthly income: "), float)
    other_monthly_commitments = validate_input(input("Enter other monthly financial commitments: "), float)

    monthly_instalment = calculate_monthly_instalment(principal_amount, annual_interest_rate, loan_term_years) # Calculate monthly instalment and total payment
    total_payment = calculate_total_payment(monthly_instalment, loan_term_years)

    debt_service_ratio = calculate_debt_service_ratio(monthly_income, monthly_instalment, other_monthly_commitments) # Calculate debt service ratio

    eligible = debt_service_ratio <= 70 # Check eligibility

    print("---------------------------------------") # Display results
    print("Loan ID:", loan_id)
    print("Monthly instalment: RM {:.2f}".format(monthly_instalment))
    print("Total payment over loan term RM {:.2f}:".format(total_payment))
    print("Debt Service Ratio (DSR) {:.2f}:".format(debt_service_ratio),"%")

    loan_calculation_details = { #with loan id
    "loan_id": loan_id,
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

def view_previous_calculations(loan_calculations): #view cal
    if len(loan_calculations) == 0:
        print("No previous calculations found.")
        return

def view_previous_calculations(loan_calculations):
    if len(loan_calculations) == 0:
        print("No previous calculations found.")
        return

    print("Previous Loan Calculations:")
    print("---------------------------------------")
    for i, calculation in enumerate(loan_calculations): #enumerate : python ver of iteration (loops)
        print(f"Loan ID: {calculation['loan_id']}")
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

def modify_dsr_for_specific_loan(loan_calculations): #optional
    loan_id = validate_input(input("Enter the loan ID you want to modify: "), int)

    found_calculation = False
    for calculation in loan_calculations:
        if calculation['loan_id'] == loan_id:
            found_calculation = True
            new_dsr = validate_input(input("Enter the new DSR threshold (in percentage): "), float)
            calculation['debt_service_ratio'] = new_dsr
            print(f"DSR for loan ID {loan_id} successfully updated to {new_dsr}.")
            break

    if not found_calculation:
        print("Loan ID not found. Please enter a valid loan ID.")

def delete_specific_loan_calculation(loan_calculations):
    loan_id = validate_input(input("Enter the loan ID you want to delete: "), int)

    found_calculation = False
    for index, calculation in enumerate(loan_calculations): #python iteration loop
        if calculation['loan_id'] == loan_id:
            found_calculation = True

            while True:
                delete_confirmation = input(f"Are you sure you want to delete loan ID {loan_id}? (Y/N): ")

                if delete_confirmation.lower() == 'y' or delete_confirmation.upper() == 'Y': #making it upper and lower case acceptable
                    del loan_calculations[index]
                    print(f"Loan ID {loan_id} successfully deleted.")
                    break
                elif delete_confirmation.lower() == 'n' or delete_confirmation.upper() == 'N': #making it upper and lower case acceptable
                    print("Cancel.")
                    break
                else:
                    print("Invalid input. Please enter Y or N.")

    if not found_calculation:
        print("Loan ID not found. Please enter a valid loan ID.")
