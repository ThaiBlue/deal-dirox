module.exports = class SlideAPI {
	/*
	Interact with Googlw side APi to modify a given presentation
	* token {String} - a string that represent Google API access token
	* slideID {String} - a string that represent the ID of a google slide presentation
	*/
	constructor (token, slideID) {
		this.token = token;
		this.slideID = slideID;
		this.axios = require('axios');
	}
	
	async getSlideRevisionID() {
		var config = {
		  method: 'get',
		  url: 'https://slides.googleapis.com/v1/presentations/' + this.slideID,
		  headers: { 
			'Authorization': 'Bearer ' + this.token
		  }
		};
		
		// start fetching data
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data.revisionId;
		} catch (err) {
			//send request again if fail
			this.getSlideRevisionID();
		}		
	}
	
	async updatePresentaion (description, deal_summary, lead_overview_1, lead_overview_2, customer_name) {
		/*
		update a presentation with deal infomation
		* description {String} - information of a deal
		* deal_summary {String} - information of a deal
		* lead_overview_1 {String} - information of a deal
		* lead_overview_2 {String} - information of a deal
		* customer_name {String} - information of a deal 
		*/
		var moment = require('moment');
		var requiredRevisionId = await this.getSlideRevisionID();
		var data = JSON.stringify(
			{
			  "requests": [
				  // can add more object to commit serveral text replacement in the whole slide
				  // ,
				  // {
				  // 	"replaceAllText": {
				  // 		"replaceText": '<Some information>',
				  // 		"pageObjectIds": [],
				  // 		"containsText": {
				  // 			"text": "Some Text>",
				  // 			"matchCase": true
				  // 		}
				  // 	}
				  // }
				{
					"replaceAllText": {
						"replaceText": description,
						"pageObjectIds": [],
						"containsText": {
							"text": "<Description>",
							"matchCase": true
						}
					}
				},
				{
					"replaceAllText": {
						"replaceText": deal_summary,
						"pageObjectIds": [],
						"containsText": {
							"text": "<Summary of the proposal 1>",
							"matchCase": true
						}
					}
				},
				{
					"replaceAllText": {
						"replaceText": lead_overview_1,
						"pageObjectIds": [],
						"containsText": {
							"text": "<lead overview 1>",
							"matchCase": true
						}
					}
				},
				{
					"replaceAllText": {
						"replaceText": lead_overview_2,
						"pageObjectIds": [],
						"containsText": {
							"text": "<Lead overview 2>",
							"matchCase": true
						}
					}
				},
				{
					"replaceAllText": {
						"replaceText": customer_name,
						"pageObjectIds": [],
						"containsText": {
							"text": "<Customer Name>",
							"matchCase": true
						}
					}
				},
				{
					"replaceAllText": {
						"replaceText": moment().format("DD/MM/YYYY"),
						"pageObjectIds": [],
						"containsText": {
							"text": "<DD/MM/YYYY>",
							"matchCase": true
						}
					}
				}

			  ],
			  "writeControl": {
				"requiredRevisionId": requiredRevisionId
			  }
			})
			
		var config = {
		  method: 'post',
		  url: 'https://slides.googleapis.com/v1/presentations/' + this.slideID + ':batchUpdate',
		  headers: { 
			'Authorization': 'Bearer ' + this.token,
			'Content-Type': 'text/plain'
		  },
		  data : data
		};
	
		// send the request
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			console.log('Slide updated');
		} catch (err) {
			//send request again if fail
			this.updatePresentaion(description, deal_summary, lead_overview_1, lead_overview_2, customer_name);
		}
	}
}