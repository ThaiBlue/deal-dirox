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
        nagivated: false,
        profile: {},
        deals: [],
        googleToken: {},
        huspotToken: {},
        folder: [],
        currentSlideID: '',
        currentDeal: 0,
        currentCompanyName: '',
        currentFolderId: 0,
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
                        resolve(response)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        fetchDeals(context) {
            /* 
                retrive deals from backend server 
            */
            return new Promise((resolve, reject) => {
                axios.get('/services/hubspot/crm/deals/makeoffer/all')
                    .then(response => {
                        response.data.results.forEach(item => {
                            this.state.deals.push({
                                id: item.id,
                                projectname: item.properties.dealname,
                                status: 'Make Offer',
                                startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                                enddate: moment(item.properties.closedate).format('DD/MM/YYYY'),
                                description: item.properties.description,
                                deal_summary: item.properties.deal_summary,
                                lead_overview_1: item.properties.lead_overview_1,
                                lead_overview_2: item.properties.lead_overview_2
                            })
                        });
                        resolve(response);
                    })
                    .catch(err => {
                        reject(err);
                    })
            })
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
            await context.dispatch('fetchAccessToken');
            const drive = new DriveAPI(this.state.googleToken.access_token);
            var response = await drive.getListOfFolder();
            const owned = [];
            await response.data.files.forEach(item => {
                if (item.ownedByMe) {
                    owned.push({
                        id: item.id,
                        label: item.name,
                        parents: item.parents[0],
                        children: []
                    })
                }
            })
            const idMapping = owned.reduce((acc, el, i) => {
                acc[el.id] = i;
                return acc;
            }, {});
            await owned.forEach(item => {
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
            var parentID = folderInfo.parentID;
            if (folderInfo.parentID === null) {
                parentID = [];
            }
            var response = await drive.createFolder(folderInfo.name, folderInfo.parentID);
            this.state.folder.push(response.data);
        },
        async prepareForInitLead(context) {
            /* 
                inner function that handle createInitLead prepare prossess 
            */
            axios.get('services/hubspot/crm/deals/' + this.state.deals[this.state.currentDeal].id + '/associations/company/info')
                .then(response => {
                    this.state.currentCompanyName = response.data.properties.name;
                })
                .catch(err => {
                    return Promise.reject(err.response);
                })

            const form = new FormData();
            
            // form.append('name', );
            form.append('parentID', this.state.currentFolderId);
            
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
            const slide = new SlideAPI(this.state.googleToken.access_token, this.state.currentSlideID);
            var res = await slide.updatePresentaion(
                this.state.deals[this.state.currentDeal].description,
                this.state.deals[this.state.currentDeal].deal_summary,
                this.state.deals[this.state.currentDeal].lead_overview_1,
                this.state.deals[this.state.currentDeal].lead_overview_2,
                this.state.currentCompanyName)

        },
        assignSlideID(context, ID) {
            /* asign current selected SideID actions */
            this.state.currentSlideID = ID;
        },
        assignCurrentFolderID(context, ID) {
            /* assign current selected ID actions */
            this.state.currentFolderId = ID;
        },
        resetFolder(context) {
            this.state.folder = [];
        }
    }
})

export default store