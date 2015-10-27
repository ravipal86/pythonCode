# -*- coding: utf-8 -*-

from config import Config
import ConfigParser
from os.path import expanduser
import click
from bookmark_v4 import main_group
from bookmark_v4 import CONTEXT_SETTINGS
import sys
import os
import os.path
import json

sources_list = [main_group]

new_path_level = ''

def check_path(new_path):
	if os.path.exists(new_path):
		return True
	else:
		False

def check_file(def_path):
	if os.path.exists(def_path):
		return True
	else:
		False

@click.command(cls=click.CommandCollection, sources=sources_list, context_settings=CONTEXT_SETTINGS, invoke_without_command=True, no_args_is_help=True)
@click.option('-c', '--configure', is_flag=True, help='configure bookmark file')
def bm(configure):

	if configure:
		home = expanduser('~')
		path = home + '/.config/google-chrome/Default/'
		default_path = ''
		file_name = 'Bookmarks'
		data = {
		   'default' : path + file_name,
		   'new_path': '',
		   'set_path': 0,
		}
		with open('.bm_data.json', 'w') as outfile:
			json.dump(data, outfile)

		with open('.bm_data.json', 'r') as f:
			default_path = json.load(f)
			def_path = default_path['default']
		f.close()

		if check_file(def_path):
			print 'inside if', def_path
		else:
			print '{0} do not exists'.format(file_name)
			new_path_raw = raw_input('Please enter new path:')
			print new_path_raw
			if check_path(new_path_raw):
				print 'inside'
				data['new_path'] = new_path_raw
				data['set_path'] = 1
				with open(".bm_data.json", "w") as outfile:
					json.dump(data, outfile)
			else:
				print 'else'
		with open('.bm_data.json', 'r') as f:
			final_path = json.load(f)
			new_path_level = final_path['new_path']

if __name__ == '__main__':
	bm()