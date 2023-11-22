#!/usr/bin/env python3
import os, sys

class Task:
	steps = []
	duration = 0
	project = ''
	type = ''
	def __init__(self, _id):
		self.id = _id

	def addstep(self, step):
		self.steps.append(step)

	def setduration(self, _duration):
		self.duration = _duration

	def setproject(self, _project):
		self.project = _project

	def settype(self, _type):
		self.type = _type

	def getid(self):
		return self.id

	def getduration(self):
		return self.duration

	def getproject(self):
		return self.project

	def gettype(self):
		return self.type

class Step:
	def __init__(self, _name, _duration, _id):
		self.name = _name
		self.duration = _duration
		self.taskid = _id

	def getname(self):
		return self.name

	def getduration(self):
		return self.duration

	def getid(self):
		return self.taskid

def main():
	intermediatelist = {}
	intermediatestepslist = {}
	file = sys.argv[1]

	with open(file, 'r') as f:
		print("################################################################################################")
		print("Reading file " + file )
		lines = f.readlines()
		
		for line in lines:
			t = None
			try:
				if line.find('Execute task') > -1:
					id = line.split('id=')[1].split('|')[0].strip()
					t = Task(id)
					intermediatelist[id] = t
					if line.find('type=') > -1:
						t.settype(line.split('type=')[1].split('|')[0].strip())
					if line.find('project=') > -1:
						t.setproject(line.split('project=')[1].split('|')[0].strip())
					intermediatestepslist[id] = []
				if line.find('[o.s.c.t.s.ComputationStepExecutor]') > -1:
					if len(intermediatelist)> 0:
						l = line.split('[o.s.c.t.s.ComputationStepExecutor]')
						name = l[1].split('|')[0]
						taskid = l[0].split('[')[1].replace(']', '')
						duration = int(line.split('time=')[1].replace('ms', ''))
						step = Step(name, duration, taskid)
						intermediatestepslist[taskid].append(step)
				if line.find('Executed task') > -1:
					if len(intermediatelist)> 0:
						l = line.split('[o.s.c.t.CeWorkerImpl]')
						taskid = l[0].split('[')[1].replace(']', '')
						duration = int(line.split('time=')[1].replace('ms', ''))
						intermediatelist[taskid].setduration(duration)
			except:
				pass

	print("Done reading file.")
	print("################################################################################################")
	print("")


	A = dict(sorted(intermediatelist.items(), key=lambda x: x[1].getduration(), reverse=True))

	#set the number of tasks we want to see in the output
	n = 5

	#get the first n tasks as set above
	first_n_tasks = list(A.values())[:n]
	i = 1
	print("################################################################################################")
	print("Top "+str(n)+" longer tasks along with their 3 longer steps in the "+ file +" file:")
	print("")
	for task in first_n_tasks:
		for key in intermediatestepslist:
			if key == task.getid():
				task.addstep(intermediatestepslist[key])


		print("Task #"+str(i)+":\n Project: " + task.getproject() + ", task id: " + task.getid() + " ran for " + str(task.getduration())+"ms => " + str(round(task.getduration()/(60*1000),2)) + "minutes")
		task.steps[0].sort(key=lambda s: s.duration)
		print("\t--------->" + task.steps[0][-1].getname() + " " + str(task.steps[0][-1].getduration())+"ms => " + str(round(task.steps[0][-1].getduration()/(60*1000),2)) + "minutes, " + str(round(task.steps[0][-1].getduration()/task.getduration()*100, 2))+"%")
		print("\t--------->" + task.steps[0][-2].getname() + " " + str(task.steps[0][-2].getduration())+"ms => " + str(round(task.steps[0][-2].getduration()/(60*1000),2)) + "minutes, " + str(round(task.steps[0][-2].getduration()/task.getduration()*100, 2))+"%")
		if task.gettype() == 'REPORT':
			print("\t--------->" + task.steps[0][-3].getname() + " " + str(task.steps[0][-3].getduration())+"ms => " + str(round(task.steps[0][-3].getduration()/(60*1000),2)) + "minutes, " + str(round(task.steps[0][-3].getduration()/task.getduration()*100, 2))+"%")
		print("")
		task.steps.pop()
		i = i + 1

if __name__=='__main__':
	main()