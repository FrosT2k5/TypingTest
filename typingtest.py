import curses
from curses import wrapper
import time
from colorama import Fore,Style
import json
import requests
from urllib.parse import unquote
from os.path import isfile
import os

#This function fetches and prints leaderboards
def leaderboards():
	try:
		txt = requests.get("http://frost.alwaysdata.net/scorelog.txt").text
	except:
		print(f"{Fore.RED}Failed to get leaderboards list, please check your internet connection{Style.RESET_ALL}")
		input()
		return 0

	txtfile = open(".scores.txt","w")
	txtfile.write(txt)
	txtfile.close()

	txtfile = open(".scores.txt","r")
	lines = txtfile.read().splitlines()
	txtfile.close()

	clr()
	scoredict = {}
	for line in lines:
		if "," in line:
			scr = line.split(",",1)
			nam = unquote(scr[0])
			try:
				score = int(scr[1])
			except: #Don't break if a line is incorrect by mistake...
				None 
			scoredict[nam] = score
		else:
			None
	
	scorelist = sorted(scoredict.items(),reverse=True,key=lambda kv:(kv[1]))
	x = 0

	print(Fore.YELLOW,"Top 15 Typers of FrosT's TypingTest!")
	print(Fore.GREEN,"Congratulations to all the fast typers\nScore is in WPM(Words Per Minute)\n\n\n",Style.RESET_ALL)

	while x<=15:	
		try:
			print(f' -  {scorelist[x][0]} - {scorelist[x][1]} WPM!')
			time.sleep(0.2)
		except IndexError:
			break
		x+=1
	input()


#This function is used to setup configuration
def config():
	if isfile(".config.json"):
		print(Fore.RED,"Previously saved config found!, overwriting",Style.RESET_ALL)
		f = open(".config.json",'r')
		co = json.load(f)
		bestscore = co['bestscore']
		score = co['score']
		f.close()

	else:
		bestscore = 0
		score = 0
	name = input("Enter your name: ")
	conf ={
		"name": name,
		"bestscore": bestscore,
		'score': score
	}

	confile = open(".config.json","w")
	json.dump(conf,confile,indent="    ")
	confile.close()

# Clear screen
def clr():
    time.sleep(0.2)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Check input, using this instead of ord directly prevents crashing on changing resolution
def checkkey(key):
	try:
		return ord(key)
	except TypeError:
		return None

def qslice(string,ind):
	#This function slices the given string into 50 characters with ind as index of the sliced string
 	st = []
 	for i in range(0,len(string),49):
 		st.append(string[i:i+49]) #Split string to list sl which has 49 characters in each element
 	try:
 		print(len(st[1]))
 		return st[ind]
 	except IndexError:
 		return None

#Result function
def result(spd,mistakes):
	curses.endwin()
	if not isfile(".config.json"):
		print(f"{Fore.RED}No local config found, generating...{Style.RESET_ALL}")
		config()


	print(f"\n\n{Fore.GREEN}Your speed is: {spd}WPM! \n Your mistakes: {mistakes} \n {Fore.RED}Each mistake reduces 0.5 second of your speed",Style.RESET_ALL)
	spd = round(spd - 0.5*mistakes)
	print(Fore.BLUE,f"So, your actual speed is: {spd}",Style.RESET_ALL)
	confile = open(".config.json",'r')
	conf = json.load(confile)
	confile.close()

	name = conf["name"]
	conf["score"] = spd
	bestscore = conf["bestscore"]
	if spd > bestscore:
		print("Highscore!")
		conf["bestscore"] = spd

	confile = open(".config.json","w")
	json.dump(conf,confile,indent=6)
	confile.close()

	ck = input(f"{Fore.BLUE}Do you want to submit your score in leaderboards?{Style.RESET_ALL}(Y/n)")
	if spd >= 230:
		print(Fore.RED,"Looks like you cheated! If u didn't then contact me @FrosT2k5",Style.RESET_ALL)
		ck = "n"
		input()
	if ck == "y" or ck == "Y":
		try:
			n = requests.get(f"http://frost.alwaysdata.net/leaderboards.php?{name},{spd}")
		except:
			print(Fore.RED,"Please check your internet connection...",Style.RESET_ALL)
			input()
	leaderboards()

