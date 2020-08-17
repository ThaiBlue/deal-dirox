async function main() {
	var HubspotAPI = require('./HubspotAPI.js');
	var SlideAPI = require('./SlideAPI.js');
	var hubspotToken = 'CJzT5-W_LhICAQEY1rSfAyC74cEFKOfFDTIZAJvykNbjkwYThybUcCvRGUOX1c349wZ6xDoaAAoCQQAADIACAAgAAAABAAAAAAAAABjAABNCGQCb8pDW6R4pwQBFrrwxIIQjFhd-bJK-i0c';
	var googleToken = 'ya29.a0AfH6SMBj5LfZ45PKvU-whrJDUb5g8slK-O3yTIKUCwaTAThBDl8yPPECgrCB14JR-db_4zVvn11S2C_rlc10QdA03IrmJQR_Q6wc2OCvzQMWlIWeU1xVBh1Si4R5rswZkY72pSdnwipy_FzlGei7Be4ZODobRg7fvCdNYRp4oEoT410'
	var prop = [
		"dealname",
		"description",
		"deal_summary",
		"lead_overview_1",
		"lead_overview_2"
	];
	var slideID = '1iaBhskmKeB7hnsd7mgMWtLi8SEfNzVFGPeIpQq5QUfE';
	var slideapi = new SlideAPI(googleToken, slideID);
	var hubspotapi = new HubspotAPI(hubspotToken);
	var deals = await hubspotapi.fetchMakeOfferDeals(prop);
	console.log(deals);
	var deal = deals[0]; //choose a deal in list deal to make Initlead from
	var companyInfo = await hubspotapi.getCompanyInfo(deal.id)
	console.log(companyInfo)
	slideapi.updatePresentaion(deal.properties.description, deal.properties.deal_summary, deal.properties.lead_overview_1, deal.properties.lead_overview_2, companyInfo.properties.name)	
}

main()