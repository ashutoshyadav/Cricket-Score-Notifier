import urllib2
import re
import json
import threading
from win10toast import ToastNotifier 
from pycricbuzz import Cricbuzz


class cricScoreUpdater():

	def __init__(self):
		self.loadInterests()
		self.loadSettings()
		self.cricbuzz = Cricbuzz()
		self.notify = ToastNotifier()
		self.notifyScore()
		print 'To change setting make changes in the cricScoreSettings.txt file'

	def loadSettings(self):
		try:
			f = open('cricScoreSettings.txt','r')
			data = f.readlines()
			data = [x.strip() for x in data]
			self.duration = int(data[0].split(':')[1])
			self.gap = int(data[1].split(':')[1])
			# print self.duration
			# print self.gap
		except:
			self.createDefaultSetting()
			self.loadSettings()

	def notifyScore(self):
		threading.Timer(self.gap,self.notifyScore).start()
		self.showNotifcation(self.getScore())

	def showNotifcation(self,score):
		for item in score:
			res = ''
			for i in xrange(2,len(item)):
				res += str(item[i])+'\n'
			self.notify.show_toast(item[0]+'\n'+item[1],res,duration=self.duration)

	def getScore(self):
		matches = self.cricbuzz.matches()
		score = []
		for match in matches:
			data = self.cricbuzz.livescore(match['id'])
			for team in self.interested_in:
				if (not data['matchinfo']['mchdesc'].find(team[1])==-1) and (data['matchinfo']['mchstate']=='inprogress'):
					temp = []
					temp.append(data['matchinfo']['mchdesc'])
					temp.append(data['matchinfo']['status'])
					for item in data['batting']['score']:
						temp.append(data['batting']['team']+' '+str(item['runs'])+'/'+str(item['wickets'])+' '+str(item['overs'])+' Ovs '+str(item['desc']))
						break
					for item in data['batting']['batsman']:
						temp.append(item['name']+' '+str(item['runs']))
					for item in data['bowling']['bowler']:
						temp.append('Bowler: '+item['name']+' '+str(item['overs'])+'-'+str(item['maidens'])+'-'+str(item['runs'])+'-'+str(item['wickets']))
						break
					score.append(temp)
					break
		return score

	def loadInterests(self):
		self.interested_in = []
		try:
			f = open('interests.txt','r')
			data = f.readlines()
			data = [x.strip() for x in data]
			for item in data:
				self.addInterest(item)
		except:
			self.createDefaultInterestList()
			self.loadInterests()

	def showInterests(self):
		for item in self.interested_in:
			print item

	def addInterest(self,team):
		self.interested_in.append(team)

	def createDefaultInterestList(self):
		f = open("interests.txt",'w')
		f.write('BAN\n')
		f.write("IND\n")
		f.write("AUS\n")
		f.write("ENG\n")
		f.write("SA\n")
		f.write("ZIM\n")
		f.write("AFG\n")
		f.close()

	def createDefaultSetting(self):
		f = open("cricScoreSettings.txt",'w')
		f.write('Notifcation-duration:5\n')
		f.write('Notifcation-gap:15\n')
		f.close()



if __name__=="__main__":
	cricScoreUpdater()