def main(stdsrc):
	stdsrc.clear()

	#Colors
	curses.init_pair(1,curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(4,curses.COLOR_YELLOW, curses.COLOR_BLACK)
	blue = curses.color_pair(1)
	green = curses.color_pair(2)
	red = curses.color_pair(3)
	yellow = curses.color_pair(4)


	# Get center co-ordinates of the display screen
	y = curses.LINES // 2
	x = curses.COLS // 2

	# Initialize windows
	q = curses.newwin(7,50,y,x-25) #This will print the query 
	txt = curses.newwin(1,50,y+1,x-25) #User will type here
	counters = curses.newwin(3,15,2,x-25) #This will print the statistics(mistakes and speed)
	#warns = curses.newwin(1,100,15,20) #This will contain debugging text or warning

	# This function updates the user input window txt according to qslice
	def updatetxt(str):
		txt.clear()
		txt.addstr(0,0,str)
		txt.move(0,0)
		txt.refresh()


	# Same as updatetxt, but updates for the user query window,q
	def updateq(str,str2,str3):
		q.clear()
		q.addstr(0,0,str,blue)
		try:
			q.addstr(3,0,str2,yellow)
			q.addstr(5,0,str3,yellow)
		except TypeError: #Don't crash if it's end of the question string
			None
		q.refresh()


	# Print counters
	counters.addstr(0,0,"Wrong: 0",blue)
	counters.addstr(2,0,"Speed: 0WPM",blue)
	counters.refresh()

	#The question string
	easy = "A quick brown fox jumps over the lazy dog. Far far away, behind the word mountains, far from the countries Vokalia and Consonantia there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."

	
	# Initialize the First string slice
	sl = 0 # Index of string qslice
	# Get the first slice of question
	query = qslice(easy,0)
	sl += 1 # We got the first slice
	updateq(query,qslice(easy,sl),qslice(easy,sl+1)) #Get next and +2 string of query to print below the user input
	updatetxt(query)
	

	i = 0 # It's probably some loop coz i :p
	which = 1 # Stores which text index of query is going on
	inp = [] #List of words user entered
	stime = time.perf_counter()
	while True:
		txt.refresh()
		key = txt.getkey() #Get user input

		if checkkey(key) == 127: #Back Key
			i -= 1
			key = ""
			txt.addstr(0,i,key)
			inp.pop() #Remove the last character

		elif checkkey(key) in (10,13): #Enter and arrow keys
			None

		else: #Process the input
			try:
				if query[i] == key:
					txt.addstr(0,i,key,green) #Green if user input is right
					i += 1
				else:
					txt.addstr(0,i,key,red) #Red if user input is wrong
					i += 1
				inp.append(key) #Append the character user entered
			except IndexError: #IndexError means question ended
				stdsrc.clear() #Clear for normal output next to this
				result(spd,mistakes)
				break
				# String Slice handler

		# After every iteration, update Speed and Mistakes:
		st = "" #Make string from the inp list
		mistakes = 0 # Start with 0 Mistakes
		cind = 0 # Custom index which will hold absolute index number
		for j in inp:
			if j != easy[cind]:
				mistakes += 1
			cind +=	1
			st += j
		newinp = st.split(" ") #Split string into set of words
		ctime = time.perf_counter() #Get current time
		tneeded = ctime - stime #Calculate time needed

		spd = round(len(newinp)/tneeded*60) #Some math that I dont know about

		#print it all out
		counters.clear()
		counters.addstr(0,0,f"Wrong: {mistakes}",blue)
		counters.addstr(2,0,f"Speed: {spd}WPM",blue)
		counters.refresh()

		if txt.getyx()[1] == 49: #Get the x coordinate of text, if it's 49 then print the next slice of string
			query = qslice(easy,sl)
			updateq(query,qslice(easy,sl+1),qslice(easy,sl+2))
			sl += 1 # Increase by 1 for next iteration
			updatetxt(query)
			i = 0 #Go to the first character input after string slice
			#j = 0 #For mistake counter 


	txt.getch()



# Main menu
menuitems = []
def menu(stdsrc):


	#Colors
	curses.init_pair(8,curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(9,curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(10,curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(11,curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(12,curses.COLOR_BLACK, curses.COLOR_BLUE)
	blue = curses.color_pair(8)
	green = curses.color_pair(9)
	red = curses.color_pair(10)
	yellow = curses.color_pair(11)

	stdsrc.clear()

	head = """╔════╗─────────────╔════╦═══╦═══╗╔╗
║╔╗╔╗║─────────────║╔╗╔╗║╔══╣╔═╗╠╝╚╗
╚╝║║╠╣─╔╦══╦╦═╗╔══╗╚╝║║╚╣╚══╣╚══╬╗╔╝
──║║║║─║║╔╗╠╣╔╗╣╔╗║──║║─║╔══╩══╗║║║
──║║║╚═╝║╚╝║║║║║╚╝║──║║─║╚══╣╚═╝║║╚╗
──╚╝╚═╗╔╣╔═╩╩╝╚╩═╗║──╚╝─╚═══╩═══╝╚═╝
────╔═╝║║║─────╔═╝║
────╚══╝╚╝─────╚══╝
By: @FrosT2k5"""


	# Get center co-ordinates of the display screen
	y = curses.LINES // 2 - 4
	x = curses.COLS // 2
	logo = curses.newwin(9,38,2,x-19)
	itemwin = curses.newwin(8,40,y+4,x-18)
	logo.addstr(0,0,head,blue)
	logo.refresh()

	#print info
	#itemwin.addstr(0,0,"Welcome to FrosT's Typing Test Program",green)
	itemwin.keypad(True)

	def printmenu(selitem):
		#print all menu items
		i = 0
		sel = curses.color_pair(12)
		for item in menuitems:
			if i == selitem:
				itemwin.addstr(i,0,item,sel) #Print selected item with sel color combo
			else:
				itemwin.addstr(i,0,item)
			i += 1
			itemwin.refresh()

	printmenu(0)
	curses.noecho()	


	inpnum = 0
	while True:
		inp = itemwin.getkey()
		if inp == "KEY_DOWN" or inp == "S" or inp == "s":
			inpnum += 1
			inpnum = 5 if inpnum > 5 else inpnum #Dont let inpnum go above 6
			printmenu(selitem=inpnum)

		elif inp == "KEY_UP" or inp == "W" or inp == "w":
			inpnum -= 1
			inpnum = 0 if inpnum < 0 else inpnum #Dont let inpnum go above 1
			printmenu(selitem=inpnum)

		elif inp == "Q" or inp == "q":
			curses.echo()
			curses.endwin()
			exit()

		elif checkkey(inp) == 10:
			curses.endwin()
			return inpnum



# function to choose options based on inpnum returned by menu function
def menufunc(inp):
	if inp == 0:
		clr()
		print(Fore.RED,f"\n\nREAD CAREFULLY!{Style.RESET_ALL}\n\nAs soon as you press enter,\ntimer will start in background\nType everything properly with minimal errors\nGood Luck :) !!\n\nPress enter to start!\nDo not resize your terminal between the test...\nPress space key once you typed everything to finish the test")
		input()
		wrapper(main)
	if inp == 1:
		leaderboards()
	if inp == 2:
		config()
		print("Done!")
		input()
	if inp == 3:
		print("Coded by FrosT2k5")
		print("GitHub, Telegram: @FrosT2k5")
		print("Instagram: @yash_patil2k5\n")
		print("@QuantumByteStudios, for making leaderboards server")
		print("Telegram, Github- @QuantumByteStudios")
		input()
	if inp == 4:
		if not os.path.isfile('.config.json'):
			print(Fore.RED,'Configuration not found, please generate it!',Style.RESET_ALL)
			input()
		with open(".config.json") as fil:
			conf = json.load(fil)
			name = conf['name']
			bs = conf['bestscore']
			score = conf['score']
		print('\n\nYour Name:',name)
		print('Your Best Score:',bs)
		print('Your last score:',score)
		chk = input(f"{Fore.YELLOW}Submit your best score to leaderboards?(Y/n): {Style.RESET_ALL}")
		if chk == 'Y' or chk == 'y':
			if bs <= 230:
				print('Submitting...')
				try:
					n = requests.get(f"http://frost.alwaysdata.net/leaderboards.php?{name},{bs}")
				except:
					print(Fore.RED,"Please check your internet connection...",Style.RESET_ALL)
			else:
				print(Fore.RED,"Looks like your score is above 230!, if your didn't cheat, drop me a message...@FrosT2k5",Style.RESET_ALL)
			input()
		else:
			input()
	if inp == 5:
		curses.endwin()
		exit()


# Start the actual program
# Add available menu items
menuitems.append("1 - Take a typing test (easy mode)")
menuitems.append("2 - See leaderboards              ")
menuitems.append("3 - Edit/Create your name config  ")
menuitems.append("4 - Credits Section               ")
menuitems.append("5 - Check/Submit your best score  ")
menuitems.append("6 - Quit (or press q)             ")

# Begin main loop
while True:
	clr()
	userinpt = wrapper(menu)
	menufunc(userinpt)
