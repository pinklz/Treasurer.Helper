# Club Treasurer 
Help visually compare Google form answers w/ payments received

## How To Use
Ensure your csv file with Venmo transaction history is in the same directory as app.py.  
Run command `python3 app.py` to execute main file. Use localhost:5000 to see site.
After filling out the forms (using format described below), it should display a checklist of who filled out the form on the left, with a list of who paid, when, how much, and the payment description listed on the right. Both columns are in alphabetical order for easier comparison.
## Credentials for Google Forms

Add credentials in file 'credentials.json'  
These can be obtained through a Google Cloud project. Add the Google Forms API to your project, and create a new OAuth 2.0 Client ID by following instructions in link below:
https://developers.google.com/forms/api/quickstart/python 
## Landing Page Input Format
The home page requires three input fields  

**Form ID**: in the Google form URL, the form ID is in   
    https://docs.google.com/forms/d/  *FORM ID*  /edit  

**Username**: your full name as it appears in venmo transaction history and on profile, not your username  

**CSV File Name**: the full file name of your transaction history saved to csv file, *including the .csv suffix*
