from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException
import csv
import sys
import threading

from random import randint

firstNameList =[]
lastNameList=[]
emailList = ['@gmail.com','@yahoo.com', '@msn.com', '@hotmail.com', '@live.com' ]

#Read the CSV files
with open('first_names.csv') as firstNameFile:
	reader = csv.reader(firstNameFile, delimiter=',')
	for row in reader:
		firstNameList.append(row)
print('all first names read: '+ str(len(firstNameList)) +' entries')

with open('last_names.csv') as lastNameFile:
	reader = csv.reader(lastNameFile, delimiter=',')
	for row in reader:
		lastNameList.append(row)
print('all last names read: '+ str(len(lastNameList)) +' entries')
	
class myThread (threading.Thread):
	def __init__(self, threadID, name, counter, voteCounter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.voteCounter = voteCounter
	def run(self):
		print ("Starting " + self.name)
		vote(self.name, self.voteCounter)
		print ("Exiting " + self.name)
	
		
def vote(threadName, voteCount):
	driver = webdriver.Firefox()
	counter =0
	while counter<voteCount:
		try: 
			FirstName = firstNameList[randint(0, len(firstNameList)-1)][0]
			LastName = lastNameList[randint(0,len(lastNameList)-1)][0]
			domain = emailList[randint(0, len(emailList)-1)]
			email = FirstName+'.'+LastName+domain
			
			print(threadName+'| email: ' +email)
			
			driver.get("https://wayup.pgtb.me/RnZkMG/pbk2V?w=68637949&e=193935051")

			driver.implicitly_wait(5)
			driver.maximize_window()

			#vote_button = driver.find_element_by_css_selector("div.ss_item_main_action_container.item_vote")
			vote_button = driver.find_element_by_xpath('//*[@id="my_db_entry_193935051"]/div[3]')
			vote_button.click()

			driver.implicitly_wait(5)

			first_button = driver.find_element_by_name("form3[first_name]")
			first_button.send_keys(FirstName)


			last_button = driver.find_element_by_name("form3[last_name]")
			last_button.send_keys(LastName)


			email_field = driver.find_element_by_name("form3[email]")
			email_field.send_keys(email)

			check = driver.find_element_by_xpath("//*[@id='form3_custom_field_5_block']/label/span[1]")
			check.click()


			finish = driver.find_element_by_css_selector("#form3_submit_block")
			finish.click()
			
			if (int(counter )% 100 == 0) and (counter >0):
				print('added '+ str(counter) + ' entries')
			
			counter = counter+1
			
		except (KeyboardInterrupt, SystemExit):
			print('Finished: added '+ str(counter) + ' entries')
			exit()
		except SessionNotCreatedException:
			print('browser closed')
			exit()
		except:
			print('error'+str(sys.exc_info()[0]))


	
	
threadCount = int(input('How many threads?'))
voteCount = int(input('How many votes per thread?'))

for i in range(threadCount) :
	threadName = "thread"+str(i)
	currentThread = myThread(i, threadName, i, voteCount)
	currentThread.start()
	

