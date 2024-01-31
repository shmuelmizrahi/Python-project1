from twilio.rest import Client
import time
import requests

# Twilio credentials
TWILIO_PHONE_NUMBER = "   "
TO_PHONE_NUMBER = "   "
TWILIO_SID = "    "
TWILIO_AUTH_TOKEN = "  "

# Initialize emergency status
emergency_triggered = False

def send_sms(message, location):
    map_url = f"https://www.google.com/maps/place/{location[0]},{location[1]}"
    message_with_map = f"{message}\nLocation: {map_url}"

    english_text = "Emergency! Request immediate assistance."

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"{message_with_map}\n{english_text}",
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )

        if message.sid:
            print(f"Message sent successfully with SID: {message.sid}")
            print(f"Sent message: {message_with_map}") 
        else:
            print("Failed to send message.")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def get_location_ipinfo():
    try:
        response = requests.get('https://ipinfo.io')
        response.raise_for_status()
        data = response.json()

        # Extract city information
        city = data.get('city')
        return city
    except requests.exceptions.RequestException as req_err:
        print(f"Request error getting location from IPinfo: {req_err}")
        return None
    except Exception as e:
        print(f"Error getting location from IPinfo: {e}")
        return None

# Set the temperature threshold for emergency
emergency_temperature_threshold = 200

# Check for emergency confirmation
while not emergency_triggered:
    # Get temperature from the heat sensor (replace with actual values based on your sensor)
    current_temperature = 201

    if current_temperature >= emergency_temperature_threshold:
        location = get_location_ipinfo()
        print(f"Temperature reached {emergency_temperature_threshold}! Initiating emergency protocol.")
        emergency_message = f"Emergency! ! ! ! \nTemperature: {current_temperature}°C"
        send_sms(emergency_message, location)

       
        emergency_triggered = True

    # Pause to avoid sending messages too quickly
    time.sleep(1)
