from operator import indexOf

import requests
import json

import config


from Job import Job

filter_words = ["Bachelor", "B.S", "Undergrad", "BS"]

def fetch_nvidia_data():
    url = "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    payload = {
        "appliedFacets": {
        # United States location ID
        "locationHierarchy1": [config.nvidia_US_code],
        # Intern subtype ID (optional, but narrows results)
        "workerSubType": [config.nvidia_intern_code]
        },
        "limit": 20,
        "offset": 0,
        "searchText": "intern",
        "searchFilters": {
            "locations": [],
            "timeType": [],
            "workerSubType": [],
            "categories": [],
            "jobFamilyGroup": [],
            "jobFamily": [],
            "teams": []
        },
        "facetCriteria": [
        {"facetName": "locationHierarchy1", "filterType": "MULTI"},  # ← FIXED
        {"facetName": "timeType", "filterType": "MULTI"},
        {"facetName": "workerSubType", "filterType": "MULTI"},
        {"facetName": "categories", "filterType": "MULTI"},
        {"facetName": "jobFamilyGroup", "filterType": "MULTI"},
        {"facetName": "jobFamily", "filterType": "MULTI"},
        {"facetName": "teams", "filterType": "MULTI"}
    ]
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    jobs = data.get("jobPostings", [])
    job_paths = [job.get("externalPath") for job in jobs]

    total_jobs_scraped = []

    for path in job_paths:
        url2 = url[:url.index("/job")] + path
        resp2 = requests.get(url2)
        data2 = resp2.json()
        jobpostingdata = data2.get("jobPostingInfo", [])
        jobhiringdata = data2.get("hiringOrganization")

        total_jobs_scraped.append(Job(
            req_id=jobpostingdata.get("jobReqID"),
            title=jobpostingdata.get("jobPostingId"),
            posted_date=jobpostingdata.get("postedOn"),
            apply_url=jobpostingdata.get("externalUrl"),
            description=jobpostingdata.get("jobDescription"),
            company=jobhiringdata.get("name")))
    return total_jobs_scraped



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

unfiltered = fetch_nvidia_data()
for item in filter_internship_results(unfiltered):
    print(item.job_to_string())