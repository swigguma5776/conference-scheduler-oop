import requests 
import requests_cache 
from datetime import datetime 



requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=180)

class ConferenceScheduler():

    """
    Class for Conference Scheduler API Assessment. The objective is to send an API GET request to the server, get back a collection of partners
    who need to attend meeting within their respected countries. From the data the class must parse through and find attendees and start dates
    for conferences in each country such that the number of attendees is maximized. The conference is a 2 day event so attendees must be able to
    attend both days. Lastly, the class must build an invitation list data object and POST it to the same API. 
    """

    def __init__(self):
        self.country_dict = {}
        self.conference_dict = {
            'Conferences': []
        }
        self.conference_api_call()
        self.create_schedule()
        self.post_schedule()

    def conference_api_call(self):

        request = requests.get("https://backendassessmentv1.onrender.com/conference")
        
        if request.status_code == 200:
            partners = request.json()['partners']
            print("Your GET request was successful")
        else:
            print("GET request failed with status code: ", request.status_code)

        for partner in partners:
            self.country_dict[partner['country']] = self.country_dict.get(partner['country'], dict()) 
            for i in range(len(partner['availableDates'])-1):
                datetime1 = datetime.strptime(partner['availableDates'][i], "%Y-%m-%d")
                datetime2 = datetime.strptime(partner['availableDates'][i+1], "%Y-%m-%d")
                difference = datetime2 - datetime1
              
                if difference.days == 1 and partner["availableDates"][i] not in self.country_dict[partner['country']]:
                    self.country_dict[partner['country']][partner["availableDates"][i]] = [partner['email']]
                elif difference.days == 1 and partner["availableDates"][i] in self.country_dict[partner['country']]:
                    self.country_dict[partner['country']][partner["availableDates"][i]].append(partner['email'])


    def create_schedule(self):

        for country, dict in self.country_dict.items():
            start_date = ""
            attendee_count = -float('inf')
            final_attendees = []
            for time, attendees in dict.items():
                if len(attendees) > attendee_count:
                    attendee_count = len(attendees)
                    start_date = time 
                    final_attendees = attendees

            conference = Conference(country, start_date, attendee_count, final_attendees)
            self.conference_dict['Conferences'].append(conference.__dict__)
        
        print(self.conference_dict)
                
    
    def post_schedule(self):
        
        response = requests.post("https://backendassessmentv1.onrender.com/conference", data=self.conference_dict)
        
        if response.status_code == 200:
            print("Your POST was successful")
        else:
            print("POST request failed with status code: ", response.status_code)


class Conference():
    def __init__(self, country, start_date, attendee_count, attendees):
        self.name = country
        self.startDate = start_date
        self.attendeeCount = attendee_count
        self.attendees = attendees 


conferences = ConferenceScheduler()


