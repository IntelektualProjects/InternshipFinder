import requests
import re
from Job import Job

class JobTypeFiltration:
    def __init__(self, list_of_jobs):
        self.job_list = list_of_jobs
        self.intern_keywords = ["intern", "internship", "co-op", "cooperative education"]
        self.ece_keywords = [
            "electrical", "ece", "electronics", "circuit", "semiconductor",
            "power systems", "vlsi", "fpga", "analog", "digital", "embedded", "signal processing",
            "microelectronics", "pcb", "rtl", "hardware", "firmware", "verification", "asic", "test"]
        self.bachelors_patterns = [
            re.compile(r"\bbachelor\b", re.IGNORECASE),
            re.compile(r"\b(b\.?s\.?)\b", re.IGNORECASE),
            re.compile(r"\bundergrad\b", re.IGNORECASE),
            re.compile(r"\bbs\b", re.IGNORECASE)
        ]


    def internship_filter_single_job(self, job):
        title = job.title.lower()
        description = job.description.lower()

        combined_text = f"{job.title} {job.description}".lower()

        is_intern = any(keyword in combined_text for keyword in self.intern_keywords)
        is_ece_related = any(keyword in combined_text for keyword in self.ece_keywords)
        is_undergrad = any(pattern.search(combined_text) for pattern in self.bachelors_patterns)

        return is_intern and is_ece_related and is_undergrad

    def internship_filter_multiple_jobs(self):
        newlist = []

        for job in self.job_list:
            if self.internship_filter_single_job(job):
                newlist.append(job)
        return newlist
