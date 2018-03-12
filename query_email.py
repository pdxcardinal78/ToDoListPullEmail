import pyodbc
import pandas as pd

# sql_login_info = input('Please Enter Password: ')
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=sql-prod;"
                      "Database=uniPoint_CompanyH;"
                      "Trusted_Connection=yes;"
                      "uid=ryanj;"
                      "pwd=sql_login_info")


df = pd.read_sql_query("SELECT TaskUserID, TaskDescription, COUNT(TaskItemType) as Tasks \
  FROM [uniPoint_CompanyH].[dbo].[PT_Todo] \
  Where TaskStatus = 'Active' \
  Group By TaskUserID, TaskDescription \
  Order By TaskUserID", cnxn)


def message_creation():
    user = None
    for index, i in df.iterrows():

        if user != i['TaskUserID'] and user is not None:

            email_task_user(new_df.to_html(), i['TaskUserID'])
            new_df = pd.DataFrame(columns=('TaskUserID', 'TaskDescription', 'TaskCount'))
            new_df = new_df.append({'TaskUserID': i['TaskUserID'], 'TaskDescription': i['TaskDescription'], 'TaskCount':
                i['Tasks']}, ignore_index=True)

            user = i['TaskUserID']

        elif user != i['TaskUserID']:
            new_df = pd.DataFrame(columns=('TaskUserID', 'TaskDescription', 'TaskCount'))
            new_df = new_df.append({'TaskUserID': i['TaskUserID'], 'TaskDescription': i['TaskDescription'], 'TaskCount':
            i['Tasks']}, ignore_index=True)

            user = i['TaskUserID']

        elif i['TaskUserID'] == user:
            new_df = new_df.append({'TaskUserID': i['TaskUserID'], 'TaskDescription': i['TaskDescription'],
            'TaskCount': i['Tasks']}, ignore_index=True)

            message = str('Subject: Weekly Task Items ' + '\n')


# Method for sending out the email using the Dataframe for the individual employee generated in message creation.
def email_task_user(new_df_html):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import passkeys as pk

    you = 'youremailhere@email.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Active ToDo List Items"
    msg['From'] = 'Benchmade uniPoint'
    msg['To'] = you

# Body of Email the Message
    text = 'Having Trouble printing out your weekly to do list. Please check uniPoint for more info.'
    html = """\
    <html>
      <head></head>
      <body>
        <p>Here is the list of items currently on your ToDo List. Please log into uniPoint to review your list. </p>
        <br>
        {code}
      </body>
    </html>
    """.format(code=new_df_html)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    # smtpObj = smtplib.SMTP('mail.benchmade.com', 25)
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('gmailaccounthere@gmail.com   ', pk.login_info) # Enter Email Account Here
    smtpObj.sendmail('gmailacounthere@gmail.com', you, msg.as_string()) # Here From and To email accounts here.
    smtpObj.quit()


message_creation()
