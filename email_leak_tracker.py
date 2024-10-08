import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def parse_parts(service, parts, message):
    """
    Utility function that parses the content of an email partition
    """
    textAttachments = 0
    htmlAttachments = 0
    otherAttachments = 0

    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), message)
            if mimeType == "text/plain":
                # if the email part is text plain
                text = urlsafe_b64decode(data).decode()
                # print(text)
                if data:
                    text = urlsafe_b64decode(data).decode()
                    # print(text)
                    textAttachments+=1
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                htmlAttachments+=1
                # if not filename:
                #     filename = "index.html"
                # filepath = os.path.join(folder_name, filename)
                # print("Saving HTML to", filepath)
                # with open(filepath, "wb") as f:
                #     f.write(urlsafe_b64decode(data))
            else:
                # attachment other than a plain text or HTML
                otherAttachments+=1
                # for part_header in part_headers:
                #     part_header_name = part_header.get("name")
                #     part_header_value = part_header.get("value")
                #     if part_header_name == "Content-Disposition":
                #         if "attachment" in part_header_value:
                #             # we get the attachment ID 
                #             # and make another request to get the attachment itself
                #             print("Saving the file:", filename, "size:", get_size_format(file_size))
                #             attachment_id = body.get("attachmentId")
                #             attachment = service.users().messages() \
                #                         .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                #             data = attachment.get("data")
                #             filepath = os.path.join(folder_name, filename)
                #             if data:
                #                 with open(filepath, "wb") as f:
                #                     f.write(urlsafe_b64decode(data))

def read_message(service, message):
    # This function breaks a particular email to its smaller parts and prints them
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        print("No Subject")

    parse_parts(service, parts, message)
    print("="*50)

def parse_message_parts(service, parts, message, search_term):
    """
    Utility function that parses the content of an email partition
    """
    textAttachments = 0
    htmlAttachments = 0
    otherAttachments = 0

    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_message_parts(service, part.get("parts"), message, search_term)
            if mimeType == "text/plain":
                # if the email part is text plain
                # print("IS TEXT")
                text = urlsafe_b64decode(data).decode()
                # print(text)
                # if data:
                #     text = urlsafe_b64decode(data).decode()
                #     email_body = text.lower()
                #     textAttachments+=1
                #     if search_term.lower() in email_body:
                #        print("PRESENT TEXT")
                #     else:
                #        print("NAAAH TEXT")
                    
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # decodes the html to text and then searches if html has search_term in it
                # print("IS HTML")
                text = urlsafe_b64decode(data).decode()
                # print(text)
                # htmlAttachments+=1
                # if data:
                #     text = urlsafe_b64decode(data).decode()
                #     email_body = text.lower()
                #     textAttachments+=1
                #     if search_term.lower() in email_body:
                #        print("PRESENT HTML")
                #     else:
                #        print("NAAAH HTML")
            else:
                # attachment other than a plain text or HTML
                otherAttachments+=1
                # print("OTHER ATTACHMENT")
    else:
        # print(message)
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # email_body = json.dumps(msg)
        # if "unsubscribe" in email_body:
        #     print("PRESENT ELSE")
        # else:
        #     print("NAAH ELSE")

def search_messages(service, message_array, search_term):
    # This function takes a list of messages and returns a list of only those messages that contain a specific 
    # search term
    for message in message_array:
        # This function breaks a particular email to its smaller parts and prints them
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # parts can be the message body, or attachments
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        has_subject = False
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                    email = get_email(value)
                    add_sender(email, service, message['id'], "Label_3203579961078862081")
                # if name.lower() == "to":
                #     # we print the To address
                #     print("To:", value)
                if name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    has_subject = True
                #     # make a directory with the name of the subject
                #     print("Subject:", value)
                # if name.lower() == "date":
                #     # we print the date when the message was sent
                #     print("Date:", value)
        if not has_subject:
            print("No Subject!")

        parse_message_parts(service, parts, message, search_term)
        print("="*50)
    

def filter_messages(service, query):
    # Takes in a search query and searches the User's inbox to find email with the query
    # Search query can be a particular word or date range ("newer_than:7d") or ("Unsubscribe")
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

# TODO Add a flag message function to add label to an email
def flag_message(service, message_id, label_id):
    # msg = service.users().messages().modify(
    #     userId='me',
    #     id=message_id,
    #     body={
    #         'addLabelIds': [label_id]
    #     }
    # ).execute()
    # print(f"Label added to email: {msg}")
    label_body = {
    'removeLabelIds': ['INBOX'],
    'addLabelIds': [label_id]
    }
    service.users().messages().modify(userId='me', id=message_id, body=label_body ).execute()

# TODO Add a sender to the json file and flag the 
# appropriate email with a label
def add_sender(email, service, message_id, label_id):
    # Load the existing data from the JSON file
    json_file_path = 'sender_list.json'
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            email_counts = json.load(file)
    else:
        email_counts = {}

    # Update the count for the received email
    if email in email_counts:
        email_counts[email] += 1
        if email_counts[email] <= 3:
            flag_message(service, message_id, label_id)
            print(email)        
    else:
        email_counts[email] = 1
        flag_message(service, message_id, label_id)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(email_counts, file, indent=4)

def get_email(email):
    # initializing substrings
    sub1 = "<"
    sub2 = ">"
    
    # getting index of substrings
    idx1 = email.index(sub1)
    idx2 = email.index(sub2)
    
    # length of substring 1 is added to
    # get string from next character
    res = email[idx1 + len(sub1): idx2]

    return(res)

def list_labels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(f"{label['name']} ({label['id']})")
    return labels


def main():
  """
    START - Initial setup
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  """
    END - Initial setup
  """
  try:
    service = build('gmail', 'v1', credentials=creds)
    # list_labels(service)
    message_array = filter_messages(service, "newer_than:7d unsubscribe")
    search_messages(service, message_array, "unsubscribe")
    # read_message(service, message_array[3])
    # flag_message(service, , "Label_3203579961078862081")
    # print(len(message_array))

  except HttpError as error:
    print(HttpError)
    print("ERROR")
    exit(1)

if __name__ == "__main__":
  main()

# TODO Create a list of green senders
    # JSON file that gets converted to objects on load to be able to be converted into a dictionary

# TODO Add a menu option?
