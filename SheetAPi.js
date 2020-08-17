module.exports = class SheetAPI {
	constructor (token, sheetID) {
		this.token = token;
		this.sheetID = sheetID;
	}
	
	async updateSheet (deal) {
		var axios = require('axios');
		var data = JSON.stringify(
			{
				"valueInputOption": "USER_ENTERED",
				"data": [
					{
						"range": "A1:AZ100",
						"values": JSON.stringify(array)
					}]
			});
			
		var config = {
		  method: 'post',
		  url: 'https://sheets.googleapis.com/v4/spreadsheets/' + this.sheetID +'/values:batchUpdate',
		  headers: { 
			'Authorization': 'Bearer ' + this.token, 
			'Content-Type': 'text/plain'
		  },
		  data : data
		};
		
		// sending the request 
		axios(config)
		.then(function (response) {
			console.log(JSON.stringify(response.data));
		  })
		.catch(function (error) {
		console.log(error);
		});	
	}
}