import housing_loan_calculator as hlc

loan_calculations = []

while True:
    print("Welcome to the Housing Loan Calculator")
    print("---------------------------------------")
    print("Please select an option:")
    print("1. Calculate new loan")
    print("2. View previous calculations")
    print("3. Modify DSR threshold")
    print("4. Delete previous calculations")
    print("5. Exit")

    option = hlc.validate_input(input("Enter your choice: "), int)

    if option == 1:
        # Calculate new loan
        loan_calculations.append(hlc.calculate_new_loan())
        print("Loan calculation successfully added.")

    elif option == 2:
        # View previous calculations
        hlc.view_previous_calculations(loan_calculations)

    elif option == 3:
        # Modify DSR threshold
        hlc.modify_dsr_threshold()

    elif option == 4:
        # Delete previous calculations
        hlc.delete_previous_calculations(loan_calculations)

    elif option == 5:
        # Exit
        print("Thank you for using the Housing Loan Calculator.")
        break

    else:
        print("Invalid option. Please enter a valid choice.")
