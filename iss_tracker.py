import requests
import smtplib
import datetime as dt
import time

#enter your email address and password
myemail = 'your email'
password = 'your password'
msg = 'The International Space Station will be in the night sky in your area. Look up!'

#enter your latitude and longitude
parameters = {'lat':1,
              'lng':1,
              'formatted': 0}
response = requests.get('https://api.sunrise-sunset.org/json', params = parameters)
response.raise_for_status()
data = response.json()
sunrise = float((data['results']['sunrise']).split('T')[1].split(':')[0])
sunset = float((data['results']['sunset']).split('T')[1].split(':')[0])

iss = requests.get('http://api.open-notify.org/iss-now.json').json()
isslong = float(iss['iss_position']['longitude'])
isslat = float(iss['iss_position']['latitude'])


now  = dt.datetime.now().hour

while True:
    time.sleep(60)
    if (now) < (sunrise) or now > (sunrise):
        if isslong - 5 < parameters['lng'] < isslong + 5 and isslat - 5 < parameters['lat'] < isslat + 5:

            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(user=myemail, password=password)
                connection.sendmail(from_addr=myemail, to_addrs=myemail,
                                    msg=f'Subject: ISS Tracker\n\n{msg}')
                connection.close()

