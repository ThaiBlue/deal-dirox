module.exports = class HubspotAPI {
	/*
	Combination of serveral function to work with Hubspot APi
	* token {String} - a string that represent Hubspot API access token
	*/
	constructor(token) {
		// store token that fetched from Hubspot
		this.token = token;
		this.axios = require('axios');
	}

	async fetchMakeOfferDeals(properties) {
		/*
		Get all Deals that have "Make Offer" deal stage from Hubspot with a specific set of information of the deal
		* properties {Array} - a list of properties as the name of the information that need to get
		*/
		var data = JSON.stringify({
			"filterGroups": [{
				"filters": [{
					"propertyName": "dealstage",
					"operator": "EQ",
					"value": "2186805" // Make Offer ID
				}]
			}],
			"properties": properties,
			"limit": 20
		});

		var config = {
			method: 'post',
			url: 'https://api.hubapi.com/crm/v3/objects/deals/search',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + this.token
			},
			data: data
		};

		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data.results;
		} catch (err) {
			//send request again if fail
			this.fetchMakeOfferDeals(properties);
		}
	}

	async getOwnerInfo(ownerID) {
		/*
		Get information of a owner from their ID
		* ownerID {String} - a string of number
		*/

		var config = {
			method: 'get',
			url: 'https://api.hubapi.com/crm/v3/owners/' + ownerID,
			headers: {
				'Authorization': 'Bearer ' + this.token
			}
		};

		try {
			//fetching data
			var res = await this.axios(config);
			return res.data;
		} catch (err) {
			//send request again if fail
			this.getOwnerInfo(ownerID);
		}
	}
	
	async getAssociateCompanyIDOfDeal(dealID) {
		var config = {
		  method: 'get',
		  url: 'https://api.hubapi.com/crm/v3/objects/deals/' + dealID + '/associations/companies',
		  headers: { 
			'Authorization': 'Bearer ' + this.token
		  }
		};

		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data.results[0].id;
		} catch (err) {
			//send request again if fail
			this.getAssociateCompanyIDOfDeal(dealID);
		}
	}
	
	async getCompanyInfo(dealID) {
		var companyID = await this.getAssociateCompanyIDOfDeal(dealID);
		var config = {
		  method: 'get',
		  url: 'https://api.hubapi.com/crm/v3/objects/companies/' + companyID,
		  headers: { 
			'Authorization': 'Bearer ' + this.token
		  }
		};

		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data;
		} catch (err) {
			//send request again if fail
			this.getCompanyInfo(dealID);
		}
	}
}