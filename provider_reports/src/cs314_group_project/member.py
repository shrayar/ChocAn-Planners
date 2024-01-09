# This module contains a class for storing a member's data
# Jessie Le
import json
import pandas as pd
import random
from enum import Enum
from tabulate import tabulate


class MemberStatus(Enum):
    NOT_FOUND = "Invalid Number"
    SUSPENDED = "Member suspended"
    VALIDATED = "Validated"


class Member:
    def __init__(self):
        self.full_name = ""
        self.member_number = 000000000
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = 00000
        self.suspended = 0

    def input_name(self):
        first_name = input("Please enter member's first name: ")
        last_name = input("Please enter member's last_name: ")
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

    def input_member_number(self):
        # Generate a random 8-digit number
        random_number = random.randint(100000000, 999999999)
        self.member_number = random_number
        return int(self.member_number)

    def input_full_details(self):
        self.full_name = self.input_name()
        # do the member number
        self.member_number = self.input_member_number()
        self.input_address()
        self.add_member()

    def add_member(self):
        while True:
            # Generate a new member number
            new_member_number = random.randint(100000000, 999999999)

            member_info = {
                "MemberName": self.full_name,
                "MemberID": new_member_number,
                "MemberAddress": self.street,
                "MemberCity": self.city,
                "MemberState": self.state,
                "MemberZip": self.zip,
                "Status": "Suspended" if self.suspended else "Active",
            }
            directory = "member_list.json"

            try:
                with open(directory) as file:
                    member_list = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # create an empty directory if file is empty
                member_list = []

            # Check if the new member number is unique
            if self.check_member_exist(new_member_number, member_list):
                print(
                    f"Generated member number {new_member_number} already exists. Regenerating..."
                )
                continue  # Retry
            else:
                member_list.append(member_info)
                with open(directory, "w") as file:
                    json.dump(member_list, file, indent=3)

                print(
                    f"Member '{self.full_name}' added to the directory with ID {new_member_number}."
                )
                self.search_member(new_member_number)
                break  # Exit the loop since a unique member number is found

    def search_member(self, member_number):
        # Check for valid input
        if not isinstance(member_number, int):
            error_message = "Argument must be an integer"
            raise TypeError(error_message)

        # Load the member directory
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # Check for matching member ID
        for member_info in member_list:
            if member_info["MemberID"] == member_number:
                # Check the "Status" of the member
                if member_info.get("Status") == "Suspended":
                    return MemberStatus.SUSPENDED
                else:
                    return MemberStatus.VALIDATED

        # Member ID not found in the list
        return MemberStatus.NOT_FOUND

    def check_member_exist(self, member_id, member_list):
        for member in member_list:
            if member["MemberID"] == member_id:
                return True
        return False

    def update_member_info(self):
        member_name = input(
            "Please enter the Member Full Name to update(Ex: Alex Nguyen): "
        )
        # Load the member directory
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return
        # Check for matching member name and ID
        for member_info in member_list:
            if member_info["MemberName"] == member_name:
                self.display_name_match(member_name)
                options = {
                    "UPDATE MEMBER MENU": [
                        "Options",
                        "1. Update Member Name",
                        "2. Update Member Address",
                        "3. Update Member ID",
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
                choice = input("Please enter your choice: ")
                print(choice)  # just checking output

                # Check if the input is a number
                if not choice.isnumeric() or (int(choice) not in [1, 2, 3, 4]):
                    print("Entered invalid option! Please try again!")
                    return self.update_member_info()
                else:
                    if int(choice) == 1:
                        self.update_full_name(member_name)
                    elif int(choice) == 2:
                        self.update_address(member_name)
                    elif int(choice) == 3:
                        self.update_member_number(member_name)
                    else:
                        print("No Information Change!")
                    break
        else:
            print(
                f"Error: Member with Name '{member_name}' not found in the directory."
            )

    def update_full_name(self, match_name):
        new_lname = input("Please enter an update last name: ")
        new_fname = input("Please enter an update first name: ")
        # need to check for invalid input too!!!
        new_name = new_fname + " " + new_lname

        # Load the member directory
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # check for matching member ID
        for member_info in member_list:
            if member_info["MemberName"] == match_name:
                # Update the member's name
                member_info["MemberName"] = new_name
                break

        with open(directory, "w") as file:
            json.dump(member_list, file, indent=3)
            print(f"Member '{match_name}' updated with new name: {new_name}")
        return

    def update_address(self, member_name):
        new_street = input("Please enter an updated street address: ")
        new_city = input("Please enter an updated city: ")
        new_state = input("Please enter an updated state: ")
        new_zip = input("Please enter an updated ZIP code: ")

        # Load the member directory
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        for member_info in member_list:
            if member_info["MemberName"] == member_name:
                # Update the member's address
                member_info["MemberAddress"] = new_street
                member_info["MemberCity"] = new_city
                member_info["MemberState"] = new_state
                if isinstance(new_zip, int) and len(str(new_zip)) == 5:
                    member_info["MemberZip"] = int(new_zip)
                else:
                    member_info["MemberZip"] = member_info["MemberZip"]
                break

        # Save the updated directory back to the file
        with open(directory, "w") as file:
            json.dump(member_list, file, indent=3)

        # print(f"Error: Member with ID {self.member_number} not found in the directory.")

    def update_member_number(self, match_name):
        new_member_number = input("Please enter the new member ID: ")
        # Validity check for the new member number
        if isinstance(new_member_number, int) and len(str(new_member_number)) == 9:
            new_member_number = int(new_member_number)
        else:
            print("Invalid member number format. Please enter a 9-digit number.")
            return

        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return
        for member_info in member_list:  # matching
            if member_info["MemberName"] == match_name:
                # Check if the new member number is unique
                if any(
                    member["MemberID"] == new_member_number for member in member_list
                ):
                    print("Error: The new member number is not unique.")
                    return
                member_info["MemberID"] = new_member_number
        with open(directory, "w") as file:
            json.dump(member_list, file, indent=3)
            print(f"Member '{match_name}' updated with new number: {new_member_number}")
        return

    def get_name(self, match_name):
        directory = "member_list.json"

        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return None

        # Check for the member ID
        for member_info in member_list:
            if member_info["MemberName"] == match_name:
                self.display_match(member_info["MemberID"])
                return member_info
        return None

    def remove_member(self):
        name_remove = input(
            "Please enter the member name that you want to remove(Ex: Alex Nguyen): "
        )
        member_info = self.get_name(name_remove)
        if member_info:
            # Member found, you can proceed with removal
            directory = "member_list.json"
            try:
                with open(directory) as file:
                    member_list = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                print("Error: Member directory not found or empty.")
                return

            # Use list comprehension to filter out the member to be removed
            member_list = [
                member for member in member_list if member["MemberName"] != name_remove
            ]

            with open(directory, "w") as file:
                json.dump(member_list, file, indent=3)

            print(f"Member with name {name_remove} removed from the directory.")
        else:
            print(f"Member with name {name_remove} not found in the directory.")

    def display_members(self):
        # Load the member directory
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # Check if the directory is empty
        if not member_list:
            print("Member directory is empty.")
            return
        headers = [
            "Member ID",
            "Member Name",
            "Member Address",
            "City",
            "State",
            "ZIP",
            "Services",
            "Status",
        ]
        rows = []
        for member_info in member_list:
            member_id = member_info["MemberID"]
            member_name = member_info["MemberName"]
            member_address = member_info["MemberAddress"]
            member_city = member_info["MemberCity"]
            member_state = member_info["MemberState"]
            member_zip = member_info["MemberZip"]
            services = member_info.get("Services", [])
            status = member_info.get("Status", "")

            rows.append(
                [
                    member_id,
                    member_name,
                    member_address,
                    member_city,
                    member_state,
                    member_zip,
                    services,
                    status,
                ]
            )

        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

    def display_match(self, match_id):
        directory = "member_list.json"

        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # Check for the member ID
        for member_info in member_list:
            if member_info["MemberID"] == match_id:
                headers = [
                    "Member ID",
                    "Member Name",
                    "Member Address",
                    "City",
                    "State",
                    "ZIP",
                    "Services",
                    "Status",
                ]
                member_data = [
                    [
                        member_info["MemberID"],
                        member_info["MemberName"],
                        member_info["MemberAddress"],
                        member_info["MemberCity"],
                        member_info["MemberState"],
                        member_info["MemberZip"],
                        member_info.get("Services", []),
                        member_info.get("Status", ""),
                    ]
                ]
                print(tabulate(member_data, headers=headers, tablefmt="fancy_grid"))
                return

        print(f"Member with ID {match_id} not found in the directory.")

    def display_name_match(self, match_name):
        directory = "member_list.json"
        try:
            with open(directory) as file:
                member_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: Member directory not found or empty.")
            return

        # Check for the member ID
        for member_info in member_list:
            if member_info["MemberName"] == match_name:
                headers = [
                    "Member ID",
                    "Member Name",
                    "Member Address",
                    "City",
                    "State",
                    "ZIP",
                    "Services",
                    "Status",
                ]
                member_data = [
                    [
                        member_info["MemberID"],
                        member_info["MemberName"],
                        member_info["MemberAddress"],
                        member_info["MemberCity"],
                        member_info["MemberState"],
                        member_info["MemberZip"],
                        member_info.get("Services", []),
                        member_info.get("Status", ""),
                    ]
                ]
                print(tabulate(member_data, headers=headers, tablefmt="fancy_grid"))
                return

        print(f"Member with name {match_name} not found in the directory.")
