# Manger Terminal inherits from the base terminal
import pandas as pd
from tabulate import tabulate

from cs314_group_project.member import Member
from cs314_group_project.provider import Provider
from cs314_group_project.services import Records


class Manager:
    def __init__(self):
        pass

    # Unfortunately for the manager, their account has no security
    # (since we don't have manager id numbers)
    def login(self):
        self.manager_menu()

    def report_menu(self):
        options = {
            "REPORT'S MENU!": [
                "Options",
                "1. Member Weekly Reports",
                "2. Provider Weekly Reports",
                "3. EFT Reports",
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
        return int(choice)

    def member_menu(self):
        options = {
            "MEMBER'S MENU!": [
                "Options",
                "1. Add a member",
                "2. Remove a member",
                "3. Update Member Records",
                "4. Display Member Lists",
                "5. Quit",
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
        if not choice.strip():
            print("Entered invalid option! Please try again!")
            return self.member_menu()

        # Check if the input is a number
        if not choice.isnumeric() or int(choice) not in range(1, 6):
            print("Entered invalid option! Please try again!")
            return self.member_menu()
        return int(choice)

    def provider_menu(self):
        options = {
            "PROVIDER'S MENU!": [
                "Options",
                "1. Add a provider",
                "2. Remove a provider",
                "3. Update Provider Records",
                "4. Display Provider Lists",
                "5. Quit",
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
        return int(choice)

    def serivce_menu(self):
        options = {
            "SERVICE'S MENU!": [
                "Options",
                "1. Add a service",
                "2. Remove a service",
                "3. Update Service Records",
                "4. Display Service Lists",
                "5. Quit",
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
        return int(choice)

    def option_menu(self):
        options = {
            "THIS IS THE MAIN MENU!": [
                "Options",
                "1. Generate reports",
                "2. Modify Members",
                "3. Modify Providers",
                "4. Modify Services",
                "5. Quit",
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
        while True:
            choice = input("Please enter your choice: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            else:
                print("Invalid input. Please enter a numeric value.")

    def manager_menu(self):
        # check for option
        choice = 0
        while choice != 5:
            choice = self.option_menu()
            match choice:
                case 1:
                    response = 0
                    while response != 4:
                        record = Records()
                        response = self.report_menu()

                        if response == 1:
                            record.generate_member_service_report()
                        elif response == 2:
                            record.generate_provider_service_report()
                        elif response == 3:
                            record.create_eft_report()
                        elif response == 4:
                            print("Returning to main menu...")
                        else:
                            print("Entered invalid option! Please enter again!")
                            continue
                    print("\n")

                case 2:
                    member = Member()
                    response = 0
                    while response != 5:
                        response = self.member_menu()
                        # do the if-else statement to call the function in member class
                        if response == 1:
                            member.input_full_details()
                        elif response == 2:
                            member.remove_member()
                        elif response == 3:
                            member.update_member_info()
                        elif response == 4:
                            member.display_members()
                        elif response == 5:
                            print("Returning to main menu...")
                        else:
                            print("Entered invalid option! Please enter again!")
                            continue
                    print("\n")
                case 3:
                    provider = Provider()
                    response = 0
                    while response != 5:
                        response = self.provider_menu()
                        # do the if-else statement to call the function in provider class
                        if response == 1:
                            provider.input_full_details()
                        elif response == 2:
                            print("Remove a provider is not implemented yet!")
                            continue
                        elif response == 3:
                            provider.update_provider_info()
                        elif response == 4:
                            provider.display_providers()
                        elif response == 5:
                            print("Returning to main menu...")
                        else:
                            print("Entered invalid option! Please enter again!")
                            continue
                case 4:
                    self.service_menu()
                case 5:
                    print("Thank you for using our program!")
            if choice >= 6:
                print("Invalid choice!")
