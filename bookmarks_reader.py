import os
import json
import sys
from os.path import expanduser
from termcolor import colored

home = expanduser("~")
new_path = '/.config/google-chrome/Default/Bookmarks'
path = home + new_path
argv_list = ['--search', '--folder', '--count']
check_text = ''
argument_count = 0
capital_text = ''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FOLDER = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# f = open(path, 'r')

# line = f.readlines()

# p = open('output_json.txt', 'rw+')
# for i in line:
# 	p.write(i)

def get_coloured_text(text,replace_text,color):
	return text.replace(replace_text,color + replace_text + bcolors.ENDC)

my_data = json.loads(open(path).read())
# print my_data
bookmarks = my_data['roots']['bookmark_bar']['children']
len_path = len(bookmarks)

def argv_list_SEARCH(check_text):
	count = 0
	if check_text != 'All':
		print bcolors.BOLD + "Searched word:"+check_text+'\n'+ bcolors.ENDC
		for i in range(len_path):
			if 'children' in bookmarks[i]:
				for j in range(len(bookmarks[i]['children'])):
					title = bookmarks[i]['children'][j]['name']
					url = bookmarks[i]['children'][j]['url']
					if check_text.lower() in title.lower() or check_text.lower() in url.lower():
						count = count + 1
						print bcolors.FOLDER + "Folder:"+bookmarks[i]['name'] + bcolors.ENDC
						title_text = "Title:\t"+bookmarks[i]['children'][j]['name']
						url_text = "URL:\t"+bookmarks[i]['children'][j]['url']
						print get_coloured_text(title_text, check_text, bcolors.OKBLUE)
						print get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
			else:
				title = bookmarks[i]['name']
				url = bookmarks[i]['url']
				if check_text.lower() in title.lower() or check_text.lower() in url.lower():
					count = count + 1
					print bcolors.FOLDER + "Folder:"+'bookmark_bar' + bcolors.ENDC
					title_text = "Title:\t"+bookmarks[i]['name']
					url_text = "URL:\t"+bookmarks[i]['url']
					print get_coloured_text(title_text, check_text, bcolors.OKBLUE)
					print get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
	else:
		print bcolors.BOLD + "All Bookmarks"+ bcolors.ENDC
		for i in range(len_path):
			if 'children' in bookmarks[i]:
				for j in range(len(bookmarks[i]['children'])):
					count = count + 1
					title = bookmarks[i]['children'][j]['name']
					print bcolors.FOLDER + "Folder:"+bookmarks[i]['name'] + bcolors.ENDC
					title_text = "Title:\t"+bookmarks[i]['children'][j]['name']
					url_text = "URL:\t"+bookmarks[i]['children'][j]['url']
					print get_coloured_text(title_text, check_text, bcolors.OKBLUE)
					print get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
			else:
				count = count + 1
				title = bookmarks[i]['name']
				print bcolors.FOLDER + "Folder:"+'bookmark_bar' + bcolors.ENDC
				title_text = "Title:\t"+bookmarks[i]['name']
				url_text = "URL:\t"+bookmarks[i]['url']
				print get_coloured_text(title_text, check_text, bcolors.OKBLUE)
				print get_coloured_text(url_text, check_text, bcolors.OKBLUE),'\n'
	print count

def argv_list_COUNT():
	link_list = {}
	count = 0
	for i in range(len_path):
		if 'children' in bookmarks[i]:
			for j in range(len(bookmarks[i]['children'])):
				count = count + 1
				title = bookmarks[i]['children'][j]['name']
				title_text = "Title:\t"+bookmarks[i]['children'][j]['name']
				url_text = "URL:\t"+bookmarks[i]['children'][j]['url']
		else:
			count = count + 1
			title = bookmarks[i]['name']
			title_text = "Title:\t"+bookmarks[i]['name']
			url_text = "URL:\t"+bookmarks[i]['url']
	print "Total Bookmarks count:",count

for agv in sys.argv:
	capital_text = capital_text + ' '+ agv

if sys.argv[1] == '--count' or sys.argv[1] == '--c':
	argv_list_COUNT()
elif sys.argv[1] == '--search' or sys.argv[1] == '--s':
	check_text = sys.argv[2]
	print check_text
	argv_list_SEARCH(check_text)
else:
	print "Error"