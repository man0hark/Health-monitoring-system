from datetime import datetime
import random
from firebase import firebase



name = input("Enter the name:\n")


now = datetime.now()
current_time = now.strftime("%H:%M")
firebase = firebase.FirebaseApplication('https://icps-9cc0a.firebaseio.com/', None)
data =  { 'time': str(current_time),
         'data':str(random.randint(80,130))
          }

firebase.post('/'+ str(name) + '/glucose',data)
print("Glucose value uploaded")
now = datetime.now()

current_time = now.strftime("%H:%M")
data =  { 'time': str(current_time),
         'data':str(random.randint(90,120))
          }

firebase.post('/'+ str(name) + '/bp',data)
print("BP value uploaded")
now = datetime.now()

current_time = now.strftime("%H:%M")
data =  { 'time': str(current_time),
         'data':str(random.randint(93,100))
          }

firebase.post('/'+ str(name) + '/temp',data)
print("Body temperature value uploaded")
print("Data uploaded")