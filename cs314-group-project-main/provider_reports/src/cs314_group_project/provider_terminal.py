# Provider Terminal inherits from the base terminal
import json
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timezone
from cs314_group_project.member import MemberStatus
from cs314_group_project.services import Records


# from enum import Enum
from cs314_group_project.member import Member  # , MemberStatus

# from provider import Provider


class ProviderTerm:
    def __init__(self):
        self.provider_number = 000000000
        self.provider_name = ""

    def login(self):
        # Go through provider list and check for ID
        # Load the provider list
        directory = "provider_list.json"
        try:
            with open(directory) as file:
                provider_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # If found, return true
        # If it's not found, allow them to try again until they give up
        while True:
            # Get user input
            user_input = input(
                "Please enter your provider ID (or type 'quit' to exit): "
            )

            # Check for quit option
            if user_input.lower() == "quit":
                print("Exiting the search.")
                break

            try:
                provider_id = int(user_input)

                # Search for the Provider ID in the data
                for provider in provider_list:
                    if provider["ProviderID"] == provider_id:
                        print(
                            f"\n*************** Welcome {provider['ProviderName']} ****************\n"
                        )
                        self.provider_number = provider_id
                        self.provider_name = provider["ProviderName"]
                        self.provider_menu()
                        return True

                # If Provider ID not found
                print("\nProvider ID not found.  Please try again.")

            except ValueError:
                # Handle invalid input
                print(
                    "Invalid input. Please enter a valid number or type 'quit' to exit."
                )

    # Displays the list of options for the provider's terminal
    def option_menu(self):
        options = {
            "Please choose from the following list of options": [
                "1. Authenticate member",
                "2. Create a visit record",
                "3. Request provider directory",
                "4. Quit",
            ]
        }
        df = pd.DataFrame(options)
        df_styled = df.style.set_table_styles(
            [{"selector": "th", "props": [("text-align", "center")]}]
        ).set_properties(**{"text-align": "left"})
        print(
            tabulate(
                df_styled.data,
                headers=df_styled.columns,
                tablefmt="fancy_grid",
                showindex=False,
            )
        )
        choice = int(input("Please enter your choice: "))
        return choice

    # Get input put until they're done
    # Not to be confused with the provider_menu in the manager_terminal which is
    # used for editing the provider list
    def provider_menu(self):
        choice = 0
        while choice != 4:
            choice = self.option_menu()
            match choice:
                case 1:
                    # Authenticate a member
                    member_number, member_status = self.authenticate_member()
                    print(member_number)
                    # This is sloppy. Just using the thing
                    if member_status:
                        print()
                case 2:
                    print("Creating visit record...")
                    self.bill_choc_an()
                case 3:
                    # Request the provider directory as an email attachment
                    self.request_prov_dir()
                case 4:
                    print("Have a nice day.")
            if choice >= 5:
                print("Invalid choice!")

    def authenticate_member(self):
        member = Member()  # Create a member object to use the search member function

        while True:
            member_number_input = input(
                "Please enter the member number (or type 'quit' to exit): "
            )

            if member_number_input.lower() == "quit":
                print("Exiting authentication.")
                return  # Exit the loop and function

            try:
                member_number = int(member_number_input)
                member_status = member.search_member(member_number)

                # Check the status of the member
                if member_status == MemberStatus.NOT_FOUND:
                    print("\n")
                    print(member_status.value)
                    print("\n")
                else:
                    print("\n")
                    print(member_status.value)
                    print("\n")

                return member_number, member_status

            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except TypeError as e:
                print(e)

    def request_prov_dir(self):
        # Path to the provider_directory.json file
        json_file_path = "provider_directory.json"

        # Path to the provider_directory.txt file
        txt_file_path = "provider_directory.txt"

        # Read the JSON file
        with open(json_file_path) as json_file:
            provider_directory = json.load(json_file)

        # Write the contents to a txt file
        with open(txt_file_path, "w") as txt_file:
            # Formatting the output
            for service in provider_directory:
                txt_file.write(json.dumps(service, indent=4))
                txt_file.write("\n\n")

        print(
            "\nPlease check your email for an attachment titled 'provider_directory.txt."
        )
        print(
            "(If you are grading this, look in the src/cs314_group_project directory.)\n"
        )

    # Generate a billing record that is written to disk
    def create_visit_record(self):
        # this should go in services.py
        pass

    def bill_choc_an(self):
        record = Records()

        # Authenticate the member
        member_number, member_status = self.authenticate_member()
        provider_number = self.provider_number

        # Check again that the member is valid
        if member_status in [MemberStatus.SUSPENDED, MemberStatus.NOT_FOUND]:
            print("Cannot complete billing process.")
            return

        # Get the date of service
        date_of_service = input("Please enter the date the service was provided: ")

        # Get the six-digit code
        service_code = self.get_and_verify_code()

        # Get the comments
        comment = input("\nPlease enter any comments about the visit: ")

        # Get the current date and time, and format it as a string
        date_recorded = datetime.now(timezone.utc).strftime("%m-%d-%Y %H:%M:%S")

        # Generate the visit record
        record.create_visit_record(
            date_recorded,
            date_of_service,
            provider_number,
            member_number,
            service_code,
            comment,
        )

        # For billing purposes, generate the eft report
        provider_name = self.provider_name
        price = record.find_price_by_code(service_code)  # Get the price of the service

        record.generate_eft_record(provider_name, provider_number, price)

    def get_and_verify_code(self):
        record = Records()
        service_code = 0

        response = "no"
        while response == "no":
            self.request_prov_dir()
            service_code = int(
                input(
                    "Please look for the correct 6-six service code corresponding to "
                    "the service provided and enter it here: "
                )
            )

            service_name = record.find_service_by_code(service_code)

            if service_name == "Service not found":
                response = "no"
            else:
                print("The service we found corresponding to that code is: \n")
                print(service_name)
                response = input("\nIs this correct? Enter 'yes' or 'no': ")

        return service_code
