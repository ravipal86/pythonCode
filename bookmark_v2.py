import os
import json
import sys
from os.path import expanduser
from termcolor import colored

home = expanduser("~")
new_path = '/.config/google-chrome/Default/Bookmarks'
path = home + new_path
check_text = ''

f = open(path, 'r')
line = f.readlines()

p = open('output_json.txt', 'rw+')
for i in line:
	p.write(i)

my_data = json.loads(open(path).read())
# print my_data

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FOLDER = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_coloured_text(text,replace_text,color):
	replace_text_list = [replace_text, replace_text.lower(), replace_text.upper(), replace_text.title()]
	return text.replace(replace_text, color + replace_text + bcolors.ENDC)


def find_keyword(check_text):
	main_root = my_data['roots']
	for i in main_root:
		if 'type' in main_root[i]:
			print bcolors.FOLDER + 'Folder:', main_root[i]['name'] + bcolors.ENDC
			for j in range(len(main_root[i]['children'])):
				if main_root[i]['children'][j]['type'] == 'folder':
					print bcolors.FOLDER + 'Folder:', main_root[i]['children'][j]['name'] + bcolors.ENDC
					for k in range(len(main_root[i]['children'][j]['children'])):
						title_text = main_root[i]['children'][j]['children'][k]['name']
						url_text = main_root[i]['children'][j]['children'][k]['url']
						if check_text.lower() in title_text.lower() or check_text.lower() in url_text.lower():
							print "Title:\t",get_coloured_text(title_text, check_text, bcolors.OKBLUE)
							print "URL:\t",get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
				else:
					title_text = main_root[i]['children'][j]['name']
					url_text = main_root[i]['children'][j]['url']
					if check_text.lower() in title_text.lower() or check_text.lower() in url_text.lower():
						print "Title:\t",get_coloured_text(title_text, check_text, bcolors.OKBLUE)
						print "URL:\t",get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'


def find_links():
	main_root = my_data['roots']
	for i in main_root:
		if 'type' in main_root[i]:
			print bcolors.FOLDER + 'Folder:', main_root[i]['name'] + bcolors.ENDC
			for j in range(len(main_root[i]['children'])):
				if main_root[i]['children'][j]['type'] == 'folder':
					print bcolors.FOLDER + 'Folder:', main_root[i]['children'][j]['name'] + bcolors.ENDC
					for k in range(len(main_root[i]['children'][j]['children'])):
						print "Title:\t",main_root[i]['children'][j]['children'][k]['name']
						print "URL:\t",main_root[i]['children'][j]['children'][k]['url'],'\n'
				else:
					print "Title:\t",main_root[i]['children'][j]['name']
					print "URL:\t",main_root[i]['children'][j]['url'], '\n'


def find_folder(check_text):
	main_root = my_data['roots']
	for i in main_root:
		if 'type' in main_root[i]:
			print bcolors.FOLDER + 'Default Folder:', main_root[i]['name'] + bcolors.ENDC
			for j in range(len(main_root[i]['children'])):
				if main_root[i]['children'][j]['type'] == 'folder':
					folder_name = main_root[i]['children'][j]['name']
					if check_text.lower() in folder_name.lower():
						print bcolors.FOLDER + 'Folder:', main_root[i]['children'][j]['name'] + bcolors.ENDC
						for k in range(len(main_root[i]['children'][j]['children'])):
							print main_root[i]['children'][j]['children'][k]['name']
							print main_root[i]['children'][j]['children'][k]['url'], '\n'
							# print "Title:\t",get_coloured_text(title_text, check_text, bcolors.OKBLUE)
							# print "URL:\t",get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
					elif check_text == 'All':
						print bcolors.FOLDER + 'Folder:', main_root[i]['children'][j]['name'] + bcolors.ENDC
					else:
						print check_text, "named folder not found"



def count_links():
	main_root = my_data['roots']
	count = 0
	for i in main_root:
		if 'type' in main_root[i]:
			for j in range(len(main_root[i]['children'])):
				if main_root[i]['children'][j]['type'] == 'folder':
					for k in range(len(main_root[i]['children'][j]['children'])):
						count = count + 1
				else:
					count = count + 1
	print "No. of Bookmarks:",count


if sys.argv[1] == '--count' or sys.argv[1] == '-c':
	count_links()
elif sys.argv[1] == '--search' or sys.argv[1] == '-s':
	check_text = sys.argv[2]
	print check_text
	find_keyword(check_text)
elif sys.argv[1] == '--folder' or sys.argv[1] == '-f':
	if len(sys.argv) == 2:
		check_text = 'All'
	else:
		check_text = sys.argv[2]
	find_folder(check_text)

else:
	print "--help"