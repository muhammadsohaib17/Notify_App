# # import requests  # Import the requests library to handle HTTP requests

# def get_page_access_token(page_id, user_access_token):
#     """
#     Function to retrieve the Page Access Token using the user access token and page ID.
#     """

#     # Define the Graph API version and construct the API URL to request the Page Access Token
#     version = 'v20.0'
#     api_url_token = f'https://graph.facebook.com/{version}/{page_id}?fields=access_token&access_token={user_access_token}'
    
#     try:
#         # Make a GET request to the Facebook Graph API to fetch the Page Access Token
#         response = requests.get(api_url_token)
#         response.raise_for_status()  # Raise an exception if the request returns an HTTP error

#         # Parse the response as JSON and return the access token
#         data = response.json()
#         return data['access_token']
#     except requests.exceptions.RequestException as e:
#         # Handle any exceptions (e.g., network issues, API errors) and print the error
#         print("Error:", e)
#         return None  # Return None if the access token retrieval fails

# def post_fb(page_id, page_access_token):
#     """
#     Function to publish a post to the Facebook Page using the Page Access Token.
#     """
    
#     message = 'Hello, World'  # The message that will be posted to the Facebook Page
    
#     # Construct the URL for the POST request to the page's feed
#     url = f'https://graph.facebook.com/v20.0/{page_id}/feed'
    
#     # Define the payload (message and access token) that will be sent in the POST request
#     payload = {
#         'message': message,
#         'access_token': page_access_token
#     }
    
#     # Make the POST request to the Facebook Graph API to publish the post
#     response = requests.post(url, data=payload)
    
#     # Check the response status and print a success or failure message accordingly
#     if response.status_code == 200:
#         print("Post successfully published!")
#     else:
#         print(f"Failed to post: {response.status_code}")
#         print(response.json())  # Print the error details from the API response

# # User access token (replace with your actual user access token)
# user_access_token = 'your_access_token_here'

# # Facebook Page ID (replace with your actual page ID)
# page_id = 'your_page_id_here'

# # Retrieve the Page Access Token using the user access token and page ID
# page_access_token = get_page_access_token(page_id, user_access_token)

# # If the Page Access Token was successfully retrieved, publish the post
# if page_access_token:
#     post_fb(page_id, page_access_token)
# else:
#     print("Failed to obtain Page Access Token.")  # Print an error if the token retrieval fails


import email
import imaplib
from email.parser import BytesParser
from email.header import decode_header
import requests
import time
import os 


memail = os.getenv ("msk1734811@gmail.com")
app_pass= os.getenv ("yndupaypaslhuret")
IMAP_SERVER = ("imap.gmail.com")


keywords= ["jobs", "hiring", "vacancy", "project",
    "salary", "deal", "wage", "account", "linked", "hats", "weekly"]

Telegram_chat_ID= os.getenv("7575524175")
Telegram_Bot_Token = os.getenv("7950022254:AAGD34I85A5L3GjeHnvBRy9-SDzIn21PV70")


def tele(text):
    try: 
        url= f"https://api.telegram.org/bot{Telegram_Bot_Token}/sendMessage"
        data= {"chat_id" : Telegram_chat_ID, "text": text}
        requests.post(url, data= data, timeout=10)
    except requests.exceptions.RequestException as e:
        print("telegram error", e)


def keyword_match(text):
    text = text.lower()
    return any (k in text for k in keywords)

def read_mails():
    mail= imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(memail, app_pass)
    mail.select("inbox")

    status, message = mail.search(None, "UNSEEN")
    email_ids= message[0].split()

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg= email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["subject"])[0]
        
        if isinstance (subject, bytes):
            subject= subject.decode(encoding or 'utf-8' )

        body= ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type()=="text/plain":
                    body= part.get_payload(decode=True).decode(errors="ignore")
                    print(body)
                    break
        else:
            body= msg.get_payload(decode=True).decode(errors="ignore")
            print(body)
        
        full_text= f"{subject}{body}"
        print("sending to telegram")

        if keyword_match(full_text):
            send_to_telegram = (f"EMAIL ALERT:\n\n {subject} ")
            tele(full_text)
    mail.logout()

def main(): 
    while True:
        read_mails()
        print("checking done")
        time.sleep(60)

if __name__=="__main__":
    main()