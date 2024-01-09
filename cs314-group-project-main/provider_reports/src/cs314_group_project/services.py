import json
import os


class Records:
    def __init__(self):
        self.visit_records = []
        self.billing_records = []

    def create_visit_record(
        self,
        date_recorded,
        date_of_service,
        provider_id,
        member_id,
        service_code,
        comment,
    ):
        # Load the visit records directory
        directory = "visit_records.json"

        # Read the existing data from the file
        try:
            with open(directory) as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Create a new record
        new_record = {
            "DateRecorded": date_recorded,
            "DateOfService": date_of_service,
            "ProviderID": provider_id,
            "MemberID": member_id,
            "ServiceCode": service_code,
            "Comment": comment,
        }

        # Append the new record to the data
        data.append(new_record)

        # Write the updated data back to the file
        with open(directory, "w") as file:
            json.dump(data, file, indent=4)

    def generate_eft_record(self, provider_name, provider_number, amount):
        # Load the eft records directory
        directory = "eft_records.json"

        # Read the existing data from the file
        try:
            with open(directory) as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        new_record = {
            "ProviderName": provider_name,
            "ProviderID": provider_number,
            "Amount": amount,
        }
        # Append the new record to the data
        data.append(new_record)

        # Write the updated data back to the file
        with open(directory, "w") as file:
            json.dump(data, file, indent=4)

    def find_service_by_code(self, service_code):
        directory = (
            "provider_directory.json"  # Path to the provider directory JSON file
        )

        # Read the provider directory from the JSON file
        try:
            with open(directory) as file:
                services = json.load(file)
        except FileNotFoundError:
            print("Provider directory file not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")
            return None

        # Search for the service with the given code
        for service in services:
            if service["ServiceCode"] == service_code:
                return service["ServiceName"]

        # If service code not found
        return "Service not found"

    def find_price_by_code(self, service_code):
        directory = (
            "provider_directory.json"  # Path to the provider directory JSON file
        )

        # Read the provider directory from the JSON file
        try:
            with open(directory) as file:
                services = json.load(file)
        except FileNotFoundError:
            print("Provider directory file not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")
            return None

        # Search for the service with the given code
        for service in services:
            if service["ServiceCode"] == service_code:
                return service["ServiceFee"]

        # If service code not found
        return 0.00

    def generate_member_service_report(self):
        # Load visit records, member list, provider list, and provider directory
        with open("visit_records.json") as file:
            visit_records = json.load(file)
        with open("member_list.json") as file:
            member_list = json.load(file)
        with open("provider_list.json") as file:
            provider_list = json.load(file)
        with open("provider_directory.json") as file:
            provider_directory = json.load(file)

        # Convert lists to dictionaries for faster lookup
        members = {member["MemberID"]: member for member in member_list}
        providers = {provider["ProviderID"]: provider for provider in provider_list}
        services = {service["ServiceCode"]: service for service in provider_directory}

        # Directory to store the generated reports
        output_directory = "member_reports"
        os.makedirs(output_directory, exist_ok=True)

        # Process each visit record
        for visit in visit_records:
            member_id = visit["MemberID"]
            member_info = members.get(member_id)
            provider_info = providers.get(visit["ProviderID"])
            service_info = services.get(visit["ServiceCode"])

            if member_info and provider_info and service_info:
                file_name = f"{member_info['MemberName'].replace(' ', '_')}.txt"
                file_path = os.path.join(output_directory, file_name)

                # Check if this is the first visit for the member
                first_visit = not os.path.exists(file_path)

                with open(file_path, "a") as file:
                    if first_visit:
                        # Write member info only for the first visit
                        file.write("Member Name: " + member_info["MemberName"] + "\n")
                        file.write(
                            "Member Number: " + str(member_info["MemberID"]) + "\n"
                        )
                        file.write(
                            "Member Address: " + member_info["MemberAddress"] + "\n"
                        )
                        file.write("Member City: " + member_info["MemberCity"] + "\n")
                        file.write("Member State: " + member_info["MemberState"] + "\n")
                        file.write(
                            "Member Zip: " + str(member_info["MemberZip"]) + "\n\n"
                        )

                    # Write visit info for every visit
                    file.write("Date of Service: " + visit["DateOfService"] + "\n")
                    file.write("Provider Name: " + provider_info["ProviderName"] + "\n")
                    file.write("Service Name: " + service_info["ServiceName"] + "\n")
                    file.write("--------------------------------------\n\n")

    def generate_provider_service_report(self):
        # Load visit records, provider list, provider directory, and member list
        with open("visit_records.json") as file:
            visit_records = json.load(file)
        with open("provider_list.json") as file:
            provider_list = json.load(file)
        with open("provider_directory.json") as file:
            provider_directory = json.load(file)
        with open("member_list.json") as file:
            member_list = json.load(file)

        # Convert lists to dictionaries for faster lookup
        providers = {provider["ProviderID"]: provider for provider in provider_list}
        services = {service["ServiceCode"]: service for service in provider_directory}
        members = {member["MemberID"]: member for member in member_list}

        # Initialize a dictionary to track services for each provider
        provider_services = {}

        # Process each visit record
        for visit in visit_records:
            provider_id = visit["ProviderID"]
            provider_info = providers.get(provider_id)
            member_info = members.get(visit["MemberID"])
            service_info = services.get(visit["ServiceCode"])

            if provider_info and member_info and service_info:
                if provider_id not in provider_services:
                    provider_services[provider_id] = {
                        "provider_info": provider_info,
                        "services": [],
                        "total_consultations": 0,
                        "total_fee": 0.0,
                    }

                # Append service info and update totals
                visit_details = {
                    "DateOfService": visit["DateOfService"],
                    "DateRecorded": visit["DateRecorded"],
                    "MemberName": member_info["MemberName"],
                    "MemberNumber": visit["MemberID"],
                    "ServiceName": service_info["ServiceName"],
                    "ServiceFee": visit.get("ServiceFee", 0),
                }
                provider_services[provider_id]["services"].append(visit_details)
                provider_services[provider_id]["total_consultations"] += 1
                provider_services[provider_id]["total_fee"] += float(
                    visit_details["ServiceFee"]
                )

        # Directory to store the generated reports
        output_directory = "provider_reports"
        os.makedirs(output_directory, exist_ok=True)

        # Write report for each provider
        for provider_id, data in provider_services.items():
            file_name = f"{data['provider_info']['ProviderName'].replace(' ', '_')}.txt"
            file_path = os.path.join(output_directory, file_name)

            with open(file_path, "w") as file:
                # Write provider info
                pi = data["provider_info"]
                file.write(f"Provider Name: {pi['ProviderName']}\n")
                file.write(f"Provider Number: {provider_id}\n")
                file.write(f"Provider Address: {pi['ProviderAddress']}\n")
                file.write(f"Provider City: {pi['ProviderCity']}\n")
                file.write(f"Provider State: {pi['ProviderState']}\n")
                file.write(f"Provider Zip: {pi['ProviderZip']}\n\n")

                # Write services info
                for service in data["services"]:
                    file.write(f"Date of Service: {service['DateOfService']}\n")
                    file.write(f"Date Recorded: {service['DateRecorded']}\n")
                    file.write(f"Member Name: {service['MemberName']}\n")
                    file.write(f"Member Number: {service['MemberNumber']}\n")
                    file.write(f"Service Name: {service['ServiceName']}\n")
                    file.write(f"Fee Paid: ${service['ServiceFee']}\n")
                    file.write("--------------------------------------\n\n")

                # Write total consultations and fee
                file.write(f"Total Consultations: {data['total_consultations']}\n")
                file.write(f"Total Fee for the Week: ${data['total_fee']:.2f}\n")

    def create_eft_report(self):
        # Read the EFT records from the JSON file
        try:
            with open("eft_records.json") as file:
                eft_records = json.load(file)
        except FileNotFoundError:
            print("Error: JSON file not found.")
            return
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")
            return

        # Write the contents to a txt file
        with open("eft_records.txt", "w") as file:
            for record in eft_records:
                if record:  # Check if the record is not empty
                    file.write(f"Provider Name: {record.get('ProviderName', 'N/A')}\n")
                    file.write(f"Provider ID: {record.get('ProviderID', 'N/A')}\n")
                    file.write(f"Amount: {record.get('Amount', 'N/A')}\n")
                    file.write("--------------------------------------\n\n")
