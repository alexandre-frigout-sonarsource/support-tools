for project in projects:
    biggerncloc = 0
    biggerbranch = ''
    try:
        for branch in project.getbranches():
            try:
                rc = requests.get(SQ_URL+NCLOC_API+'?component='project.getkey()'&branch='branch.getname()'&metricKeys=ncloc', auth=AUTH)
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