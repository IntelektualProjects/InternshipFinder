from io import StringIO


class Job:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "No Title For Position")
        self.date_posted = kwargs.get("posted_date", "No Date Posted For Position")
        self.apply_url = kwargs.get("apply_url", "No Application URL For Position")
        self.req_id = kwargs.get("req_id", "No Req. ID For Position")
        self.company = kwargs.get("company", "No Company Defined for Position")
        self.description = kwargs.get("description", "No Description For Position")

    def job_to_string(self):
        string = StringIO()
        string.write("Title: " + self.title + "\n")
        string.write("Requisition ID: " + str(self.req_id) + "\n")
        string.write("Company: " + self.company + "\n")
        string.write("Date Posted: " + self.date_posted + "\n")
        string.write("Apply URL: " + self.apply_url + "\n")
        string.write("Company: " + self.company + "\n")
        string.write("Description: " + self.description + "\n")

        return string.getvalue()
