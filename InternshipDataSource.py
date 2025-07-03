import requests

from Job import Job

class WorkdayFetch:

    def __init__(self, url):
        self.url = url

    def get_facets(self):
        # Send a base POST request to retrieve available facetFields.
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        payload = {
            "appliedFacets": {},
            "searchText": "",
            "limit": 1,
            "offset": 0
        }

        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Failed to fetch facets: {response.status_code}")
            return []
        return response.json().get("facets", [])



    def get_facet_field(self, facets, labels):
        # Finds the internal facetField given a user-facing label.
        for facet in facets:
            for label in labels:
                if label.lower() in (facet.get("facetParameter")).lower():
                    return facet
        return None



    def locationfiltration(self):
        united_states_descriptors = ["us", "united states", "u.s", "america", "united states of america"]

        facets = self.get_facets()
        location_facet = self.get_facet_field(facets, ["country", "location"])

        location_internal_filters = location_facet.get('values')
        for internal_filter in location_internal_filters:
            name = internal_filter.get('descriptor')

            if name.lower() in united_states_descriptors:
                return location_facet.get('facetParameter'), internal_filter.get('id')

            if ("location" in name.lower()) or ('country' in name.lower()):
                values = internal_filter.get('values')
                for option in values:
                    if option.get('descriptor').lower() in united_states_descriptors:
                        return internal_filter.get('facetParameter'), option.get('id')

        return "No Location Found"



    def worktypefiltration(self):
        facets = self.get_facets()
        worktype_facet = self.get_facet_field(facets, ["worker"])

        worker_internal_filters = worktype_facet.get('values')
        for internal_filter in worker_internal_filters:
            name = internal_filter.get('descriptor')
            if "intern" in name.lower():
                return worktype_facet.get("facetParameter"), internal_filter.get('id')
        return "No Worktype Found"



    def base_payload(self):
        return {
            "appliedFacets": {},
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
                {"facetName": "location", "filterType": "MULTI"},  # ← FIXED
                {"facetName": "timeType", "filterType": "MULTI"},
                {"facetName": "workerSubType", "filterType": "MULTI"},
                {"facetName": "categories", "filterType": "MULTI"},
                {"facetName": "jobFamilyGroup", "filterType": "MULTI"},
                {"facetName": "jobFamily", "filterType": "MULTI"},
                {"facetName": "teams", "filterType": "MULTI"}
            ]
        }



    def filter_payload(self, location, worker):
        return {
            "appliedFacets": {
                # United States location ID
                location[0]: [location[1]],
                # Intern subtype ID
                worker[0]: [worker[1]],
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
                {"facetName": location[0], "filterType": "MULTI"},  # ← FIXED
                {"facetName": "timeType", "filterType": "MULTI"},
                {"facetName": "workerSubType", "filterType": "MULTI"},
                {"facetName": "categories", "filterType": "MULTI"},
                {"facetName": "jobFamilyGroup", "filterType": "MULTI"},
                {"facetName": "jobFamily", "filterType": "MULTI"},
                {"facetName": "teams", "filterType": "MULTI"}
            ]
        }



    def obtain_workday_data(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        locationfilter = self.locationfiltration()
        worktypefilter = self.worktypefiltration()
        print("locationfilter:", locationfilter)
        print("worktypefilter:", worktypefilter)

        if locationfilter == "No Location Found" or worktypefilter == "No Worktype Found":
            payload = self.base_payload()
        else:
            payload = self.filter_payload(locationfilter, worktypefilter)

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            return "Bad HTTP Request: " + str(response.status_code)

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