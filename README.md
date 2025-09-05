# InternshipFinder

**InternshipFinder** is a Python-based automation tool that helps students and early-career professionals track internship postings from multiple company career pages. 
It uses live webscraping techniques to monitor career portals and store relevant job listings in an accessible Google Sheet.

**Background**:
I'm a college electrical engineering major that was fed up with having to keep track of 100 company job application portals. To that end, I created this tool to simplify my workflow. No fancy AI stuff or anything. Just a solid Python automation script for webscraping company jobsites. No support for big sites like Linkedin, Indeed, etc. due to their terms of service.

<span style="color:red;">*Disclaimer:*</span>
This tool is intended to show off my programming skils in building custom software applications with a use. 
Anyone who forks/copies the code is individually responsible for ensuring they comply with the terms of service of any site they scrape. 
The author is not responsible for misuse or legal consequences resulting from this software.

Feel free to fork or submit issues as you see fit!

**Current Build Status**:
- Support for ECE/Electrical Engineering Undergraduate Internships (cause that's my major :D )
- Currently works for all Workday-based portals (custom webpages are not supported yet)
- Location Filtering currently set to United States
- No direct executable has been made, but the main.py and usermain.py scripts are all you need.
- Windows-specific as of this point

## 🔍 Features
InternshipFinder streamlines the internship hunting process by:
- ✅ **Track internships from custom JSON job feeds**
- 📄 **Integrates with Google Sheets** for centralized job listing storage
- ⏱️ **Daily update support** (via Windows Task Scheduler) only once per day
- 🧠 **Smart filtering** to avoid duplicates
- 💬 **Interactive CLI prompts** to manage tracked companies
- 📊 **Logs timestamped responses** for better organization

This tool is designed to be **easy to use, efficient, and customizable** for your internship search needs.

## 🔧 How It Works
Upon running the script:
1. You'll be greeted with an interactive CLI interface.
2. You're prompted to begin scraping jobs or exit.
3. If you continue, you can enter:
   - The **Company Name**
   - The **Company’s JSON Endpoint** (not the public careers page, but the endpoint URL containing job data)
4. The information is added to a **Google Sheet** using the [Google Sheets API](https://developers.google.com/sheets/api).
5. You can continue adding multiple companies to track.
6. Each day, the script checks for **new job listings** from the companies entered previously, updates the sheet, and notifies you of changes.

## ⚙️ Prerequisites
- Python 3.10+
- Google Sheets API credentials (OAuth2 setup)
- Required Python packages:
  - `google-api-python-client`
  - `colorama`
  - `requests`
  - `plyer` for desktop notifications

## Instructions on How to Run Program (Windows Only)
1. Fork/download repo to your computer
2. Make sure to install prerequisite libraries
3. Create a desktop shortcut for usermain.py with this target command:
```
"C:\\User\profile_name\...path to python executable...\Python310\python.exe" ""C:\\User\profile_name\...path to saved folder...\InternshipFinder\usermain.py"
```
4. To set up daily desktop notifications, go to task scheduler and create a new basic task. Follow through the instructions and preferences for updates.

    For **Program/Script**:
    ```
      C:\\User\profile_name\...path to python executable...\Python310\python.exe
    ```

    For **Arguments**:
    ```
    C:\\User\profile_name\...path to saved folder...\InternshipFinder\main.py
    ```
5. Save Changes and click Desktop Shortcut to begin entering companies

## Future Integrations
- Position-specific Automated Resume Creation with Latex Templating
- Mac/Linux Support and installers
   
