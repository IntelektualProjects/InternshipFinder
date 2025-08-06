import requests
from Job import Job

class JobTypeFiltration:
    def __init__(self, list_of_jobs):
        self.job_list = list_of_jobs
        self.intern_keywords = ["intern", "internship", "co-op", "cooperative education"]
        self.ece_keywords = [
            "electrical engineering", "ece", "electronics", "circuit", "semiconductor",
            "power systems", "vlsi", "fpga", "analog", "digital", "embedded", "signal processing",
            "microelectronics", "pcb", "rtl", "hardware", "firmware", "verification", "asic", "test"]
        self.bachelors_keywords = ["Bachelor", "B.S", "Undergrad", "BS"]


    def internship_filter_single_job(self, job):
        title = job.title.lower()
        description = job.description.lower()

        # Check for intern keyword
        is_intern = any((keyword in title) or (keyword in description) for keyword in self.intern_keywords)
        # Check for ECE-related keyword
        is_ece_related = any((keyword in title) or (keyword in description) for keyword in self.ece_keywords)
        # Check for Bachelor's Degree
        is_undergrad = any((keyword in title) or (keyword in description) for keyword in self.bachelors_keywords)

        return is_intern and is_ece_related and is_undergrad

    def internship_filter_multiple_jobs(self):
        newlist = []

        for job in self.job_list:
            if self.internship_filter_single_job(job):
                newlist.append(job)
        return newlist