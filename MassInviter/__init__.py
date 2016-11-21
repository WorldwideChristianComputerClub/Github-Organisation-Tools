import json
from requests.auth import HTTPBasicAuth
from requests import put,get

class Inviter:
    def __init__(self,usernames:list,organisation_name:str,organisation_owner_username:str,organisation_owner_password:str):
        self.organisation_name = organisation_name
        self.usernames = usernames
        self.authentication = HTTPBasicAuth(organisation_owner_username, organisation_owner_password)

    def invite_single_user(self, username_to_invite, role="member"): # else role = "admin" - to invite an admin

        response = put("https://api.github.com/orgs/%s/memberships/%s" % (self.organisation_name, username_to_invite), data=json.dumps({"role":role}), auth=self.authentication).text
        print("response is ",response)
        if json.loads(response)['state'] == "pending":
            return True
        else:
            return False

    def invite_all(self):
        for user in self.usernames:
            invite_successful = self.invite_single_user(user)
            if invite_successful:
                print("invitation for user ",user," successful")
            else:
                print("invitation for user ",user," unsuccessful")


class Searcher:
    def __init__(self,search_term:str,organisation_owner_username:str,organisation_owner_password:str):
        self.search_term = search_term
        self.organisation_owner_username = organisation_owner_username
        self.organisation_owner_password = organisation_owner_password

    def get_all_results(self):
        all_results = dict()
        last_result = {"intialise":"initialised for while loop"}
        page = 1
        #  search is limited to 1000 results by github
        #  will return first empty page as well if it finishes early
        while last_result != {'items': [], 'incomplete_results': False, 'total_count': 0} and page != 11:
            page_results = get("https://api.github.com/search/repositories?q=%s&page=%s&per_page=100&sort=stars&order=desc" % (self.search_term,page),auth= HTTPBasicAuth(self.organisation_owner_username, self.organisation_owner_password)).text
            page_results_dict = json.loads(page_results)
            print("results for page ",page)
            print(page_results_dict)
            last_result = json.loads(page_results)
            all_results.update(page_results_dict)
            page += 1
        return all_results

    def get_username_by_project_search_results(self):
        usernames = list()
        for result in self.get_all_results()['items']:
            # print("result item is",result) # uncomment for debug
            try:
                if result['owner']['type'] != "Organization":
                    username = result['owner']['login']
                    usernames.append(username)
            except Exception as e:
                print(e)
                break
        return usernames



if __name__ == __name__:
    search_term = "bible"
    credentials = json.loads(open("private.json").read())
    search = Searcher(search_term,credentials['username'],credentials['password'])
    # search.get_all_results()
    usernames = search.get_username_by_project_search_results()

    print("found usernames are",usernames)
    print("number of usernames found: ",len(usernames))

    inviter = Inviter(usernames,'WorldwideChristianComputerClub',credentials['username'],credentials['password'])

    inviter.invite_all()