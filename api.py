import requests 
import requests_cache 



requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=180)

class ConferenceScheduler():

    def __init__(self):
        self.country_dict = {}
        self.conference_dict = {
            'Conferences': []
        }
        self.conference_api_call()

    def conference_api_call(self):

        request = requests.get("https://backendassessmentv1.onrender.com/conference")
        
        if request.status_code == 200:
            partners = request.json()['partners']
            print("Your GET request was successful")
        else:
            print("GET request failed with status code: ", request.status_code)

        for partner in partners:
            self.country_dict[partner['country']] = self.country_dict.get(partner['country'], dict()) 
            for date in partner['availableDates']:
                if date not in self.country_dict[partner['country']]:
                    self.country_dict[partner['country']][date] = []

            for date in self.country_dict[partner['country']]:
                self.country_dict[partner['country']][date].append(partner['email'])


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

print('hello')
conferences = ConferenceScheduler()
conferences.create_schedule()
conferences.post_schedule()

