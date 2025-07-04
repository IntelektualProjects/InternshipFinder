import requests
from Job import Job

class JobTypeFiltration:
    def __init__(self, list_of_jobs):
        self.job_list = list_of_jobs

    def bachelors_internship_results(self):
        filter_words = ["Bachelor", "B.S", "Undergrad", "BS"]

        newlist = []

        for item in self.job_list:
            for keyword in filter_words:
                if (keyword in item.title) or (keyword in item.description):
                    newlist.append(item)
        return newlist

    def subject_internship_results(self):
        pass

