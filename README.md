# one-click-cold-emails
A resourceful one-click-run tool to use to help in job hunting

Cold Emails are one of the integral parts of the jon hunting process for anyone. When dealing with the same process, It was evident that emailing everyone separately is a very tedious task and can be cumbersome. So I put on my automation hat and tried ease out the email sending process,assuming the same email content is to be sent to every recipient.

There are two yml files:
- main_email_list.yaml - This is where all the recipient info goes in. Please follow the same yaml file format which is shown in the commented examples.
- sender_info.yaml - This is where the sender info is stored. Follow the same format to store your email credentials.


PS - If your (professional) email provider does not allow a code based email sending facility. Please reach out to them for an SMTP relay information which will allow you to mask your personal email with the professional one.


## Update v1.1 (5/21/2024) - 

- Added another (easier) way to do make cold emailing more faster and trackable with reduced manual intervention and enhanced email message customization.
  - Now the script ""SendColdEmailsFromExcel.py" uses an excel file with the schema like shown in "ColdEmailTrackingSample.xlsx".
  - Instructions to fill the excel sheet:
    - Enter "FirstName <space> LastName" in the first column, email in the second, and so on.
    - Leave the job postings column as **blank** if you do not have a relevant open job post link for that company.
    - **Save and close the excel file** after you are done with new additions. If you do not do this, you will have to update the email sent statuses of all the new recipients manually as the script requires the file to be available to write programatically which won't be possible if it is open.
    - Always check for logs in the "cold_email_logs.log" file for any errors / bugs. Detailed logs have been inculcated for a reason.
- You can now add additional text having links to relevant job descriptions with the email message now. (See sub-point 2.2 above)

If you have any suggestions / feedback, please find me on (LinkedIn)[https://www.linkedin.com/in/attharvaj3147/] here.
