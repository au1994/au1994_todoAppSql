import sched, time
import requests
import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from push_notifications.models import GCMDevice

from todo.models import Task,Notification

def run():
    print "in run function"
    start_scheduler()

def start_scheduler():
    print "in start scheduler"
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, send_notification, (s,))
    s.run()

def send_notification(sc):
    
    print "yes doing job"
    nowtime = datetime.now()
    tasktime = datetime.now() + timedelta(hours=2,minutes=30)
    tasks = Task.objects.filter(due_date__gt=nowtime)
    tasks = tasks.filter(due_date__lt=tasktime)
    tasks = tasks.filter(is_notified=False)
    tasks = tasks.filter(is_completed=False)    
    for task in tasks:

        flag = True
        user = User.objects.get(username=task.owner)
        devices = GCMDevice.objects.filter(user=user.id)
        for device in devices:

            print device.registration_id
            url = "https://android.googleapis.com/gcm/send"
            reg_ids = []
            reg_ids.append(device.registration_id)
            payload = {
                    'registration_ids': reg_ids
                    }
            payload = json.dumps(payload)
            print payload

            headers = {
                'authorization': "key=AIzaSyCgvC4H3BagTrXpOM1GZfCY-V8xC36-sJs",
                'content-type': "application/json",
                }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text) 
            if(response.status_code != 200):
                flag = False
        
        if flag is True:
            task.is_notified = True
            task.save()
        
    sc.enter(10, 1, send_notification, (sc,))
