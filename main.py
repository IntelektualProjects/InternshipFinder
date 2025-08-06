
from plyer import notification

from WorkdayFetch import WorkdayFetch
from SheetsIntegration import SheetsIntegration
from JobTypeFiltration import JobTypeFiltration

import config

# START OF RUNTIME PROGRAM
gsheet_endpoints = SheetsIntegration(config.spreadsheet_backend_id, config.url_base_range)
endpoints = gsheet_endpoints.get_endpoints_from_sheet()

gsheet_jobentries = SheetsIntegration(config.spreadsheet_backend_id, config.job_sheet_range)

# Get all existing req_ids to avoid duplicates
existing_req_ids = gsheet_jobentries.get_reqid_from_sheet()

# Notification data variables
job_listings_today = 0
hiring_org_set = set()

# For workday listings (no site sorting)
for ep in endpoints:
    job_from_endpoint = WorkdayFetch(url=ep["url"])
    job_listings_from_company = job_from_endpoint.obtain_workday_data()

    filtering_object = JobTypeFiltration(job_listings_from_company)
    filtered_job_listings = filtering_object.internship_filter_multiple_jobs()

    if len(filtered_job_listings) != 0:

        for entry in filtered_job_listings:
            if str(entry.req_id) not in existing_req_ids:
                gsheet_jobentries.add_job_entry(entry)
                existing_req_ids.add(str(entry.req_id))
                # update the notification variables
                job_listings_today += 1
                hiring_org_set.add(ep["company"])

        print(f"Company Data Acquisition Successful\n {ep['company']}: {len(filtered_job_listings)}\n")

# Notification Generation for Desktop
notification.notify(
    title=f"New InternshipFinder Listings: {job_listings_today}",
    message=f"Companies: {', '.join(hiring_org_set)}",
    timeout=25
)