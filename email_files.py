import win32com.client
import os
from datetime import datetime

def email_file_path(subject_keyword, save_folder : str = None):
    outlook =  win32com.client.Dispatch("Outlook.Application").GetNamespace('MAPI')
    inbox = outlook.GetDefaultFolder(6) # 6 corresponds to the inbox
    last_email =  None
    file_path = None
    filter_date = datetime.combine(datetime.today(), datetime.min.time()).strftime("%Y-%m-%d %H:%M:%S")

    emails = inbox.Items.Restrict(f"@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"" LIKE '%s' AND " 
                                    f"\"urn:schemas:httpmail:datereceived\" > '{filter_date}'" % subject_keyword)
    for email in emails:
        try:
            if last_email is None or email.ReceivedTime > last_email.ReceivedTime:
                last_email = email
        except AttributeError as e:
            print(f'Error>>processing an email: {e}')
            continue

    if last_email:
        print(f"Last email details - Sender: {last_email.SenderEmailAddress}, Subject: {last_email.Subject}, Received Time: {last_email.ReceivedTime}")
        if last_email.Attachments.Count > 0:
            for attachment in last_email.Attachments:
                if attachment.FileName.endswith('.xlsx'):
                    file_path = os.path.join(save_folder, attachment.FileName)
                    attachment.SaveAsFile(file_path)
        else:
            print("No attachments found in the last email")
    else:
        print("No matching email found")

    return file_path


folder = r'Z:\DWH Load\Islam\src'
result = email_file_path('Daily VAS%',folder)
print(result)
