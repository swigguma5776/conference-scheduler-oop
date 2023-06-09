import requests 
import requests_cache 
from datetime import datetime 



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
            for i in range(len(partner['availableDates'])-1):
                datetime1 = datetime.strptime(partner['availableDates'][i], "%Y-%m-%d")
                datetime2 = datetime.strptime(partner['availableDates'][i+1], "%Y-%m-%d")
                difference = datetime2 - datetime1
              
                if difference.days == 1 and partner["availableDates"][i] not in self.country_dict[partner['country']]:
                    self.country_dict[partner['country']][partner["availableDates"][i]] = [partner['email']]
                elif difference.days == 1 and partner["availableDates"][i] in self.country_dict[partner['country']]:
                    self.country_dict[partner['country']][partner["availableDates"][i]].append(partner['email'])


            # for date in partner['availableDates']:
            #     if date in self.country_dict[partner['country']]:
            #         self.country_dict[partner['country']][date].append(partner['email'])

            # for date in self.country_dict[partner['country']]:
            #     print(date)
                # self.country_dict[partner['country']][date].append(partner['email'])

        # print(self.country_dict['United States'])


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
        
        response = requests.post("https://backendassessmentv1.onrender.com/conference", self.conference_dict)
        
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

# print('hello')
conferences = ConferenceScheduler()
conferences.create_schedule()
conferences.post_schedule()

