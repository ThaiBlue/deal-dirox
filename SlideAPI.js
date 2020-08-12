class SlideAPI {
	constructor (token, slideID) {
		this.token = token;
		this.slideID = slideID;
	}
	
	async getSlideRevisionID() {
		var axios = require('axios');
		var config = {
		  method: 'get',
		  url: 'https://slides.googleapis.com/v1/presentations/' + this.sheetID,
		  headers: { 
			'Authorization': 'Bearer ' + this.token
		  }
		};
		
		// start fetching data
		var response = await axios(config);
		
		return response.data.revisionId;
	}
	
	async updatePresentaion (deal) {
		var axios = require('axios');
		var requiredRevisionId = await this.getSlideRevisionID();
		var data = JSON.stringify(
			{
			  "requests": [
				{
					"replaceAllText": {
						"replaceText": deal.properties.description,
						"pageObjectIds": [],
						"containsText": {
							"text": "<Description>",
							"matchCase": true
						}
					}
				}
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
		axios(config)
		.then(function (response) {
		  console.log(JSON.stringify(response.data));
		})
		.catch(function (error) {
		  console.log(error);
		});
	}
}