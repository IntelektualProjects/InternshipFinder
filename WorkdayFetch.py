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
        us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                     "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                     "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        facets = self.get_facets()
        loc_facet = self.get_facet_field(facets, ["country", "location"])
        if not loc_facet:
            return None


        facets = self.get_facets()
        location_facet = self.get_facet_field(facets, ["country", "location"])

        location_internal_filters = location_facet.get('values')

        # try to find a direct United States filter (country-level)
        for internal_filter in location_internal_filters:
            name = internal_filter.get('descriptor')

            if name.lower() in united_states_descriptors:
                return location_facet.get('facetParameter'), internal_filter.get('id')

            if ("location" in name.lower()) or ('country' in name.lower()):
                values = internal_filter.get('values')
                for option in values:
                    if option.get('descriptor').lower() in united_states_descriptors:
                        return internal_filter.get('facetParameter'), option.get('id')

        listed_us_locations = []
        facetparameter = ""
        for internal_filter in location_internal_filters:
            nested_values = internal_filter.get("values")
            for value in nested_values:
                descriptor = value.get("descriptor").lower()

                # Match either a US descriptor or a US state abbreviation
                if any(us_desc in descriptor.lower() for us_desc in united_states_descriptors) or \
                        any(state in descriptor.upper() for state in us_states):

                    # Return the parent facet parameter and the matched ID
                    listed_us_locations.append(value.get('id'))
            facetparameter = internal_filter.get('facetParameter')


        if len(listed_us_locations) == 0:
            return None
        return facetparameter, listed_us_locations



    def worktypefiltration(self):
        facets = self.get_facets()
        worktype_facet = self.get_facet_field(facets, ["worker"])

        worker_internal_filters = worktype_facet.get('values')
        for internal_filter in worker_internal_filters:
            name = internal_filter.get('descriptor')
            if "intern" in name.lower():
                return worktype_facet.get("facetParameter"), internal_filter.get('id')
        return None



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
        applied_facets = {}
        facet_criteria = []

        # If a location filter was found
        if location:
            loc_key, loc_vals = location
            if not isinstance(loc_vals, list):
                loc_vals = [loc_vals]
            applied_facets[loc_key] = loc_vals
            facet_criteria.append({"facetName": loc_key, "filterType": "MULTI"})

        # If a worker (e.g., intern) filter was found
        if worker:
            wk_key, wk_val = worker
            if not isinstance(wk_val, list):
                wk_val = [wk_val]
            applied_facets[wk_key] = wk_val
            facet_criteria.append({"facetName": wk_key, "filterType": "MULTI"})

        # Add static filters (these remain unchanged)
        static_filters = [
            "timeType", "categories", "jobFamilyGroup", "jobFamily", "teams"
        ]
        for field in static_filters:
            facet_criteria.append({"facetName": field, "filterType": "MULTI"})

        return {
            "appliedFacets": applied_facets,
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
            "facetCriteria": facet_criteria
        }

    def obtain_workday_data(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        locationfilter = self.locationfiltration()
        worktypefilter = self.worktypefiltration()
        #print("locationfilter:", locationfilter)
        #print("worktypefilter:", worktypefilter)

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