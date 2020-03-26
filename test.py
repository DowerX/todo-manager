import todo

testJob = {
    "name" : "TestJobName",
    "deadline" : 12345,
    "description" : "SomeDescriptionForTheTestJob",
    "tags" : ["FisrtTag", "SecondTag"]
}

testJob1 = {
    "name" : "TestJobName1",
    "deadline" : 123451,
    "description" : "SomeDescriptionForTheTestJob1",
    "tags" : ["FisrtTag1", "SecondTag1"]
}

todo.jobs.append(testJob)
todo.jobs.append(testJob1)
todo.saveJobs("./jobs.json")
todo.jobs = []
todo.loadJobs("./jobs.json")
print(todo.jobs)

print(todo.searchTags(["FisrtTag", "FisrtTag1"]))