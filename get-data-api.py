#!/usr/bin/python3
import requests
import pprint
import json

import requests

import requests

url = "https://api.hubapi.com/crm/v3/objects/deals/search?hapikey=325cadcb-2526-4d69-befc-e0faa744726a"

payload = "{\n \"filterGroups\":[\n {\n \"filters\":[\n {\n \"propertyName\":\
		\"dealstage\",\n \"operator\": \"EQ\",\n \"value\": \"2186805\"\n }\n ]\n }\n ],\
		\n \"properties\": [\"dealstage\",\"source\",\"amount\",\"hs_object_id\",\
		\"description\",\"win\",\"ambassador\",\"createdate\",\"dealname\",\"date_offered\"\
		,\"date_won\",\"hubspot_owner_id\",\"dealtype\",\"dev_\",\"duration\",\
		\"notes_last_updated\",\"hs_lastmodifieddate\",\"new_renew\",\"pic\",\
		\"start_date\",\"t_m_fp\",\"technology\",\"source\",\"date_lost\",\
		\"closed_lost_reason\",\"notes_next_activity_date\",\"dealstage\",\
		\"source\",\"amount\",\"hs_object_id\",\"description\",\"win\",\
		\"ambassador\",\"createdate\",\"dealname\",\"date_offered\",\"date_won\",\
		\"hubspot_owner_id\",\"dealtype\",\"dev_\",\"duration\",\"notes_last_updated\",\
		\"hs_lastmodifieddate\",\"new_renew\",\"pic\",\"start_date\",\"t_m_fp\",\
		\"technology\",\"source\",\"date_lost\",\"closed_lost_reason\",\
		\"notes_next_activity_date\"],\n \"limit\": 20\n }"

headers = {
	'Content-Type': 'application/json',
	'Cookie': '__cfduid=d8f2e3e0924f5f0d3e239db357e4651391596621839'
}

response = requests.request("POST", url, headers=headers, data = payload)

def get_total_deal(response):
	"""
	Function 'get_total_deal' return total deal in Hubspot
		by using API

	:param: reponse: the data after fetch from API by POST method 
	"""
	total_deal = (response.json()).get('total')

	return total_deal


def get_properties_data(response):
	"""
	Function 'get_properties_data' return a JSON file of 'Make offer'
	"""
	data = (response.json()).get('results')
	get_data = [ properties['properties'] for properties in data ]

	with open("data.json", "w") as fout:
		json.dump(get_data, fout)

if __name__ == "__main__":
	get_properties_data(response)
	print(get_total_deal(response))
	
