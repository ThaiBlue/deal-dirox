module.exports = class DriveAPI {
	/*
	Interact with Drive APi to manage Google Drive data
	* token {String} - Bearer token to grant access to Google API
	*/
	constructor(token) {
		this.token = token;
		this.axios = require('axios');
	}

	async getListOfFolder() {
		/*
		Implement Drive API to retrieve Drive folder data
		*/
		var config = {
			method: 'get',
			url: 'https://www.googleapis.com/drive/v3/files?q=mimeType=\'application/vnd.google-apps.folder\'andtrashed=false&fields=files(id,name,mimeType,ownedByMe,parents)',
			headers: {
				'Authorization': 'Bearer ' + this.token
			}
		};

		// connection handler
		try {
			// send request
			var response = await this.axios(config);
			//return fetched data
			return response.data;
			
		} catch (err) {
			if (err.code=408) {
				//send request again if request time out
				this.getListOfFolder();				
			}
			//return error code
			return err.code;
		}
	}

	async importFile() {

	}
}