#!/usr/bin/python3
import requests
import pprint
import json

import requests

url = "https://api.hubapi.com/crm/v3/objects/deals/search"

querystring = {"hapikey":"325cadcb-2526-4d69-befc-e0faa744726a"}

payload = "{\n\"filterGroups\":[\n{\n\"filters\":[\n{\n\"propertyName\":\
					\"dealstage\",\n \"operator\": \"EQ\",\n\"value\": \"2186805\"\
					\n}\n]\n}\n],\n\"properties\": [\"ambassador\", \"amount_in_home_currency\",\
					\"browsers\", \"cms\", \"database\", \"date_lost\", \"date_offered\",\
					\"date_won\", \"days_to_close\", \"deal_currency_code\", \"deal_summary\", \
					\"dev_\", \"duration\", \"hs_acv\", \"hs_analytics_source\", \
					\"hs_analytics_source_data_1\", \"hs_analytics_source_data_2\", \
					\"hs_arr\", \"hs_campaign\", \"hs_closed_amount\", \
					\"hs_closed_amount_in_home_currency\", \"hs_created_by_user_id\", \
					\"hs_date_entered_1442962\", \"hs_date_entered_1442963\", \"hs_date_entered_1442964\", \
					\"hs_date_entered_1442968\", \"hs_date_entered_2111226\", \"hs_date_entered_2111227\", \
					\"hs_date_entered_2142342\", \"hs_date_entered_2148969\", \"hs_date_entered_2186805\", \
					\"hs_date_entered_2186806\", \"hs_date_entered_2186816\", \"hs_date_entered_2186859\", \
					\"hs_date_entered_appointmentscheduled\", \"hs_date_entered_closedlost\", \
					\"hs_date_entered_closedwon\", \"hs_date_entered_contractsent\", \
					\"hs_date_entered_decisionmakerboughtin\", \"hs_date_entered_presentationscheduled\", \
					\"hs_date_entered_qualifiedtobuy\", \"hs_date_exited_1442962\", \
					\"hs_date_exited_1442963\", \"hs_date_exited_1442964\", \"hs_date_exited_1442968\", \
					\"hs_date_exited_2111226\", \"hs_date_exited_2111227\", \"hs_date_exited_2142342\", \
					\"hs_date_exited_2148969\", \"hs_date_exited_2186805\", \"hs_date_exited_2186806\", \
					\"hs_date_exited_2186816\", \"hs_date_exited_2186859\", \
					\"hs_date_exited_appointmentscheduled\", \"hs_date_exited_closedlost\", \
					\"hs_date_exited_closedwon\", \"hs_date_exited_contractsent\", \
					\"hs_date_exited_decisionmakerboughtin\", \"hs_date_exited_presentationscheduled\", \
					\"hs_date_exited_qualifiedtobuy\", \"hs_deal_amount_calculation_preference\", \
					\"hs_deal_stage_probability\", \"hs_is_closed\", \"hs_lastmodifieddate\", \
					\"hs_likelihood_to_close\", \"hs_manual_forecast_category\", \
					\"hs_merged_object_ids\", \"hs_mrr\", \"hs_object_id\", \
					\"hs_predicted_amount\", \"hs_predicted_amount_in_home_currency\", \
					\"hs_projected_amount\", \"hs_projected_amount_in_home_currency\", \
					\"hs_tcv\", \"hs_time_in_1442962\", \"hs_time_in_1442963\", \
					\"hs_time_in_1442964\", \"hs_time_in_1442968\", \"hs_time_in_2111226\", \
					\"hs_time_in_2111227\", \"hs_time_in_2142342\", \"hs_time_in_2148969\", \
					\"hs_time_in_2186805\", \"hs_time_in_2186806\", \"hs_time_in_2186816\", \
					\"hs_time_in_2186859\", \"hs_time_in_appointmentscheduled\", \
					\"hs_time_in_closedlost\", \"hs_time_in_closedwon\", \
					\"hs_time_in_contractsent\", \"hs_time_in_decisionmakerboughtin\", \
					\"hs_time_in_presentationscheduled\", \"hs_time_in_qualifiedtobuy\", \
					\"hs_updated_by_user_id\", \"hs_user_ids_of_all_owners\", \
					\"hubspot_owner_assigneddate\", \"infrastructure\", \"lead_overview_1\", \
					\"lead_overview_2\", \"new_renew\", \"os\", \"payment_module\", \"pic\", \
					\"source\", \"start_date\", \"t_m_fp\", \"technologies\", \"technology\", \
					\"win\", \"dealname\", \"amount\", \"dealstage\", \"pipeline\", \"closedate\", \
					\"createdate\", \"engagements_last_meeting_booked\", \
					\"engagements_last_meeting_booked_campaign\", \"engagements_last_meeting_booked_medium\",\
					\"engagements_last_meeting_booked_source\", \"hs_latest_meeting_activity\", \
					\"hs_sales_email_last_replied\", \"hubspot_owner_id\", \"notes_last_contacted\", \
					\"notes_last_updated\", \"notes_next_activity_date\", \"num_contacted_notes\", \
					\"num_notes\", \"hs_createdate\", \"hubspot_team_id\", \"dealtype\", \
					\"hs_all_owner_ids\", \"description\", \"hs_all_team_ids\", \
					\"hs_all_accessible_team_ids\", \"num_associated_contacts\", \
					\"closed_lost_reason\", \"closed_won_reason\"],\n\"limit\": 20\n}"
headers = {
		'Content-Type': "application/json",
		'cache-control': "no-cache",
		'Postman-Token': "dd3e75de-5778-49ba-9e27-4c23b1779ed1"
		}


response = requests.request("POST", url, data=payload, headers=headers, params=querystring)


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

get_properties_data(response)
