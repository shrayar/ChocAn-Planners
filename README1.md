# ChocAn
**CS314**
**Group 3 - Fall 2023**
**Sjeobb: Shraya Ramanoorthy, Jessie Le, Elliot Roberts, Otter Winter, Benjamin Lutz, Baylie Gende**

## Project Overview
ChocAn wants to help people addicted to chocolate by offering a membership. Members pay every month to get unlimited advice and treatments from health experts like dietitians, doctors, and exercise specialists. The ChocAn project uses a computer system to make it easy to talk with members, handle payments, and create reports efficiently.

## Software Structure:
To receive healthcare from ChocAn, each member visiting ChocAn will be issued a unique card and a personal number ID. This exclusive card and number ID are assigned to every member, and the same applies to the providers within ChocAn. When a member arrives at ChocAn, they must present their card for validation. If the number ID is valid, the system will display "Active" in the status section. If the number ID is invalid, the system will show "Suspended," accompanied by the specific reason, such as an Invalid number ID or a Member Suspended status. This validation process also extends to providers. The main terminal becomes accessible for tasks related to members or providers, such as working with their information, viewing weekly reports, or accessing services. Each section is equipped with its own set of sub-menus, enhancing the overall user experience and facilitating navigation.

## Member
While members have the right to modify their personal information, they are not authorized to make changes to the list of services; this task is reserved for their respective providers. To update personal information, a member must go through a validation process. This involves providing their name and member ID. The system checks this information against the ChocAn directory stored in the 'member_list.json' file. If either the name or member ID does not match any records, the system displays the message 'The member is not found in the directory.' For each member, the system displays comprehensive information, including personal details and a list of services received. The information is presented in an easily understandable format, with services listed in order of the service date. This structure ensures clarity and a seamless experience for both members and providers interacting with the ChocAn system. The member's information includes:
- Member name (25 characters). 
- Member number (9 digits). 
- Member street address (25 characters). 
- Member city (14 characters). 
- Member state (2 letters). 
- Member zip code (5 digits). 
- Member status(Active or Suspended)

For each service provided, the following details are required: 
- Date of service (MM-DD-YYYY). 
- Provider name (25 characters). 
- Service name (20 characters). 

# Provider
In the ChocAn system, each member who has consulted a ChocAn provider during a given week is provided with a list of services received, sorted chronologically based on the service date. Providers are empowered to access member information through the provider terminal, allowing them to add new services and modify existing member details.

To enhance security and accountability, providers are required to enter their unique provider number ID before gaining access to the provider terminal. Providers can also update their personal information through the system. However, before proceeding with any modifications, the system prompts providers to input their name and provider number ID. The system cross-references this information with the 'provider_list.json' file. If no match is found, the system displays either 'The provider is not found in the directory' or 'The provider is suspended' based on the circumstances. Each provider's information, once validated, is presented comprehensively, encompassing personal details and the ability to modify both member records and their own personal information. This structured approach ensures a seamless and secure experience for providers within the ChocAn system. Each provider must contains the follow fields:
- Provider name (25 characters). 
- Provider number (9 digits). 
- Provider street address (25 characters). 
- Provider city (14 characters). 
- Provider state (2 letters). 
- Provider zip code (5 digits). 
- Provider status (Active or Suspended)

# Reports
The primary accounting procedure is executed at the ChocAn Data Center every Friday at midnight. It involves reading the file of services provided throughout the week and generating several reports. Additionally, ChocAn managers can request individual reports at any time during the week.
The software product now writes a record to "visit_records.json" file that includes the following fields: 
- Current date and time (MM-DD-YYYY HH:MM:SS). 
- Date service was provided (MM-DD-YYYY). 
- Provider number (9 digits). 
- Member number (9 digits). 
- Service code (6 digits). 
- Comments (100 characters). The comment section could be empty since it is optional.

# Services
ChocAn offers a range of health-related services to its members. Each service is uniquely identified by a name, a service code, and an associated price. These services cover various aspects of health, including consultations with dietitians, doctors, and exercise specialists. At any given moment, a provider has the option to request the software product for a Provider Directory, which is a list of service names along with their corresponding service codes and fees, arranged in alphabetical order. The Provider Directory is then sent to the provider as an email attachment(see provider_directory.json). For each service provided, the following details are required: 
- Service name (20 characters)
- Service code (6 digits)
- Service fee (up to $99,999.99)

The manager receives a summary report for accounts payable, which details every provider slated for payment in the current week. The report includes the number of consultations each provider conducted and their total fee for the week. Additionally, the report prints the total count of service-providing providers, the overall number of consultations, and the aggregate fee total.

Throughout the day, the ChocAn Data Center software operates interactively, enabling operators to include new members in ChocAn, remove members who have resigned, and make updates to member records. Similarly, provider records undergo additions, deletions, and updates using the interactive mode.

ChocAn has outsourced the handling of membership fee payments to Acme Accounting Services, a third-party organization. Acme is tasked with financial procedures, including recording membership fee payments, suspending members with overdue fees, and reinstating suspended members upon payment. The Acme computer updates the corresponding ChocAn Data Center membership records every evening at 9 P.M.

## Testing and Acceptance
Your organization has secured the contract specifically for developing the ChocAn data processing software. Another organization will handle the communications software, design the ChocAn provider’s terminal, create the software required by Acme Accounting Services, and implement the EFT component. According to the contract terms, during the acceptance test, the data from a provider’s terminal must be simulated using keyboard input, and the data intended for transmission to a provider’s terminal display must be visible on the screen. Simulation of a manager’s terminal should also be done using the same keyboard and screen. Each member report is required to be written to its individual file, with the file name starting with the member name followed by the report date. The provider reports should follow the same format. Additionally, the Provider Directory must be generated as a file, and none of these files should be sent as actual email attachments. Regarding the EFT data, the contract specifies the creation of a file containing the provider name, provider number, and the transfer amount as the only requirement.