module.exports = class SheetAPI {
	constructor(token, sheetID) {
		this.token = token;
		this.sheetID = sheetID;
		this.axios = require('axios');
	}

	async updateSheet(deal) {
		var data = JSON.stringify({
			"valueInputOption": "USER_ENTERED",
			"data": [{
				"range": "A1:AZ100",
				"values": JSON.stringify(array)
			}]
		});

		var config = {
			method: 'post',
			url: 'https://sheets.googleapis.com/v4/spreadsheets/' + this.sheetID + '/values:batchUpdate',
			headers: {
				'Authorization': 'Bearer ' + this.token,
				'Content-Type': 'text/plain'
			},
			data: data
		};

		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data;

		} catch (err) {
			if (err.response.status == 408) {
				//send request again if request time out
				this.updateSheet(deal);
			}
			//return error code
			return err.response.status;
		}
	}
}