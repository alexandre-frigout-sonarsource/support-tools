import requests
import sys


class Branch:
    def __init__(self, _name):
        self.name = _name
        self.ncloc = 0
        self.idbigger = False

    def setncloc(self, _ncloc):
        self.ncloc = int(_ncloc)

    def getncloc(self):
        return self.ncloc

    def getname(self):
        return self.name

    def setbigger(self):
        self.idbigger = True

    def getisbigger(self):
        return self.idbigger


class Project:
    def __init__(self, _key):
        self.key =_key
        self.branches = []

    def addbranch(self, branch):
        self.branches.append(branch)

    def getbranches(self):
        return self.branches

    def getkey(self):
        return self.key


#Page size
PS = 500

#API's used
SQ_URL = 'http://localhost:9000/'
PROJECTS_API = 'api/projects/search?qualifiers=TRK&ps='+str(PS)
BRANCHES_LIST_API = 'api/project_branches/list'
NCLOC_API = 'api/measures/component'

#Credentials
AUTH = ('admin', 'admin1')

try:
    print("Getting projects list...")
    print(SQ_URL+PROJECTS_API)
    r = requests.get(SQ_URL+PROJECTS_API, auth=AUTH)
    if r.status_code != 200:
        print("response from sonarqube:", r.status_code)
        sys.exit(1)
    components = []
    total = int(r.json()['paging']['total'])
    ps = int(r.json()['paging']['pageSize'])
    index = r.json()['paging']['pageIndex']
    for component in r.json()['components']:
        components.append(component)

    if ps < total:
        while int(index) <= total // ps:
            index = index + 1
            t = requests.get(SQ_URL + PROJECTS_API + '&p=' + str(index), auth=AUTH)
            for component in t.json()['components']:
                components.append(component)
except Exception as e:
    print(e)
    sys.exit(2)

print("There are {} projects in your SonarQube instance".format(len(components)))

projects = []

print("Getting branches for all projects...")
for component in components:
    try:
        P = Project(component['key'])
        brs = requests.get(SQ_URL+BRANCHES_LIST_API+'?project='+component['key'], auth=AUTH)
        for br in brs.json()['branches']:
            B = Branch(str(br['name']))
            P.addbranch(B)
        projects.append(P)
    except ConnectionError as e:
        pass

totalncloc = 0
print("Counting the number of lines of code...")
for project in projects:
    biggerncloc = 0
    biggerbranch = ''
    try:
        for branch in project.getbranches():
            try:
                ncloc = requests.get(SQ_URL+NCLOC_API+'?component='+project.getkey()+'&branch='+branch.getname()+'&metricKeys=ncloc', auth=AUTH)
                if rc.status_code == 200:
                    measures_list = rc.json()['component']['measures']
                    if len(measures_list) == 1:
                        branch.setncloc(measures_list[0]['value'])
                    else:
                        branch.setncloc(0)
                else:
                    branch.setncloc(0)
            except ConnectionError as c:
                pass
            if branch.getncloc() > biggerncloc:
                biggerncloc = branch.getncloc()
                biggerbranch = branch.getname()

        #printing the biggest branch of the project along with its ncloc
        print(project.getkey(), biggerbranch, biggerncloc)
        totalncloc = totalncloc + biggerncloc
    except Exception as e:
        pass

print("Total nuumber of lines of code in your SonarQube instance:", totalncloc)

