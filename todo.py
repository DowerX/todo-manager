import yaml
import datetime
import enum
import os
import sys

class Status(enum.Enum):
    PENDING = 1
    STARTED = 2
    COMPLETED = 3

class Job:
    name = ""
    description = ""
    deadline = None
    tags = []
    status = Status.PENDING

    def Create(self, name, description, deadline, tags, status):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.tags = tags
        self.status = status
        return self

    def Load(self, data):
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.deadline = data["deadline"]
            self.tags = data["tags"]
            self.status = data["status"]
        except:
            print("Error while loading Job.")

    def Dump(self):
        data = {
            "name" : self.name,
            "description" : self.description,
            "deadline" : self.deadline,
            "tags" : self.tags,
            "status" : self.status
        }
        return data

class TodoList:
    loadedpath = ""
    jobs = []

    def Load(self, path):
        try:
            if os.path.exists(path):
                self.loadedpath = path
                self.jobs = []
                with open(self.loadedpath, "r") as f:
                    data = yaml.load(f.read(), Loader=yaml.CLoader)
                    for jobdata in data:
                        job = Job()
                        job.Load(jobdata)
                        self.jobs.append(job)
            self.Sort()
        except:
            print("Error while loading TodoList.")

    def Save(self, path):
        try:
            data = []
            for j in self.jobs:
                data.append(j.Dump())

            with open(path, "w+") as f:
                f.write(yaml.dump(data, Dumper=yaml.CDumper))
                self.loadedpath = path
        except:
            print("Error while saving to file.")

    def SearchTags(self, tgs):
        idx = []
        for i, j in enumerate(self.jobs):
            found = True
            for x in tgs:
                if not x in j.tags:
                    found = False
            if found:
                idx.append(i)
        return idx

    def Sort(self):
        self.jobs = sorted(self.jobs, key=lambda i: i.deadline)

class Interface:

    autosave = True
    dateformat = "%Y/%m/%d %H:%M"
    todolist = TodoList()

    def Run(self):
        running = True
        while running:
            try:
                args = input("> ").strip().split(" ")
                if "exit" == args[0]:
                    running = False
                elif "add" == args[0]:
                    self.cmdAdd()
                elif "remove" == args[0]:
                    self.cmdRemove(int(args[1]))
                elif "edit" == args[0]:
                    self.cmdEdit()
                elif "save" == args[0]:
                    self.cmdSave(args)
                elif "autosave" == args[0]:
                    if args[1] == "true":
                        self.autosave = True
                    else:
                        self.autosave = False
                elif "file" == args[0]:
                    self.cmdFile(args[1])
                elif "list" == args[0]:
                    self.cmdList()
                elif "search" == args[0]:
                    self.cmdSearch(args)
                elif "detail" == args[0]:
                    self.cmdDetail(int(args[1]))
            except:
                print("Wrong arguments.")

    def cmdAdd(self):
        name = input("Name: ")
        description = input("Description: ")
        deadline = datetime.datetime.strptime(input("Deadline: "), self.dateformat)
        tags = input("Tags: ").lstrip().rstrip().split(" ")
        status = Status(int(input("Status: ")))

        job = Job().Create(name, description, deadline, tags, status)
        self.todolist.jobs.append(job)
        self.todolist.Sort()
        self.Autosave()

    def cmdRemove(self, i):
        self.todolist.jobs.pop(i)
        self.todolist.Sort()
        self.Autosave()

    def cmdEdit(self):
        i = int(input("Index of job you want to edit: "))
        job = self.todolist.jobs[i]
        print(0, "| Nothing, we are done here")
        print(1, "| Name:", job.name)
        print(2, "| Description:", job.description)
        print(3, "| Deadline:", job.deadline)
        print(4, "| Tags:", job.tags)
        print(5, "| status:", job.status.name)

        done = False
        while not done:
            c = int(input("Which one you want to edit: "))
            if c == 1:
                job.name = input("Name: ")
            elif c == 2:
                job.description = input("Description: ")
            elif c == 3:
                job.deadline = datetime.datetime.strptime(input("Deadline: "), self.dateformat)
            elif c == 4:
                job.tags = input("Tags: ").lstrip().rstrip().split(" ")
            elif c == 5:
                job.status = Status(int(input("Status: ")))
            elif c == 0:
                done = True

        self.todolist.jobs[i] = job
        self.todolist.Sort()
        self.Autosave()

    def cmdSave(self, args):
        if len(args) > 1:
            path = args[1]
        else:
            path = input("Path to save to:")
        self.todolist.Save(path)

    def cmdFile(self, path):
        self.todolist.Load(path)

    def cmdList(self):
        for i, j in enumerate(self.todolist.jobs):
            print(i, "| ", j.name, j.deadline.strftime(self.dateformat))

    def cmdSearch(self, args):
        args.pop(0)
        idx = self.todolist.SearchTags(args)
        for i in idx:
            print(i, "| ", self.todolist.jobs[i].name, self.todolist.jobs[i].deadline.strftime(self.dateformat))

    def cmdDetail(self, i):
        j = self.todolist.jobs[i]
        print(i, "| ", j.name)
        print(j.deadline.strftime(self.dateformat))
        print(j.description)
        print(j.tags)
        print(j.status.name)

    def Autosave(self):
        if self.autosave:
            self.todolist.Save(self.todolist.loadedpath)

if __name__ == "__main__":
    i = Interface()
    i.Run()