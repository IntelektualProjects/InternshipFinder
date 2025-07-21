import requests
from plyer import notification
from datetime import datetime
from time import sleep
import os

from Job import Job
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

job_listings_today = []
hiring_org_set = set()
# For workday listings (no site sorting or job filtration implemented yet)
for ep in endpoints:
    job_from_endpoint = WorkdayFetch(url=ep["url"])
    job_listings_from_company = job_from_endpoint.obtain_workday_data()

    if len(job_listings_from_company) != 0:
        job_listings_today.extend(job_listings_from_company)
        for j in job_listings_from_company:
            print(Job.job_to_string(j))
        hiring_org_set.add(ep["company"])
        print(f"Company Data Acquisition Successful\n {ep['company']}: {len(job_listings_today)}\n")

notification.notify(
    title=f"New InternshipFinder Listings: {len(job_listings_today)}",
    message=f"Companies: {', '.join(hiring_org_set)}",
    timeout=25
)
# waiting time
sleep(7)