#!/usr/bin/python3

import yaml

def printUsage(strVal):
	print("""
* {} *

[Usage]
====================
assetInfo:
    assetType:
        - OS
    assetSubType:
        - LINUX
    assetCode:
        - U-01 ~ U-10
        - U-11 ~ U-20
        - U-21 ~ U-30
	""".format(strVal))

def readConfig(name):
	document = yaml.load(open("AVAS.yaml", 'r'))
	doc = document['assetInfo']
	print("""

***** Current Configration File Settings *****

TYPE : {}
SUBTYPE : {}
CODE : {}

**********************************************

	""".format(doc['assetType'], doc['assetSubType'], doc['assetCode']))
	return doc
