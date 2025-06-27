import requests

from Job import Job


class WorkdayFetch:

    def __init__(self, url, intern_code, us_code):
        self.url = url
        self.intern_code = intern_code
        self.us_code = us_code

    def ObtainWorkdayData(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        payload = {
            "appliedFacets": {
                # United States location ID
                "locationHierarchy1": [self.us_code],
                # Intern subtype ID (optional, but narrows results)
                "workerSubType": [self.intern_code]
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

        response = requests.post(self.url, headers=headers, json=payload)
        data = response.json()
        jobs = data.get("jobPostings", [])
        job_paths = [job.get("externalPath") for job in jobs]

        total_jobs_scraped = []

        for path in job_paths:
            url2 = self.url[:self.url.index("/job")] + path
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
