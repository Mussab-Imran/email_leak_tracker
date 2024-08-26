Email Leak Tracker 

Overview
The python script works by building a database of past senders who have sent emails that contain the word unsubscribe in them. It then checks the newer emails with the keyword in them to see if the sender is already in the list, if they are, their count gets incremented. Otherwise it will add a label to the email which the user can then view through gmail and decide what to do next.

Features:
- Build Database: Looks at the past emails with a keyword and updates a local json file with the senders and their counts
- List Labels: Lists the label_ID for the labels in a user's gmail account which can then be used in the script to assign appropriate labels to flagged emails
- Run: Runs the script to go over the emails with a specified keyword over a set period of time

Prerequisites:
- Python 3
- Gmail account
- oAuth credentials

Instruction:
  oAuth Credentials:
  - To generate a credentials file head to https://console.cloud.google.com/apis/dashboard
  - Click on enable APIs and services
  - Navigate to gmail API and click enable
  - Once enabled head to credentials tab in the dashboard and download the appropriate OAuth 2.0 Client ID
  - rename it to credentials.json and place it in the same directory as the python script


Contact
Provide contact information for users who have questions or need support.

Author: Your Name
GitHub: username
