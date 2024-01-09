# This module contains a class for storing a provider's data
import json
import random

import pandas as pd
from tabulate import tabulate


class Provider:
    def __init__(self):
        self.full_name = ""
        self.provider_number = 000000000
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = 00000

    def input_name(self):
        first_name = input("Please enter provider's first name: ")
        last_name = input("Please enter provider's last_name: ")
        # check for first name and last name error
        if first_name.isalpha() is True and last_name.isalpha() is True:
            self.full_name = first_name + " " + last_name
            return self.full_name
        else:
            print("Invalid input name format! Please try again!\n")
            return self.input_name()

    def input_address(self):
        street = input("Please enter the street address: ")
        city = input("Please enter the city: ")
        state = input("Please enter the state: ")
        zip_code = input("Please enter the ZIP code: ")

        # Check for valid address format
        # MISSING: need to check for individual input too!!!
        if (
            street
            and city
            and state
            and isinstance(zip_code, int)
            and len(str(zip_code)) == 5
        ):
            self.street = street
            self.city = city
            self.state = state
            self.zip = int(zip_code)
        else:
            print("Invalid input address format! Please try again!\n")
            return self.input_address()

    def input_provider_number(self):
        # Generate a random 8-digit number
        random_number = random.randint(100000000, 999999999)
        self.provider_number = random_number
        # return int(self.provider_number)

    def input_full_details(self):
        self.full_name = self.input_name()
        # do the provider number
        self.input_provider_number()
        self.input_address()
        self.add_provider()

    def add_provider(self):
        provider_info = {
            "ProviderName": self.full_name,
            "ProviderID": self.provider_number,
            "ProviderAddress": self.street,
            "ProviderCity": self.city,
            "ProviderState": self.state,
            "ProviderZip": self.zip,
        }
        directory = "provider_list.json"

        try:
            # Load existing directory if it exists
            with open(directory) as file:
                provider_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, create an empty directory
            provider_list = []

        # Add the new provider to the directory
        provider_list.append(provider_info)

        # Save the updated directory back to the file
        with open(directory, "w") as file:
            json.dump(provider_list, file, indent=3)

        print(f"Provider '{self.full_name}' added to the directory.")

    def update_provider_info(self):
        options = {
            "UPDATE provider MENU": [
                "Options",
                "1. Update Provider Name",
                "2. Update Provider Address",
                "3. Quit",
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
        choice = input("Please enter your choice: ")
        print(choice)  # just checking output

        # check if the input is a number
        if choice.isnumeric() is False or (
            int(choice) != 1 and int(choice) != 2 and int(choice) != 3
        ):
            print("Entered invalid option! Please try again!")
            return self.update_provider_info()
        elif int(choice) == 1:
            self.update_full_name()
        elif int(choice) == 2:
            self.update_address()
        else:
            print("No Information Change!")

    def update_full_name(self):
        new_lname = input("Please enter an update last name: ")
        new_fname = input("Please enter an update first name: ")
        new_name = new_fname + " " + new_lname  # need to check for invalid input too!!!

        # Load the provider directory
        directory = "provider_list.json"
        try:
            with open(directory) as file:
                provider_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Provider directory not found or empty.")
            return

        # check for matching provider ID
        for provider_info in provider_list:
            if provider_info["ProviderID"] == self.provider_number:
                # Update the provider's name
                provider_info["ProviderName"] = new_name

                with open(directory, "w") as file:
                    json.dump(provider_list, file, indent=3)

                print(f"Provider '{self.full_name}' updated with new name: {new_name}")
                return

        # If the provider with the given ProviderID is not found
        print(
            f"Error: Provider with ID {self.provider_number} not found in the directory."
        )

    def update_address(self):
        new_street = input("Please enter an updated street address: ")
        new_city = input("Please enter an updated city: ")
        new_state = input("Please enter an updated state: ")
        new_zip = input("Please enter an updated ZIP code: ")

        # Load the provider directory
        directory = "provider_list.json"
        try:
            with open(directory) as file:
                provider_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Provider directory not found or empty.")
            return

        # Check for matching provider ID
        for provider_info in provider_list:
            if provider_info["ProviderID"] == self.provider_number:
                # Update the provider's address
                provider_info["ProviderAddress"] = new_street
                provider_info["ProviderCity"] = new_city
                provider_info["ProviderState"] = new_state
                if isinstance(new_zip, int) and len(str(new_zip)) == 5:
                    provider_info["ProviderZip"] = int(new_zip)
                else:
                    provider_info["ProviderZip"] = provider_info["ProviderZip"]
                break
            # Save the updated directory back to the file
            with open(directory, "w") as file:
                json.dump(provider_list, file, indent=3)

            print(f"Address for Provider '{self.full_name}' updated.")
            return

        print(
            f"Error: Provider with ID {self.provider_number} not found in the directory."
        )

    def display_providers(self):
        # Load the provider directory
        directory = "provider_list.json"
        try:
            with open(directory) as file:
                provider_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Provider directory not found or empty.")
            return

        # Check if the directory is empty
        if not provider_list:
            print("Provider directory is empty.")
            return

        # Display the providers in a tabular format
        headers = [
            "Provider ID",
            "Provider Name",
            "Provider Address",
            "City",
            "State",
            "ZIP",
        ]
        rows = []
        for provider_info in provider_list:
            provider_id = provider_info["ProviderID"]
            provider_name = provider_info["ProviderName"]
            provider_address = provider_info["ProviderAddress"]
            provider_city = provider_info["ProviderCity"]
            provider_state = provider_info["ProviderState"]
            provider_zip = provider_info["ProviderZip"]

            rows.append(
                [
                    provider_id,
                    provider_name,
                    provider_address,
                    provider_city,
                    provider_state,
                    provider_zip,
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
