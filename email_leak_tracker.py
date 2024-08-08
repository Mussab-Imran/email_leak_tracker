import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

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
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
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
                # make a directory with the name of the subject
                # folder_name = clean(value)
                # we will also handle emails with the same subject name
                # folder_counter = 0
                # while os.path.isdir(folder_name):
                #     folder_counter += 1
                #     # we have the same folder name, add a number next to it
                #     if folder_name[-1].isdigit() and folder_name[-2] == "_":
                #         folder_name = f"{folder_name[:-2]}_{folder_counter}"
                #     elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                #         folder_name = f"{folder_name[:-3]}_{folder_counter}"
                #     else:
                #         folder_name = f"{folder_name}_{folder_counter}"
                # os.mkdir(folder_name)
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
        # if not os.path.isdir(folder_name):
        #     os.mkdir(folder_name)
        print("No Subject")

    parse_parts(service, parts, message)
    print("="*50)

# TODO Add the ability to search within a date range
    # User specified range or last week?
def search_messages(service, query):
    # Takes in a search query and searches the User's inbox to find email with the query
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

# TODO Add a flag message function
def flag_message(message):
   print("flag message")

# TODO Add a check sender function
def check_sender(message):
   print("check sender")

# TODO Add a add sender function
def add_sender():
   print("add sender")

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
    message_array = search_messages(service, "unsubscribe")
    read_message(service, message_array[0])
    print(message_array[0])

  except HttpError as error:
    print("ERROR")
    exit(1)

#   try:
#     # Call the Gmail API
#     service = build("gmail", "v1", credentials=creds)
#     results = service.users().labels().list(userId="me").execute()
#     labels = results.get("labels", [])
#     search_messages()

#     if not labels:
#       print("No labels found.")
#       return
#     print("Labels:")
#     for label in labels:
#       print(label["name"])

#   except HttpError as error:
#     # TODO(developer) - Handle errors from gmail API.
#     print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

# TODO Create a list of green senders
    # JSON file that gets converted to objects on load to be able to be converted into a dictionary

# TODO Add a menu option?
