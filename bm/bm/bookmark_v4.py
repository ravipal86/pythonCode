# -*- coding: utf-8 -*-

import json
import sys
import os
from os.path import expanduser
import lxml.html
from lxml.html import parse
import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup
import click
from termcolor import colored
import datetime
import time
import calendar
from datetime import datetime

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
home = expanduser("~")
new_path = '/.config/google-chrome/Default/Bookmarks'
path = home + new_path
folder_text = ''
abc = []
kbc = []
xyz = []
test = []
count = 0
add_dir = {}
keys_list = []
values_list = []
id = 0
url = ''
folder = ''
sync_transv = 0

# f = open(path, 'r')
# line = f.readlines()

# p = open('output_json.txt', 'rw+')
# for i in line:
# 	p.write(i)

my_data = json.loads(open(path).read())
main_root = my_data['roots']
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
	return text.replace(replace_text, color + replace_text + bcolors.ENDC)

def folder_list(root):
    if isinstance(root, dict):
        for i in root.keys():
            if i == 'type':
                if root['type'] == 'folder':
                    if root['name'] not in values_list:
                        values_list.append(root['name'])
        map(lambda x: folder_list(x), root.values())
    elif isinstance(root, list):
        map(lambda x: folder_list(x), root)

@click.group()
def main_group():
  pass

@main_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--folder_text','-f', required=False, help='Search for folder.')
@click.option('--get_list','-l', is_flag=True, help='get list of all folders.')
@click.option('--search','-s', required=False, help='Search keyword inside folder. Use "" for more than one words.')
def check_folder(folder_text, get_list, search):
    if folder_text != None:
        if search != None:
            get_folder(main_root, abc, xyz, folder_text, get_list, search)
        else:
            get_folder(main_root, abc, xyz, folder_text, get_list, search)
    else:
        if search != None:
            print "search needs folder name to be searched in."
            folder_list(my_data)
        else:
            print "Please enter folder to be searched."

def get_folder(root, keys_list, values_list, folder_text, get_list, search):
    if isinstance(root, dict):
        if get_list == False:
            if 'children' in root.keys():
                if root['name'] == folder_text:
                    print bcolors.FOLDER + "Folder:",root['name'] + bcolors.ENDC, '\n'
                    print folder_details(root['children'],test, search)
            keys_list += root.keys()
            values_list += root.values()
        if get_list:
            if 'children' in root.keys():
                print bcolors.FOLDER + "Folder:",root['name'] + bcolors.ENDC
        map(lambda x: get_folder(x, keys_list, values_list, folder_text, get_list, search), root.values())
    elif isinstance(root, list):
        map(lambda x: get_folder(x, keys_list, values_list, folder_text, get_list, search), root)


def folder_details(root, keys_list, search):
    if isinstance(root, dict):
        if 'name' in root.keys() and 'url' in root.keys():
            name = root['name']
            url = root['url']
            if search != None:
                if search in name or search in url:
                    print get_coloured_text(name, search, bcolors.OKBLUE)
                    print get_coloured_text(url, search, bcolors.OKBLUE),'\n'
            else:
                print name
                print url,'\n'
        keys_list += root.keys()
    elif isinstance(root, list):
        map(lambda x: folder_details(x, keys_list, search), root)

# Count the no. of links in the folder, total links
@main_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--folder', required=False, help='Name of folder.')
def total_links(folder):
    if folder:
        print bcolors.FOLDER + "Searched Folder:"+ folder + bcolors.ENDC, '\n'
        print count_in_folder(main_root, folder)
        print "Total no. of links:",count
    else:
        print count_links(main_root)
        print "Total no. of links:",count

def count_links(root):
    global count
    if isinstance(root, dict):
        if 'url' in root.keys():
            count += 1
        map(lambda x: count_links(x), root.values())
    elif isinstance(root, list):
        map(lambda x: count_links(x), root)

def count_in_folder(root, folder):
    global count
    if isinstance(root, dict):
        if 'children' in root.keys():
            if root['name'] == folder:
                for link in root['children']:
                    if 'url' in link:
                        count = count + 1
        map(lambda x: count_in_folder(x, folder), root.values())
    elif isinstance(root, list):
        map(lambda x: count_in_folder(x, folder), root)

# Search All links, search specific keyword in all links.
@main_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--search', required=False, help='Search by keywpord. Type "All" for all links. User "" for more than one word')
def search_link(search):
    if search == 'All':
        print bcolors.FOLDER + "Search:"+ search + bcolors.ENDC, '\n'
        search_in(main_root, search)
    else:
        print bcolors.FOLDER + "Search:"+ search + bcolors.ENDC, '\n'
        search_in(main_root, search)

