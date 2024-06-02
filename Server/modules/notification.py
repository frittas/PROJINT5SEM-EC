from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
account_sid = ""
auth_token = ""
client: Client
from_: str
to: str

class Message:
    def __init__(self, account_sid, auth_token):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_ID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)
        self.from_ = "whatsapp:+14155238886"
        self.to = "whatsapp:+5512996676921"  # Rafa

    def send(self, message: str):
        whats_message = self.client.messages.create(
            from_=self.from_,
            body=message,
            to=self.to,  # Rafa
            # to='whatsapp:+5512997795365'   #Murilo
        )
        return whats_message.sid
