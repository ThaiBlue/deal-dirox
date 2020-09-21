import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import FormData from 'form-data'
import moment from 'moment'
import DriveAPI from '../assets/js/DriveAPI'
import SlideAPI from '../assets/js/SlideAPI'
import HubspotAPI from '../assets/js/HubspotAPI'

Vue.use(Vuex)
axios.defaults.baseURL = 'https://api.deal.dirox.dev'
axios.defaults.withCredentials = true

export const store = new Vuex.Store({
    state: {
        folder: [], // store all drive folder meta data
        profile: {}, // store user profile
        deals: [], // store all make offer deal
        googleToken: {}, // store google crendential
        googleAccountEmail: '', // store connected google account email 
        hubspotAccountEmail: '', // store connected hubspot account email 

        currentSlideID: '', // cache current created slide ID
        currentDeal: {}, // cache current deal object
        currentCompanyName: '', // cache current fetched company name
        currentFolderId: null, // cache current selected folder id
        folderCacheData: {}, // cache current fetched folder meta data
        idMappingForDeals: [], //cache deal indice
        isLoged: false
    },
    getters: {
        // loggedIn(state) {
        //     return state.token !== null
        // }
    },
    mutations: {
        // retriveToken(state, token) {
        //     state.token = token
        // }
    },
    actions: {
        authenticate(context, credentials) {
            /* 
                send authenticate request to backend server 
            */
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('user_id', credentials.username);
                form.append('password', credentials.password);
                axios.post('/accounts/user/login', form)
                    .then(response => {
                        //parse user info from response
                        this.state.profile = response.data;
                        context.dispatch('fetchDeals');
                        resolve(response);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
        },
        async retrieveFolderMetaData(context, folder_id) {
            /* Return name and url of the Drive folder 
            payload: {
                caches: cache object,
                deal: deal object
            }
            */
            await context.dispatch('fetchAccessToken', 'google');

            var config = {
                url: 'https://www.googleapis.com/drive/v3/files/' + folder_id + '?fields=*',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer ' + this.state.googleToken.access_token
                }
            }

            try {
                var res = await axios(config)

                this.state.folderCacheData = {
                    id: res.data.id,
                    name: res.data.name,
                    url: res.data.webViewLink
                }

            } catch (err) {
                this.state.folderCacheData = {
                    id: '',
                    name: '',
                    url: ''
                }
            }

        },
        async fetchDeals(context) {
            /* 
                retrive deals and cache from backend server
            */

            try {
                // var deals = [];
                var response = await axios.get('/services/hubspot/crm/deals/makeoffer/all')

                response.data.results.forEach(async (item, index) => {
                    var cache = response.data.caches.filter(el => el.deal_id == item.id)[0];

                    if (cache === undefined) {
                        this.state.folderCacheData = {
                            id: '',
                            name: '',
                            url: ''
                        }
                    } else {
                        await context.dispatch('retrieveFolderMetaData', cache.folder_id)
                    }
                    this.state.deals.push({
                        id: item.id,
                        projectname: item.properties.dealname,
                        stage: 'Make Offer',
                        startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                        enddate: moment(item.properties.closedate).format('DD/MM/YYYY'),
                        description: item.properties.description,
                        deal_summary: item.properties.deal_summary,
                        lead_overview_1: item.properties.lead_overview_1,
                        lead_overview_2: item.properties.lead_overview_2,
                        status: (cache === undefined) ? '' : cache.status, // [0] is unpack the single element array
                        folder: this.state.folderCacheData
                    })
                });

            } catch (err) {
                console.log(err)
            }

        },
        fetchAccessToken(context) {
            /*
                fetch access token from backend server
            */
            return new Promise((resolve, reject) => {
                axios.get('/services/google/auth/token')
                    .then(response => {
                        this.state.googleToken = response.data;
                        resolve(response);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
        },
        async fetchFolder(context) {
            /* 
                get folder meta data from google drive 
            */
            this.state.folder = [];
            var owned = [];

            await context.dispatch('fetchAccessToken');
            const drive = new DriveAPI(this.state.googleToken.access_token);

            try {
                var response = await drive.getListOfFolder();
                response.data.files.forEach(item => {
                    if (item.ownedByMe) {
                        owned.push({
                            id: item.id,
                            label: item.name,
                            parents: item.parents[0],
                            children: []
                        })
                    }
                })

            } catch (err) {
                console.log(err)
            }

            const idMapping = owned.reduce((acc, el, i) => {
                acc[el.id] = i;
                return acc;
            }, {});

            owned.forEach(item => {
                // Handle the root element
                if (idMapping[item.parents] === undefined) {
                    this.state.folder.push(item);
                    return;
                }
                // Use our mapping to locate the parent element in our data array
                const parentEl = owned[idMapping[item.parents]];
                // Add our current el to its parent's `children` array
                parentEl.children.push(item)
            })
        },
        async createFolder(context, folderInfo) {
            /*
                folderInfo : {
                    name: new folder name,
                    parentID: ID of the parent folder
                }
            */
            await context.dispatch('fetchAccessToken', 'google');
            const drive = new DriveAPI(this.state.googleToken.access_token);
            var parentID = [];
            if (folderInfo.parentID[0] !== null) {
                parentID = folderInfo.parentID;
            }
            try {
                var response = await drive.createFolder(folderInfo.name, parentID);
                context.dispatch('updateCache', {
                    dealID: this.state.currentDeal.id,
                    folderID: response.data.id,
                    status: 'folder-created'
                });

                // update frondend cache
                await context.dispatch('retrieveFolderMetaData', response.data.id);
                
                var index = this.state.deals.indexOf(this.state.currentDeal);
                
                this.state.deals[index].folder = this.state.folderCacheData;
                this.state.deals[index].status = 'folder-created';
                
                this.state.folder.push(response.data);
            } catch (err) {
                console.log(err);
            }
        },
        async prepareForInitLead(context) {
            /* 
                inner function that handle createInitLead prepare prossess 
            */
            axios.get('services/hubspot/crm/deals/' + this.state.currentDeal.id + '/associations/company/info')
                .then(response => {
                    this.state.currentCompanyName = response.data.properties.name;
                })
                .catch(err => {
                    return Promise.reject(err.response);
                })

            // form.append('name', );
            const form = new FormData();
            if (this.state.currentFolderId !== null) {
                form.append('parentID', this.state.currentFolderId);
            }

            await axios.post('/services/google/drive/file/create/initlead', form)
                .then(response => {
                    this.state.currentSlideID = response.data.id;
                })
                .catch(err => {
                    return Promise.reject(err.response);
                })
        },
        assignCurrentDeal(context, currentDeal) {
            /* 
                assign current selected deal 
            */
            this.state.currentDeal = currentDeal;
        },
        async createInitLead(context) {
            /*
                send create InitLead request to google service
            */
            await context.dispatch('prepareForInitLead');
            await context.dispatch('fetchAccessToken');
            await context.dispatch('generateIdMapping');
            const slide = new SlideAPI(this.state.googleToken.access_token, this.state.currentSlideID);
            try {
                var res = await slide.updatePresentaion(
                    this.state.currentDeal.description,
                    this.state.currentDeal.deal_summary,
                    this.state.currentDeal.lead_overview_1,
                    this.state.currentDeal.lead_overview_2,
                    this.state.currentCompanyName);
                
                // get index of current deal
                var index = this.state.deals.indexOf(this.state.currentDeal);
                this.state.deals[index].status = 'transfer-to-ba'
                
            } catch (err) {
                console.log(err)
            }

        },
        assignSlideID(context, ID) {
            /* asign current selected SideID actions */
            this.state.currentSlideID = ID;
        },
        assignCurrentFolderID(context, ID) {
            /* assign current selected ID actions */
            this.state.currentFolderId = ID;
        },
        fetchGoogleAccountInfo(context) {
            /* Fetch service infomation or registered google account email info */
            return new Promise((resolve, reject) => {
                axios.get('services/google/info')
                    .then(res => {
                        this.state.googleAccountEmail = res.data.emailAddress;
                        resolve(res);
                    })
                    .catch(err => {
                        this.state.googleAccountEmail = 'No service';
                        reject(err);
                    })
            })
        },
        fetchHubspotAccountInfo(context) {
            /* Fetch service infomation or registered hubspot account email info */
            return new Promise((resolve, reject) => {
                axios.get('services/hubspot/info')
                    .then(res => {
                        this.state.hubspotAccountEmail = res.data.user;
                        resolve(res);
                    })
                    .catch(err => {
                        this.state.hubspotAccountEmail = 'No service';
                        reject(err);
                    })
            })
        },
        updateCache(context, payload) {
            /* update cache from both client and server side */
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('status', payload.status);
                form.append('folder_id', payload.folderID);
                form.append('deal_id', payload.dealID);
                axios.post('accounts/setting/cache', form)
                    .then(res => {
                        resolve(res);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
        },
        googleCredentialRevoke(context) {
            return new Promise((resolve, reject) => {
                axios.get('services/google/auth/token/revoke')
                    .then(res => {
                        this.state.googleAccountEmail = 'No service';
                        resolve(res);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
        },
        hubspotCredentialRevoke(context) {
            return new Promise((resolve, reject) => {
                axios.get('services/hubspot/auth/token/revoke')
                    .then(res => {
                        this.state.hubspotAccountEmail = 'No service';
                        resolve(res);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
        }
    }
})

export default store