def search_in(root, search):
    if search != 'All':
        if isinstance(root, dict):
            if 'url' in root.keys():
                if search in root['name'] or search in root['url'] or search.lower() in root['name'] or search.lower() in root['url']:
                    name, url = root['name'], root['url']
                    print get_coloured_text(name, search, bcolors.OKBLUE)
                    print get_coloured_text(url, search, bcolors.OKBLUE),'\n'
            map(lambda x: search_in(x, search), root.values())
        elif isinstance(root, list):
            map(lambda x: search_in(x, search), root)
    elif search == 'All':
        if isinstance(root, dict):
            if 'url' in root.keys():
                name, url = root['name'], root['url']
                print get_coloured_text(name, search, bcolors.OKBLUE)
                print get_coloured_text(url, search, bcolors.OKBLUE),'\n'
            map(lambda x: search_in(x, search), root.values())
        elif isinstance(root, list):
            map(lambda x: search_in(x, search), root)

@main_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--url','-u', required=True, help='Search for folder.')
@click.option('--folder','-f', required=False, help='Search for folder.')
@click.option('--add_folder','-a', required=False, help='Add Folder and Link in that folder')
@click.option('--inside','-i', required=False, help='Add Folder and Link inside exisiting folder')
def add_link(url, folder, add_folder, inside):
    add_dir = {}
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    title = soup.title.string
    text_folder = folder
    fixup(my_data, text_folder)
    add_dir['date_added'] = str(int(time.time() * 1000))
    add_dir['id'] = str(id + 1)
    add_dir['name'] = title
    add_dir['type'] = 'url'
    add_dir['url'] = url
    folder_list(my_data)
    if inside != None:
        if add_folder == None:
            print "inside folder works with add_folder"
        else:
            if inside not in values_list:
                text = inside+"-Folder does not exists. Please chech the folders."
                print get_coloured_text(text, inside,bcolors.FOLDER)
                print get_coloured_text("Folder List:", "Folder List:", bcolors.FOLDER)
                for i in values_list:
                    print get_coloured_text(i, i,bcolors.FOLDER)
            else:
                if add_folder in values_list:
                    print add_folder, " folder already exists."
                    check_add_folder = raw_input("Do you want to rename folder(y) or check folder list(y/n)?:")
                    if check_add_folder == 'y':
                        add_folder = raw_input('New folder name:')
                        append_dir(my_data, text_folder, add_dir, add_folder, inside)
                    else:
                        for i in values_list:
                            print get_coloured_text(i, i,bcolors.FOLDER)
                else:
                    append_dir(my_data, text_folder, add_dir, add_folder, inside)
    else:
        append_dir(my_data, text_folder, add_dir, add_folder, inside)

def fixup(root, folder):
    if isinstance(root, dict):
        for key in root.keys():
            if key == 'id':
                global id
                if id < int(root[key]):
                    id = int(root[key])
            if key == 'sync_transaction_version':
                global sync_transv
                if sync_transv < int(root[key]):
                    sync_transv = int(root[key])
        map(lambda x: fixup(x, folder), root.values())
    elif isinstance(root, list):
        map(lambda x: fixup(x, folder), root)

def append_dir(root, folder, add_dir, add_folder, inside):
    if isinstance(root, dict):
        for key in root.keys():
            if key == 'type':
                if root[key] == 'folder':
                    if folder == None:  # When user do not enter folder name so url should pe added in default i.e. 'bookmarks bar'
                        if add_folder == None:  #When user 
                            if root['name'] == 'Bookmarks bar':
                                print add_folder, inside
                                root['children'].append(add_dir)
                                root['date_modified'] = str(int(time.time() * 1000))
                                json_write()
                        elif inside == None:
                            if root['name'] == 'Bookmarks bar':
                                folder_dir = {}
                                child_list = []
                                folder_dir['date_added'] = str(int(time.time() * 1000))
                                folder_dir['date_modified'] = str(int(time.time() * 1000))
                                folder_dir['id'] = str(id + 1)
                                folder_dir['name'] = add_folder
                                folder_dir['sync_transaction_version'] = str(sync_transv + 1)
                                folder_dir['type'] = 'folder'
                                child_list.append(add_dir)
                                folder_dir['children'] = child_list
                                root['children'].append(folder_dir)
                                json_write()
                        else:
                            if root['name'] == inside:
                                folder_dir = {}
                                child_list = []
                                folder_dir['date_added'] = str(int(time.time() * 1000))
                                folder_dir['date_modified'] = str(int(time.time() * 1000))
                                folder_dir['id'] = str(id + 1)
                                folder_dir['name'] = add_folder
                                folder_dir['sync_transaction_version'] = str(sync_transv + 1)
                                folder_dir['type'] = 'folder'
                                child_list.append(add_dir)
                                folder_dir['children'] = child_list
                                root['children'].append(folder_dir)
                                json_write()
                    elif root['name'] == folder:
                        root['children'].append(add_dir)
                        root['date_modified'] = str(int(time.time() * 1000))
                        json_write()
        map(lambda x: append_dir(x, folder, add_dir, add_folder, inside), root.values())
    elif isinstance(root, list):
        map(lambda x: append_dir(x, folder, add_dir, add_folder, inside), root)

def json_write():
    with open((path), 'w') as outfile:
        json.dump(my_data, outfile)
    print "Adding Done"

