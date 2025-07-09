import requests

from Job import Job
from WorkdayFetch import WorkdayFetch

filter_words = ["Bachelor", "B.S", "Undergrad", "BS"]
test_urls = ["https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs",
             "https://analogdevices.wd1.myworkdayjobs.com/wday/cxs/analogdevices/External/jobs",
             "https://cadence.wd1.myworkdayjobs.com/wday/cxs/cadence/External_Careers/jobs",
             "https://marvell.wd1.myworkdayjobs.com/wday/cxs/marvell/MarvellCareers/jobs",
             "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
             "https://broadcom.wd1.myworkdayjobs.com/wday/cxs/broadcom/External_Career/jobs",
             "https://nxp.wd3.myworkdayjobs.com/wday/cxs/nxp/careers/jobs"]


def fetch_raw_intern_data(page):
    url = "https://careers.amd.com/api/jobs"
    params = {
        "keywords": "intern",
        "sortBy": "posted_date",
        "page": page,
        "internal": "false",
        "country": "United%20States",
        "limit": 100
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    # this endpoint returns an object with a "jobs" list
    jobs = data.get("jobs", [])

    # extract and return "data" key in each job listing
    job_data_list = [job.get("data") for job in jobs]

    total_jobs_scraped = []

    for job in job_data_list:
        total_jobs_scraped.append(Job(
            req_id=job.get("req_id"),
            title=job.get("title"),
            posted_date=job.get("posted_date"),
            apply_url=job.get("apply_url"),
            description=job.get("description"),
            company=job.get("hiring_organization")))

    return total_jobs_scraped

def filter_internship_results(job_list):
    newlist = []

    for item in job_list:
        for keyword in filter_words:
            if (keyword in item.title) or (keyword in item.description):
                newlist.append(item)

    return newlist


# unfiltered_jobs = fetch_raw_intern_data(page=1)
# filtered_jobs = filter_internship_results(unfiltered_jobs)
# print(str(len(filtered_jobs)) + " " + str(len(unfiltered_jobs)))

unfiltered = WorkdayFetch(url = test_urls[2])
unfiltered2 = WorkdayFetch(url = test_urls[0])
unfiltered3 = WorkdayFetch(url= test_urls[2])

r = unfiltered3.obtain_workday_data()
for i in r:
    print(Job.job_to_string(i))