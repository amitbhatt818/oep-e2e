from api_request.request import *
from group.group import *

class Invite():
   
    def __init__(self, director_url):
        self.base_url = director_url
       
    def invite(self, api_key, api_password, account_id):
        requestobj = Data(api_key, api_password) 
        url = self.base_url
        groupObj = Groups(self.base_url, api_key, api_password)
        id = groupObj.getProjectAccountID()
        # send invite post request
        url = self.base_url + f"/v3/groups/{id}/emailinvitations"
        data = {}
        data['groupId'] = id
        data['inviteeId'] = account_id
        data['kind'] = 'projectInvitation'
        data['role'] = "ProjectMember"
        response = requestobj.post(url, data)
        print("Invite sent")
       
    def isActive(self, api_key, api_password):
        requestobj = Data(api_key, api_password) 
        url = self.base_url + "/v3/emailinvitations"
        response = requestobj.get(url)
        # assuming there is only one invitation
        print(response[0]['state'])
        if response[0]['state'] == 'active':
            return True
        else:
            return False 
        
    def accept(self, api_key, api_password):
        requestobj = Data(api_key, api_password) 
        url = self.base_url + "/v3/emailinvitations"
        response = requestobj.get(url)
        accept_url = response[0]['actions']['accept']
        print(requestobj.post(accept_url, {}))

    def reject(self, api_key, api_password):
        requestobj = Data(api_key, api_password) 
        url = self.base_url + "/v3/emailinvitations"
        response = requestobj.get(url)
        reject_url = response[0]['actions']['reject']
        print(requestobj.post(reject_url, {}))
