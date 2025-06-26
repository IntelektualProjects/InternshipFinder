import requests
import json

from Job import Job

filter_words = ["Bachelor's", "B.S", "Undergrad"]


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

if __name__ == "__main__":
    unfiltered_jobs = fetch_raw_intern_data(page=1)
    filtered_jobs = filter_internship_results(unfiltered_jobs)
    print(str(len(filtered_jobs)) + " " + str(len(unfiltered_jobs)))

    for i in filtered_jobs:
        print(i.job_to_string())
