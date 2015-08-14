# -*- coding: utf-8 -*-

from config import Config
import click
from bookmark_v4 import main_group
from bookmark_v4 import CONTEXT_SETTINGS
from bookmark_v4 import new_path
import sys
import os

sources_list = [main_group]

@click.command(cls=click.CommandCollection, sources=sources_list, context_settings=CONTEXT_SETTINGS, invoke_without_command=True, no_args_is_help=True)
@click.option('-c', '--configure', is_flag=True, help='configure bookmark file')
def bm(configure):
	path = '/.config/google-chrome/Default/Bookmarks'
	if configure:
		path = raw_input('Enter bookmarks path:')
		f = file('/.bm.cfg')
		cfg = Config(f)
		print cfg.message
	new_path = path
	print new_path



if __name__ == '__main__':
	bm()