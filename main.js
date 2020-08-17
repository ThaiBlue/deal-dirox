async function main() {
	var HubspotAPI = require('./HubspotAPI.js');
	var SlideAPI = require('./SlideAPI.js');
	var hubspotToken = 'CJzT5-W_LhICAQEY1rSfAyC74cEFKOfFDTIZAJvykNbjkwYThybUcCvRGUOX1c349wZ6xDoaAAoCQQAADIACAAgAAAABAAAAAAAAABjAABNCGQCb8pDW6R4pwQBFrrwxIIQjFhd-bJK-i0c';
	var googleToken = 'ya29.a0AfH6SMDTP6UASPxqYuBZZecdVPTwsZHzWr0O1InZTS_5M_MhJda3adZwbeexfJBPftObC_n5CEhLgpAd1gx9YD1PxtcQ22v-elTTeT1hOFWyv7KquZKrIbKhl74RQ1ejG8LZy9HAxipE6Gvua2VQ4kxjJBnUa37zbfKw0w4QN158mVQ'
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
	var deal = deals[6]; //choose a deal in list deal to make Initlead from
	var companyInfo = await hubspotapi.getCompanyInfo(deal.id)
	console.log(companyInfo)
	slideapi.updatePresentaion(deal.properties.description, deal.properties.deal_summary, deal.properties.lead_overview_1, deal.properties.lead_overview_2, companyInfo.properties.name)	
}

main()