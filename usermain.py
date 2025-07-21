from googleapiclient.errors import HttpError

from SheetsIntegration import SheetsIntegration
import config

# This is the Second User Entry Point of InternshipFinder
# - Purpose: User can enter new Company and API endpoint url to the GSheet backend for daily updates
#           on jobs.
# - Access point: Create a desktop shortcut to the script which will allow for user access to program

from colorama import init, Fore, Style
import time
import os


# Initialize colorama
init(autoreset=True)

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Title block
print(Fore.CYAN + Style.BRIGHT + "=" * 60)
print(Fore.CYAN + Style.BRIGHT + "        🚀 InternshipFinder Project".center(60))
print(Fore.CYAN + Style.BRIGHT + "=" * 60)
print()

# Description
print(Fore.YELLOW + Style.BRIGHT + "Welcome to InternshipFinder!\n")
print(
    "This tool automates the process of finding internship postings "
    "from various company career pages using live webscraping techniques."
)

print()
print(Fore.MAGENTA + "🔍 Features:")
print(Fore.WHITE + Style.BRIGHT + " - Collects job listings from custom endpoints and stores into Accessible Google Sheet")
print(Fore.WHITE + Style.BRIGHT + " - Filters new listings daily")
print(Fore.WHITE + Style.BRIGHT + " - Notifies you of active postings")
print(Fore.WHITE + Style.BRIGHT + " - Logs company responses and timestamp")
print()

print(Fore.BLUE + "✨ Designed for students. Powered by Python.")
print(Fore.RED + Style.NORMAL + "   Script created by Shreyas Potnuru\n")
print(Fore.CYAN + Style.BRIGHT + "=" * 60)
time.sleep(1)


setup_response = input("Do you wish to start scraping jobs [" + Fore.GREEN + Style.BRIGHT + "y" + Style.RESET_ALL + Fore.RESET +
                       "/" + Fore.RED + Style.BRIGHT + 'n' + Style.RESET_ALL + "]? ")

tries = 1
while tries <= 3:
    if setup_response.lower() == "n":
        print("Exiting InternshipFinder Application...")
        exit(1)
    elif setup_response.lower() == "y":
        break
    else:
        setup_response = input("\nUnrecognized Response. Please Enter only a yes [y] or no [n] response: ")
        tries += 1
else:
    print(Fore.RED + Style.DIM + "\n3 Incorrect Question Attempts. Exiting InternshipFinder Application...")
    exit(1)



while True:
    print('Great! Now lets add some companies to track!\n')

    company_name = input("Please enter the Company Name: ")
    c_url = input("Please enter the JSON Endpoint cURL. Please note that this is not the direct URL to the Company Careers page,"
                  " rather the JSON endpoint which holds all the job information.\n\nCompany JSON Jobs cURL: ")

    gsheetAdder = SheetsIntegration(config.spreadsheet_backend_id, config.url_base_range)

    try:
        gsheetAdder.add_endpoint_to_sheet(company_name, c_url)
    except HttpError as error:
        print(f"Google Sheets API error: {error}")
        break
    print(Fore.GREEN + Style.NORMAL + f"{company_name} has been successfully added to Tracked Companies.")

    continue_request = input("\nDo you wish to continue adding companies[" + Fore.GREEN + Style.BRIGHT + "y" + Style.RESET_ALL + Fore.RESET +
                       "/" + Fore.RED + Style.BRIGHT + 'n' + Style.RESET_ALL + "]? ")

    if continue_request.lower() == "y":
        continue
    else:
        print("Thank you for using InternshipFinder. Exiting Application...")
        exit(1)

