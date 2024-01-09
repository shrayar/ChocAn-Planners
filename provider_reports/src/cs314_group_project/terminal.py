# This file is for the base terminal class.  Common methods between the provider
# and manager terminal classes should be put here
import pandas as pd
from tabulate import tabulate

from cs314_group_project.manager_terminal import Manager
from cs314_group_project.provider_terminal import ProviderTerm


class Terminal:
    def __init__(self):
        self.type = ""

    def get_input_type(self):
        options = {
            "WELCOME TO CHOCAN!": ["Options"],
            "Welcome, Provider!": "1. If you are a Provider",
            "Welcome, Manager!": "2. If you are a Manager",
            "Goodbye!": "3. Quit",
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
            return self.get_input_type()
        else:
            return int(choice)

    # function to assign type
    def assign_type(self, choice):
        if choice == 1:
            self.type = "Provider"
        elif choice == 2:
            self.type = "Manager"
        elif choice == 3:
            self.type = "Quit"
        else:
            self.type = None
        return self.type

    # started to look into the derive classes
    def retrieve_type(self):
        choice = self.get_input_type()
        while choice != 3:
            self.assign_type(choice)
            if self.type == "Provider":
                provider = ProviderTerm()
                provider.login()
            else:
                manager = Manager()
                manager.login()
            choice = self.get_input_type()

    # Request the provider directory
    def request_prov_direc(self):
        pass
