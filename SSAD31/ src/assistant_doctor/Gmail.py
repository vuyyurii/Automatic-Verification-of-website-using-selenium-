from __future__ import print_function
import base64
import email
from apiclient import errors
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


# For retrieving content of a mail using GMAIL API
class Gmail_Api():

    def get_credentials(self):
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        return creds

    def initialize(self):
        global GMAIL
        creds = self.get_credentials()
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    def ListMessagesMatchingQuery(self, user_id, query):
        try:
            response = GMAIL.users().messages().list(userId=user_id,
                                                     q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = GMAIL.users().messages().list(userId=user_id, q=query,
                                                         pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_required(self, user_id, m_id, data, fu):
        try:
            message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
            a = message['payload']['body']['data']
            b = base64.urlsafe_b64decode(a.encode('ASCII'))
            c = b.split('<br />')
            for i in c:
                if "Password" in i:
                    d = i.split('<strong>')
                    e = d[1].split('</strong>')
                    pas = e[0]
                if "Login" in i:
                    f = i.split('<strong>')
                    g = f[1].split('</strong>')
                    log = g[0]
            # print(fu)
            data[fu].append({'username': log, 'password': pas})

        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def get_allrequired(self, user_id, query, data, fu):
        messages = self.ListMessagesMatchingQuery(user_id, query)
        length = messages.__len__()
        for i in range(length):
            self.get_required(user_id, messages[i]['id'], data, fu)
            self.update_flag(user_id, messages[i]['id'])

    def update_flag(self, user_id, m_id):
        try:
            message = GMAIL.users().messages().modify(userId=user_id, id=m_id,
                                                      body={'removeLabelIds': ['UNREAD'], 'addLabelIds': []}).execute()
            label_ids = message['labelIds']
            # print('Message ID: %s - With Label IDs %s' % (id, label_ids))
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
