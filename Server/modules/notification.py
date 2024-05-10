from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_ID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Teste Envio',
  to='whatsapp:+5512996676921' #Rafa
  # to='whatsapp:+5512997795365'   #Murilo
)

print(message.sid)