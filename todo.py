import json
import sys
import os
import datetime

jobs = []
file_path = ""
autosave = True
dateformat = "%Y/%m/%d %H:%M"

def loadJobs(path):
    global jobs
    jobs = []
    data = ""
    try:
        with open(path, "r") as f:
            data = json.loads(f.read())
        for i in data:
            jobs.append(i)
    except:
        pass
    jobs = sorted(jobs, key=lambda i: i["deadline"])

def saveJobs(path):
    try:
        os.remove(path)
    except:
        pass

    with open(path, "w") as f:
        json_data = json.dumps(jobs)
        f.write(json_data)

def searchTags(tags):
    global jobs
    idx = []
    for x in range(len(jobs)):
        j = jobs[x]
        found = True
        for t in tags:
            if not t in j["tags"]:
               found = False 
               break
        if found:
            idx.append(x)
    return idx

def interface():
    global file_path, dateformat
    print("Todo manager")
    while True:
        inp = input(">")
        inp_list = inp.strip().split(" ")
        if inp_list[0] == "add":
            add()
        if inp_list[0] == "remove" or inp_list[0] == "done":
            remove(int(inp_list[1])-1)
        elif inp_list[0] == "list":
            listJobs()
        elif inp_list[0] == "detail":
            detail(int(inp_list[1])-1)
        elif inp_list[0] == "file":
            file_path = inp_list[1]
            loadJobs(file_path)
        elif inp_list[0] == "dateformat":
            dateformat = inp_list[1]
            loadJobs(file_path)
        elif inp_list[0] == "exit" or inp_list[0] == "close" or inp_list[0] == "q":
            return

def add():
    global jobs
    job = {}
    job["name"] = input("Name: ")
    job["description"] = input("Description: ")
    deadline_raw = input("Deadline: ")
    deadline_raw = deadline_raw.strip()
    job["deadline"] = datetime.datetime.strptime(deadline_raw, dateformat).__str__()
    tags_raw = input("Tags: ")
    job["tags"] = tags_raw.strip().split(",")

    jobs.append(job)
    jobs = sorted(jobs, key=lambda i: i["deadline"])
    if autosave:
        saveJobs(file_path)

def remove(i):
    global jobs
    jobs.pop(i)
    if autosave:
        saveJobs(file_path)

def save(inp_list):
    if len(inp_list) > 1:
        saveJobs(inp_list[1])
    else:
        saveJobs(file_path)

def listJobs():
    for i, job in enumerate(jobs):
        print(f"{i+1} | {job['name']} : {job['deadline']}")

def detail(i):
    global jobs
    job = jobs[i]
    print(f'{job["name"]}:\n{job["description"]}, Deadline: {job["deadline"]}\nTags: {job["tags"]}')

def main():
    global file_path, autosave
    for i, arg in enumerate(sys.argv):
        if arg == "-f":
            try:
                file_path = sys.argv[i+1]
            except:
                print("Wrong args!")
        elif arg == "-na":
            autosave = False

    if not file_path == "":
        try:
            loadJobs(file_path)
        except:
            print("Couldn't load in file!")
    
    interface()

if __name__ == "__main__":
    main()