class HubspotAPI {
	constructor (token) {
		// store token that fetched from Hubspot
		this.token = token;
	}
	
	async fetchMakeOfferDeals (properties) {
		var axios = require('axios');
		var data = JSON.stringify(
			{
				"filterGroups":[
					{
						"filters": [
							{
								"propertyName":"dealstage",
								"operator":"EQ",
								"value":"2186805" // Make Offer ID
							}]
					}],
						"properties":properties,
				"limit":20
			});
		
		var config = {
			method: 'post',
			url: 'https://api.hubapi.com/crm/v3/objects/deals/search',
			headers: { 
			  'Content-Type': 'application/json',
			  'Authorization': 'Bearer ' + this.token
			},
			data : data
		  };
		 // send request
		var response = await axios(config);
		//return fetched data
		return response.data
	}
}

async function main () {
	var token = 'CKy68Ze-LhICAQEY1rSfAyC74cEFKOfFDTIZAJ-qy2tKFEchHkOx5RPVsTwqLjtqAHsbfDoaAAoCQQAADIACAAgAAAABAAAAAAAAABjAAANCGQCfqstr19Lm_hem9KWOwcEe2WZGVRzu1vM';
	var prop = [
		"dealstage",
		"source",
		"amount",
		"hs_object_id",
		"description",
		"win",
		"ambassador",
		"createdate",
		"dealname",
		"date_offered",
		"date_won",
		"hubspot_owner_id",
		"dealtype",
		"dev_",
		"duration",
		"notes_last_updated",
		"hs_lastmodifieddate",
		"new_renew",
		"pic",
		"start_date",
		"t_m_fp",
		"technology",
		"source",
		"date_lost",
		"closed_lost_reason",
		"notes_next_activity_date",
		"deal_currency_code",
		"amount_in_home_currency"
	];
	var hubspotapi = new HubspotAPI(token);
	var data = await hubspotapi.fetchMakeOfferDeals(prop)
	console.log(data)
}

main()