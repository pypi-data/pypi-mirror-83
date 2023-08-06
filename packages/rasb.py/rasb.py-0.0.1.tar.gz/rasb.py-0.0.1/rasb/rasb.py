import requests

class RASBClient():
    """
    Defines the RASB Client.
    """
    def isUserBanned(self, user_id):
        """
        Returns if the specified user id is banned or not.
        """
        ban_list = requests.get("https://www.rasb.xyz/api/bans")
        ban_list.raise_for_status()
        ban_json = ban_list.json()

        for i in ban_json["discord"]:
            if i["id"] == user_id:
                return f"User: ({user_id}) is banned."
            else:
                return f"User: ({user_id}) is not banned."

    def getBans(self):
        """
        Returns the entire RASB ban list.
        """
        ban_list = requests.get("https://www.rasb.xyz/api/bans")
        ban_list.raise_for_status()
        ban_json = ban_list.json()

        final_list = ""
        for i in ban_json["discord"]:
            if i["id"]:
                final_list = final_list + f"ID: {i['id']} Name: {i['name']} \n"
        return final_list
    
    def getReport(self, report_id):
        """
        Returns info about the report from the report id specified.
        """
        report_list = requests.get(f"https://www.rasb.xyz/api/reports/{report_id}")
        report_list.raise_for_status()
        report_json = report_list.json()

        return f"Report ID: {report_json['data']['id']} Accused: {report_json['data']['accused']} \n\nEvidence: \n{report_json['data']['evidence']} Status: {report_json['data']['status']}\n"
