from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from date import tz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Event():
    def __init__(self, start_datetime, end_datetime):
        self.start = start_datetime
        self.end = end_datetime
        self.next = None
        
        self.containsTime = False
        self.beforeTime = False
        
    def addEvent(self, event):
        self.next = event
        return self.next
    
    def __str__(self):
        return("(" + str(self.start) + " , " + str(self.end) + ")")
        
    def display(self):
        print(self)
        if self.next is not None:
            self.next.display()
        
class TZ(datetime.tzinfo):
    def __init__(self, hr_offset):
        self.hr_offset = hr_offset
    def utcoffset(self, dt):
        return datetime.timedelta(0, 0, 0, 0, self.hr_offset * 60)

def convertTimeToDT(hour_variable, date):
    day = date.day
    month = date.month
    year = date.year
    
    return datetime.datetime(year, month, day, hour_variable[0], hour_variable[1])


def convertEventToDT(event):
    # Takes in event and creates Event instance
    start_datetime = datetime.datetime.strptime(event['start']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
    end_datetime = datetime.datetime.strptime(event['end']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
    return Event(start_datetime, end_datetime)


def getFreePeriods(eventsHead):
    #takes in linkedlist of Events with start and end date and creates list of Events of free blocks
    slow = eventsHead
    fast = slow.next
    list = []
    
    while(fast is not None):
        if (fast.start - slow.end) >= datetime.timedelta(0):
            if(fast.start - slow.end) >= datetime.timedelta(0, 0, 0, 0, 20):
                list.append(Event(slow.end, fast.start))
            slow = fast
            fast = fast.next
        elif fast.end >= slow.end:
            slow = fast
            fast = fast.next
        else:
            fast = fast.next
            
    return list

def writeToCalendar(time):
    #end = time + 15 minutes
    #convert time to string
    #convert end to string
    event = {
      'summary': 'Injection',
      'location': 'Home',
      'description': 'Scheduled injection time',
      'start': {
        'dateTime': str(time).append("-05:00"),
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': str(time).append("-05:00"),
        'timeZone': 'America/Los_Angeles',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

event = service.events().insert(calendarId='primary', body=event).execute()
print ('Event created: %s' % (event.get('htmlLink')))  

def getProjectedTime(schedule_day, weekday_hours, weekend_hours):
    # Accepts date of scheduling and weekday and weekend hours and returns pojected next best injection datetime
    weekday_datetime = convertTimeToDT(weekday_hours, schedule_day)
    weekend_datetime = convertTimeToDT(weekend_hours, schedule_day)
    if (schedule_day.weekday() < 5):
        return weekday_datetime
    else:
        return weekend_datetime

def findInjTime(free_list, proj_datetime):
    previous_event = free_list[0]
    closest_event = free_list[0]
    for event in free_list:
        if event.end > proj_datetime:
            if event.start < proj_datetime:
                closest_event = event
                self.containsTime = True
                break
            else:
                if event.start - proj_datetime < proj_datetime - previous_event.end:
                    closest_event = event
                else:
                    closest_event = previous_event
                    closest_event.beforeTime = True
                break        
    proj_end = proj_datetime + datetime.timedelta(0, 0, 0, 0, 15)
    if closest_event.containsTime:
        if closest_event.end <= proj_end:
            return proj_datetime
        else:
            return closest_event.end - datetime.timedelta(0, 0, 0, 0, 15)
    else:
        return closest_event.start + datetime.timedelta(0, 0, 0, 0, 5)

def sinceLastMedication():
        return datetime of sincelastMedication


def main():
    
    
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    
    # Call the Calendar API
    
    from_zone = tz.gettz('America/New_York')
    to_zone = tz.gettz('UTC')
    
    
    now = datetime.datetime.today().date() - sinceLastMedication() + 29
    now = now.replace(tzinfo = from_zone)
    
    now_utc = now.astimezone(to_zone)
    
    
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=str(now_utc) + 'Z',
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
                                        
    events = events_result.get('items', [])
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    """    
    lastMedDay = lastmedicationdate() #Instance of datetime
    
    
    
    
    datetime.datetime.strptime(events[0]['start']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
    
    delta = CurrentDay - lastmedicationdate()
    
    def lastMedicationDate():
        return datetime.datetime(2019, 11, 20)
    print(lastMedicationDate())
    
    """
    
    
    
    nextInjectionSet = False
    injection_period_days = 30
    prev_weekend_time = (12, 0)
    
    prev_weekday_time = (18, 0)
    
    abs_earliest = (6, 0)
    abs_latest = (22, 0)

    sched_day = datetime.date(2019, 11, 11)

    while (sched_day - datetime.datetime.today().date() < 7 and not nextInjectionSet):
    
    
        #Setup LL of events in calendar
        head = Event(convertTimeToDT((0, 0), sched_day), convertTimeToDT(abs_earliest, sched_day))
        current = head
        end = convertTimeToDT(abs_latest, sched_day)
        
        for event in events:
            tmp = convertEventToDT(event)
            if startingPt < tmp.end:
                if end < tmp.start:
                    current.next = Event(end, convertTimeToDT((23, 59), sched_day))
                    break
                current.next = tmp
                current = tmp
        
        inj_time = findInjTime(getFreePeriods(head), getProjectedTime(sched_day,prev_weekday_time, prev_weekend_time))
        
    
           
if __name__ == '__main__':
    main()
