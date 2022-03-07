from os import environ
import requests


YOUR_DOMAIN_NAME = environ.get('YOUR_DOMAIN_NAME', '')
YOUR_API_KEY = environ.get('YOUR_API_KEY', '')

# YOUR_DOMAIN_NAME ='sandbox76165a034aa940feb3ef785819641871.mailgun.org'
# YOUR_API_KEY = '441acf048aae8d85be1c41774563e001-19f318b0-739d5c30'

# def send_simple_message(YOUR_DOMAIN_NAME, YOUR_API_KEY):
#     return requests.post(
#         "https://api.mailgun.net/v3/" + YOUR_DOMAIN_NAME + "/messages",
#         auth=("api", YOUR_API_KEY),
#         data={"from": "Abel <mailgun@" + YOUR_DOMAIN_NAME + ">",
#               "to": ["greatabel2@126.com", "YOU@abelCorp"],
#               "subject": "email test: hello world",
#               "text": "Testing some Mailgun awesomness!"})


# if __name__ == "__main__":
#     r = send_simple_message(YOUR_DOMAIN_NAME, YOUR_API_KEY)

#     print(r, type(r), r.json())

from mailgun import MailgunApi

mailgun =  MailgunApi(domain=YOUR_DOMAIN_NAME, api_key=YOUR_API_KEY)
r = mailgun.send_email(to='greatabel2@126.com',
                   subject='Hello',
                   text='Testing some Mailgun awesomeness!')
print(r.json())