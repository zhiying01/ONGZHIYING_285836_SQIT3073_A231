import calculate_loan

def main_menu():
    print("Housing Loan Calculator")
    print("------------------------")
    print("1. Calculate New Loan")
    print("2. Display Previous Calculations")
    print("3. Exit")
    print("------------------------")

    option = int(input("Enter your choice: "))

    if option == 1:
        calculate_loan.calculate_loan()
    elif option == 2:
        print("Display previous calculations")
    elif option == 3:
        exit()
    else:
        print("Invalid option. Please enter a valid choice (1-3).")
        main_menu()

if __name__ == "__main__":
    main_menu()
