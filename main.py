import requests
from datetime import datetime
import time
import smtplib

MY_LAT = 6.512990
MY_LONG = 3.321320
ONE_MIN = 60

my_outlook = "matthew.ogalu@outlook.com"
my_password = "123123"# 😃
iss_is_close = False

"""response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()"""

# Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def check_for_iss():
    global iss_is_close
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    data = iss_response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sun_data = response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour - 1

    if MY_LAT - 5 < iss_latitude < MY_LAT + 5 and MY_LONG - 5 < iss_longitude < MY_LONG + 5:
        if hour >= sunset or hour <= sunrise:
            iss_is_close = True

    print(iss_latitude, iss_longitude)
    print(MY_LAT, MY_LONG)
    print(time_now)
    return iss_is_close


while not iss_is_close:
    check_for_iss()
    time.sleep(ONE_MIN)
if iss_is_close:
    with smtplib.SMTP(host="smtp.office365.com:587") as connection:
        connection.starttls()
        connection.login(user=my_outlook, password=my_password)
        connection.sendmail(from_addr=my_outlook,
                            to_addrs=("vanessanwolisa64@gmail.com", "obioracelestine@gmail.com"),
                            msg="Subject:Look up, the ISS is close\n\n"
                                "Hi, Look into the sky and locate the ISS.")

# If the ISS is close to my current position
# ,and it is currently dark
# Then email me to look up.
# BONUS: run the code every 60 seconds.
