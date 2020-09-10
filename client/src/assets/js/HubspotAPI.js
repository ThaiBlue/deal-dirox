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
		Get all Deals that have 'Make Offer' deal stage from Hubspot with a specific set of information of the deal
		* properties {Array} - a list of properties as the name of the information that need to get
		*/
		var data = JSON.stringify({
			filterGroups: [{
				filters: [{
					propertyName: 'dealstage',
					operator: 'EQ',
					value: '2186805' // Make Offer ID
				}]
			}],
			properties: properties,
			limit: 20
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
			return Promise.resolve(response);

		} catch (err) {
			if (err.status == 408) {
				//send request again if request time out
				this.fetchMakeOfferDeals(properties);
			}
			//return error code
			return Promise.reject(err);
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
			//return response data
			return Promise.resolve(res.data);

		} catch (err) {
			if (err.status == 408) {
				//send request again if request time out
				this.getOwnerInfo(ownerID);
			}
			//return error code
			return Promise.reject(err);
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

		// connection handler
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return Promise.resolve(response.data.results[0].id);

		} catch (err) {
			if (err.status == 408) {
				//send request again if request time out
				this.getAssociateCompanyIDOfDeal(dealID);
			}
			//return error code
			return Promise.reject(err);
		}
	}

	async getCompanyInfo(dealID) {
		/*
		Fetch infomation of the Company(Customer) that associates with the Deal has the given dealID
		* dealID {Number} identity of the Deal needs to get its' relative Company info(Customer name)
		*/
		var companyID = await this.getAssociateCompanyIDOfDeal(dealID);
		console.log(companyID)
		
		var config = {
			method: 'get',
			url: 'https://api.hubapi.com/crm/v3/objects/companies/' + companyID,
			headers: {
				'Authorization': 'Bearer ' + this.token
			}
		};

		// connection handler		
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return Promise.resolve(response.data);

		} catch (err) {
			if (err.status == 408) {
				//send request again if request time out
				this.getCompanyInfo(dealID);
			}
			//return error code
			return Promise.reject(err);
		}
	}
}