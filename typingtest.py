import os
import time
from colorama import Fore,Style
import json

def config():
	if os.path.isfile(".config.json"):
		print(Fore.RED,"Previously saved config found!, overwriting",Style.RESET_ALL)
	else:
		None
	name = input("Enter your name: ")
	conf ={
		"name": name,
		"bestscore": 0
	}

	confile = open(".config.json","w")
	json.dump(conf,confile,indent="    ")
	confile.close()

def clr():
    time.sleep(0.2)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clr()

head = """
		╔════╗─────────────╔════╦═══╦═══╗╔╗
		║╔╗╔╗║─────────────║╔╗╔╗║╔══╣╔═╗╠╝╚╗
		╚╝║║╠╣─╔╦══╦╦═╗╔══╗╚╝║║╚╣╚══╣╚══╬╗╔╝
		──║║║║─║║╔╗╠╣╔╗╣╔╗║──║║─║╔══╩══╗║║║
		──║║║╚═╝║╚╝║║║║║╚╝║──║║─║╚══╣╚═╝║║╚╗
		──╚╝╚═╗╔╣╔═╩╩╝╚╩═╗║──╚╝─╚═══╩═══╝╚═╝
		────╔═╝║║║─────╔═╝║
		────╚══╝╚╝─────╚══╝
	"""

def test():
	pararaw = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life."
	para = """
			Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, 
			there live the blind texts. Separated they live in Bookmarksgrove right at the coast 
			of the Semantics, a large language ocean. A small river named Duden flows by their 
			place and supplies it with the necessary regelialia. It is a paradisematic country, 
			in which roasted parts of sentences fly into your mouth. Even the all-powerful 
			Pointing has no control about the blind texts it is an almost unorthographic life. 
			"""

	print(head)
	print("Welcome to Typing Test Program")
	print("By",Fore.GREEN,"@FrosT2k5, @QuantumByteStudios and @Vissu01",Style.RESET_ALL)

	print(Fore.RED,"\n\nNOTE:")
	print(Style.RESET_ALL)
	print("You will be given a paragraph of 100 words\nYou have to type it as fast as possible\nEach Mistake adds +5 seconds to your typing speed\nNOTE that paragraph doesn't have newlines!")
	input("\nPress Enter to continue:")
	print("\n")

	for i in (3,2,1):
		print(f"{Fore.GREEN}The test will begin in {i} seconds, get ready!{Style.RESET_ALL}",end="\r")
		time.sleep(1)
	clr()

	print(para)

	StartTime = time.perf_counter()
	inp = input("Enter the above paragraph below! Note that paragraph doesn't have newline!. Press enter only if you are done!:\n\n")
	print("\n\n")
	EndTime = time.perf_counter()

	orig = pararaw.split(" ")
	typ = inp.split(" ")
	mistakes = 0
	i = 0

	while i < len(orig):
		try:
			if orig[i] != typ[i]:
				print(Fore.RED,"Mistake: expected:",orig[i],", You typed: ",typ[i],Style.RESET_ALL)
				mistakes += 1
			else:
				None
		except IndexError:
			mistakes += 1
		i+=1

	print(Fore.GREEN,"Total number of mistakes: ",mistakes,Style.RESET_ALL)
	print("\n")


	time_taken = EndTime - StartTime
	penalty = mistakes*5
	time_taken = time_taken + penalty
	wpm = round(len(orig)*60/time_taken)

	print(f"{Fore.YELLOW}You took total {time_taken} seconds to type the paragraph")
	print(f"{Fore.YELLOW}So your typing speed is around: {wpm} words per minute!{Style.RESET_ALL}")
	print(f"{Fore.GREEN}\nSaving your score...{Style.RESET_ALL}")
	if not os.path.isfile(".config.json"):
		print(f"{Fore.RED}No local config found, generating...{Style.RESET_ALL}")
		config()
	
	confile = open(".config.json",'r')
	conf = json.load(confile)
	confile.close()

	name = conf["name"]
	conf["score"] = wpm
	bestscore = conf["bestscore"]
	print(bestscore,wpm)
	if wpm > bestscore:
		print("Highscore!")
		conf["bestscore"] = wpm

	print(conf)
	confile = open(".config.json","w")
	json.dump(conf,confile,indent=6)
	confile.close()

	ck = input(f"{Fore.BLUE}Do you want to submit your score in leaderboards?{Style.RESET_ALL}(Y/n)")
	if ck == "y" or ck == "Y":
		print("Coming Soon!")
	exit()

if __name__=="__main__":
	while True:
		clr()
		print(head)
		print("Welcome to Typing test program")
		print(Fore.GREEN,"\nPlease enter one of the following options - ")
		print("""
1 - Take a typing test (Medium mode, easy and difficult coming soon!)
2 - See leaderboards
3 - Edit/Create your name configuration 
4 - Credits Section
5 - Quit
			""")

		inp = input(f"{Fore.YELLOW}[COMMAND] : {Style.RESET_ALL}")
		if inp == "1":
			clr()
			test()
		if inp == "2":
			print("Coming SOON!")
		if inp == "3":
			config()
		if inp == "4":
			print("Coded by FrosT2k5")
			print("GitHub, Telegram: @FrosT2k5")
			print("Instagram: @yash_patil2k5\n\n")
			print("Leaderboards database and code by @Vissu01")
			print("Telegram: @Vissu01")
			print("@QuantumByteStudios, making difficulty levels and alternative way of leaderboards")
			print("Telegram, Githu b- @QuantumByteStudios")
			input()
		if inp == "5":
			exit()