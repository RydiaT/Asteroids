from colorama import Fore, Style
import os.path
from random import uniform

def cprint(message, message_type="info"):
	prefix = ""
	if message_type == "info":
		prefix = Fore.CYAN
	elif message_type == "warning":
		prefix = Fore.YELLOW
	elif message_type == "error":
		prefix = Fore.RED
	elif message_type == "success":
		prefix = Fore.GREEN

	print(prefix + message + Style.RESET_ALL)


def get_highscore():
	if not os.path.exists("highscore.txt"):
		cprint("No highscore file found.", "warning")

		f = open("highscore.txt", "x")
		f = open("highscore.txt", "w")
		f.write("0")
		f.close()

		cprint("Highscore save created.", "info")
		print("\n=====================================\n")

	with open("highscore.txt", "r") as score_raw:
		score = score_raw.read().strip()

		try:
			return int(score)
		except ValueError:
			cprint("Highscore unable to be read.", "error")
			print(score)
			print(type(score))
			return -1

def set_highscore(score):
	with open("highscore.txt", "w") as score_raw:
		score_raw.write(f"{score}")

def on_exit(score, highscore):
	if score > highscore:
		cprint("NEW HIGHSCORE!!!!", "success")
		cprint(f"{highscore} ───▶ {score}", "warning")

		print("\n=====================================\n")

		set_highscore(score)

def generate_bright_color():
	red = uniform(150, 255)
	blue = uniform(150, 255)
	green = uniform(150, 255)

	return red, blue, green