Email Leak Tracker 

Overview
The python script works by building a database of past senders who have sent emails that contain the word unsubscribe in them. It then checks the newer emails with the keyword in them to see if the sender is already in the list, if they are, their count gets incremented. Otherwise it will add a label to the email which the user can then view through gmail and decide what to do next.

Features:
- Build Database: Looks at the past emails with a keyword and updates a local json file with the senders and their counts
- List Labels: Lists the label_ID for the labels in a user's gmail account which can then be used in the script to assign appropriate labels to flagged emails
- Run: Runs the script to go over the emails with a specified keyword over a set period of time

Prerequisites:
- Python
- Gmail account
- oAuth credentials

Instruction:


Contact
Provide contact information for users who have questions or need support.

Author: Your Name
GitHub: username
