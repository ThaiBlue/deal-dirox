module.exports = class SlideAPI {
	/*
	Interact with Googlw slide APi to modify a given presentation
	* token {String} - a string that represent Google API access token
	* slideID {String} - a string that represent the ID of a google slide presentation
	*/
	constructor(token, slideID) {
		this.token = token;
		this.slideID = slideID;
		this.axios = require('axios');
	}

	async getPresentationRevisionID() {
		/*
		Retrieve the RevisionID of the Presentation
		*/
		var config = {
			method: 'get',
			url: 'https://slides.googleapis.com/v1/presentations/' + this.slideID,
			headers: {
				'Authorization': 'Bearer ' + this.token
			}
		};

		// connection handler
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data.revisionId;
			
		} catch (err) {
			if (err.code = 408) {
				//send request again if request time out
				this.getPresentaionRevisionID();
			}
			//return error code
			return err.code;
		}
	}

	async updatePresentaion(description, deal_summary, lead_overview_1, lead_overview_2, customer_name) {
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
		var data = JSON.stringify({
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
						"replaceText": moment().format("DD/MM/YYYY"), //retrieve current date
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
			data: data
		};

		// connection handler
		try {
			// send request
			var response = await this.axios(config);
			//return response
			return response.data;

		} catch (err) {
			if (err.code = 408) {
				//send request again if request time out
				this.updatePresentaion(description, deal_summary, lead_overview_1, lead_overview_2, customer_name);
			}
			//return error code
			return err.code;
		}
	}
}