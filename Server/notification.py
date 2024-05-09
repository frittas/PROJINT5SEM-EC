from twilio.rest import Client

account_sid = 'AC772f295041937437dc5d65a8732d3962'
auth_token = 'bc581068a01524f33c2c696e86064aee'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Teste Envio',
  to='whatsapp:+5512996676921' #Rafa
  # to='whatsapp:+5512997795365'   #Murilo
)

print(message.sid)