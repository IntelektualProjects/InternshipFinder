
from plyer import notification

from WorkdayFetch import WorkdayFetch
from SheetsIntegration import SheetsIntegration
from JobTypeFiltration import JobTypeFiltration

import config

filter_words = ["Bachelor", "B.S", "Undergrad", "BS"]
test_urls = ["https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
             "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs",
             "https://cadence.wd1.myworkdayjobs.com/wday/cxs/cadence/External_Careers/jobs",
             "https://marvell.wd1.myworkdayjobs.com/wday/cxs/marvell/MarvellCareers/jobs",
             "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
             "https://broadcom.wd1.myworkdayjobs.com/wday/cxs/broadcom/External_Career/jobs",
             "https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs"]


# START OF RUNTIME PROGRAM
gsheet_endpoints = SheetsIntegration(config.spreadsheet_backend_id, config.url_base_range)
endpoints = gsheet_endpoints.get_endpoints_from_sheet()

gsheet_jobentries = SheetsIntegration(config.spreadsheet_backend_id, config.job_sheet_range)

job_listings_today = 0
hiring_org_set = set()
# For workday listings (no site sorting or job filtration implemented yet)
for ep in endpoints:
    job_from_endpoint = WorkdayFetch(url=ep["url"])
    job_listings_from_company = job_from_endpoint.obtain_workday_data()

    filtering_object = JobTypeFiltration(job_listings_from_company)
    filtered_job_listings = filtering_object.internship_filter_multiple_jobs()

    if len(filtered_job_listings) != 0:
        job_listings_today += len(filtered_job_listings)
        hiring_org_set.add(ep["company"])

        for entry in filtered_job_listings:
            gsheet_jobentries.add_job_entry(entry)

        print(f"Company Data Acquisition Successful\n {ep['company']}: {len(filtered_job_listings)}\n")

# Notification Generation for Desktop
notification.notify(
    title=f"New InternshipFinder Listings: {job_listings_today}",
    message=f"Companies: {', '.join(hiring_org_set)}",
    timeout=25
)