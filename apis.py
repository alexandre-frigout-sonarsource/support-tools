#!/usr/bin/env python3
import os, sys, json
import requests
import argparse


def main():
	
	# The web api lists need to be retrieved from the following web api call and put into two separate files with json format: api/webservices/list?include_internals=true
	# Example of usage to get the list of dropped apis between SQ 8.9 and SQ 9.9:
	# 		python3 apis.py --old 8.9-webapi-list.json --new 9.9-webapi-list.json --dropped
	# Example of usage to get the list of deprecated apis since SQ 8.9:
	# 		python3 apis.py --current 9.9-webapi-list.json --since 8.9

	parser = argparse.ArgumentParser()
	parser.add_argument("--old", dest='old', help='Name of the json file containing the web api list of the old sonarqube instance')
	parser.add_argument("--new", dest='new', help='Name of the json file containing the web api list of the old sonarqube instance')
	parser.add_argument("--dropped", dest='dropped', action='store_true', help='add this if you want to see dropped apis')
	parser.add_argument("--added", dest='added', action='store_true', help='add this if you want to see added apis')
	parser.add_argument("--current", dest='current', help='Name of the json file containing the web api list of the sonarqube instance, use this to see deprecated apis')
	parser.add_argument("--since", dest='since')
	results = parser.parse_args()

	if results.old and results.new:
		try:
			file1 = results.old
			f1 = open(file1)
		except IOError:
			print("###### \n The file for the old instance could not be open.")
			exit(3)
		try:
			file2 = results.new
			f2 = open(file2)
		except IOError:
			print("###### \n The file for the new instance could not be open.")
			exit(3)

		APIS1 = []
		APIS2 = []

		data1 = json.load(f1)
		data2 = json.load(f2)

		webs1 = data1['webServices']
		webs2 = data2['webServices']

		for apis in webs1:
			api = apis['path']
			for a in apis['actions']:
				api = api + '/' + a['key']
				APIS1.append(api)
				api = apis['path']
			api = ''

		for apis in webs2:
			api = apis['path']
			for a in apis['actions']:
				api = api + '/' + a['key']
				APIS2.append(api)
				api = apis['path']
			api = ''

		
		print("\n\n\n")
		if results.dropped:
			print("web apis dropped between " + file1 + " and " + file2)
			for ap in set(APIS1) - set(APIS2):
				print('\t'+ap)
		if results.added:
			print("web apis added between " + file1 + " and " + file2)
			for ap in set(APIS2) - set(APIS1):
				print('\t'+ap)
		print("\n\n\n")

	if results.current and results.since:
		try:
			file1 = results.current
			f1 = open(file1)
		except IOError:
			print("###### \n The file for the SQ instance could not be open.")
			exit(3)

		APIS = []
		data1 = json.load(f1)
		webs1 = data1['webServices']
		print("web apis deprecated since " + results.since + ":")
		for apis in webs1:
			api = apis['path']
			for a in apis['actions']:
				b = a.get('deprecatedSince')
				if b is not None and b >= results.since:
					api = api + '/' + a['key']
					APIS.append(api)
				api = apis['path']
			api = ''
		for ap in APIS:
				print('\t'+ap)


if __name__ == '__main__':
	main()
