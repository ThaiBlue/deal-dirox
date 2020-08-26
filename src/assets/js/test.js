async function main() {
	var HubspotAPI = require('./HubspotAPI.js');
	var SlideAPI = require('./SlideAPI.js');
	// access token to access user data
	var hubspotToken = 'CMbq0Y7BLhICAQEY1rSfAyC74cEFKOfFDTIZAJ6YgzRa7OOXtpQdZ_I48tSTaEQfIgPrXjoaAAoCQQAADIACAAgAAAABAAAAAAAAABjAABNCGQCemIM0rxFH-47I0MvVWZlimXKokUDFIms';
	var googleToken = 'ya29.a0AfH6SMDw3xjoRrLQSlLVeLOK-kcvpNmWyF4GebP600WJj17bSyl-W5feMxvdtXgYX8NODcA84Erd7z87QG0Dj6oj_arRQXRaK6YheYtyBVsn3b1dWNobleUCjYb-ecvUpN4JzjDyIBiQu49wQiphHa18_dog0UN4MuD2';
	
	// modified properties if needed
	var prop = [
		"dealname",
		"description",
		"deal_summary",
		"lead_overview_1",
		"lead_overview_2"
	];
	// ID of the template slide
	var slideID = '1-MvAwMusL_lSbsDGN_1lfXatYEBBmqAIkncMGVL21cI';
	
	var slideapi = new SlideAPI(googleToken, slideID);
	var hubspotapi = new HubspotAPI(hubspotToken);
	
	var deals = await hubspotapi.fetchMakeOfferDeals(prop); // fetch all make offer deals
	console.log(deals);
	
	var deal = deals[11]; //choose a deal in list deal to make Initlead from
	
	// get customer info
	var companyInfo = await hubspotapi.getCompanyInfo(deal.id);
	console.log(companyInfo)
	
	//update the template
	slideapi.updatePresentaion(deal.properties.description, deal.properties.deal_summary, deal.properties.lead_overview_1, deal.properties.lead_overview_2, companyInfo.properties.name);	
}

main() 