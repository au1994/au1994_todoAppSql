import sched, time
import requests
from datetime import datetime, timedelta

from django.contrib.auth.models import User

from push_notifications.models import GCMDevice

from todo.models import Task,Notification


def start_scheduler():
    
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, send_notification, (s,))
    s.run()

def send_notification(sc):
    
    nowtime = datetime.now() + timedelta(hours=5,minutes=30)
    tasktime = datetime.now() + timedelta(hours=7,minutes=30)
    tasks = Task.objects.filter(due_date__gt=nowtime)
    tasks = tasks.filter(due_date__lt=tasktime)
    tasks = tasks.filter(is_notified=False)
    
    if len(tasks) > 0:
        task = tasks[0]
        user = User.objects.get(username=task.owner)
        devices = GCMDevice.objects.filter(user=user.id)
        for device in devices:
            url = "https://android.googleapis.com/gcm/send"
            payload = "{\n    \"registration_ids\": [\"fCPrZ6g0hvI:APA91bFNGhe8eHi6fRLXKHexS-Lw9iohD9iC2Hd9IB_E4_D_R9EM6RoSwiF6TFLgvBhF3iwFSn9AF_kKYvTYTRuPzVdHZGurXnRGF_rITsUWkdZTKq1VhYj0AtsZPb-k34g3uE6GU00B\"]\n    \n}"
            headers = {
                'authorization': "key=AIzaSyCgvC4H3BagTrXpOM1GZfCY-V8xC36-sJs",
                'content-type': "application/json",
                }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text) 
    
    
    sc.enter(1, 1, send_notification, (sc,))

start_scheduler()
