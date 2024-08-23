Email Leak Tracker 

Overview
The python script works by building a database of past senders who have sent emails that contain the word unsubscribe in them. It then checks the newer emails with the keyword in them to see if the sender is already in the list, if they are, their count gets incremented. Otherwise it will add a label to the email which the user can then view through gmail and decide what to do next.

Features:
- Build Database: Looks at the past emails with a keyword and updates a local json file with the senders and their counts
- List Labels: Lists the label_ID for the labels in a user's gmail account which can then be used in the script to assign appropriate labels to flagged emails
- Run: Runs the script to go over the emails with a specified keyword over a set period of time

Prerequisites
- Python
- Gmail account
- oAuth credentials

Clone the repository:

bash
Copy code
git clone https://github.com/username/repository.git
Navigate to the project directory:

bash
Copy code
cd repository
Install dependencies:

bash
Copy code
npm install
Additional setup: Include any additional setup steps if necessary.

Usage
Provide instructions and examples for using the project. Include code snippets or command-line instructions as needed.

Basic usage:

bash
Copy code
npm start
Example code:

javascript
Copy code
const example = require('example');
example.doSomething();
Configuration
Describe any configuration options or environment variables that can be set up to customize the project.

Environment 
Variables:

ENV_VAR_NAME: Description of what this variable does.
Configuration Files:

config.json: Description of the configuration file and its purpose.
Contributing
If applicable, outline the guidelines for contributing to the project. Include instructions for reporting issues, submitting pull requests, or following a code of conduct.

Fork the repository
Create a new branch
bash
Copy code
git checkout -b feature-branch
Make your changes and commit
bash
Copy code
git commit -am 'Add new feature'
Push to the branch
bash
Copy code
git push origin feature-branch
Create a pull request
License
Specify the license under which the project is distributed. Include a brief summary of the license terms and a link to the full license text.

This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Provide contact information for users who have questions or need support.

Author: Your Name
GitHub: username
