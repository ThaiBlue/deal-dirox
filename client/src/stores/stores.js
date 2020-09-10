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
        // token:localStorage.getItem('access_token') || null,
        profile: {},
        deals: [],
        googleToken: {},
        huspotToken: {},
        folder: [],
        currentSlide: {},
        currentDeal: {},
        currentCompany: {},
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
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('user_id', credentials.username);
                form.append('password', credentials.password);
                axios.post('/accounts/user/login', form)
                    .then(response => {
                        //parse user info from response
                        this.state.profile = response.data;
                        resolve(response);
                    })
                    .catch(error => {
                        console.log(error);
                        reject(error);
                    })
            })
        },
        fetchDeals(context) {
            return new Promise((resolve, reject) => {
                //Fetch data from server
                // moment(item.properties.start_date).format('DD/MM/YYYY')
                axios.get('/services/hubspot/crm/deals/makeoffer/all')
                    .then(response => {
                        response.data.results.forEach(item => {
                            this.state.deals.push({
                                id: item.id,
                                projectname: item.properties.dealname,
                                status: 'Make Offer',
                                startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                                enddate: moment(item.properties.closedate).format('DD/MM/YYYY')
                            })
                        });
                        resolve(response);
                    })
                    .catch(error => {
                        console.log(error);
                        reject(error);
                    })
            })
        },
        fetchAccessToken(context, service) {
            /*
                static function 
                service must be 'google' or 'hubspot'
            */
            return new Promise((resolve, reject) => {
                axios.get('/services/' + service + '/auth/token')
                    .then(response => {
                        if(service=='google') {
                            console.log('google token')
                            this.state.googleToken = response.data;
                        }
                        if(service=='hubspot') {
                            console.log('hubspot token')
                            this.state.hubspotToken = response.data;
                        }
                        resolve(response);
                    })
                    .catch(error => {
                        console.log(error);
                        reject(error);
                    })
            })
        },
        fetchFolder(context) {
            return new Promise((resolve, reject) => {
                context.dispatch('fetchAccessToken', 'google')
                    .then(response => {
                        const drive = new DriveAPI(this.state.googleToken.access_token)
                        drive.getListOfFolder().then(response => {
                            response.data.files.forEach(item => {
                                if (item.ownedByMe) {
                                    this.state.folder.push(item);
                                }
                            });
                            resolve(response);
                        }).catch(error => {
                            console.log(error);
                            reject(error);
                        })
                    })
                    .catch(error => {
                        console.log(error);
                        reject(error);
                    })
            })
        },
        createFolder(context, folderInfo) {
            /*
                folderInfo : {
                    name: new folder name,
                    parentID: ID of the parent folder
                }
            */
            return new Promise((resolve, reject) => {
                context.dispatch('fetchAccessToken', 'google')
                    .then(response => {
                        const drive = new DriveAPI(this.state.googleToken.access_token)
                        drive.createFolder().then(response => {
                            this.state.folder.push(response.data);
                            resolve(response);
                        }).catch(error => {
                            console.log(error);
                            reject(error);
                        })
                    })
                    .catch(error => {
                        console.log(error);
                        reject(error);
                    })
            })

        },
        prepareForInitLead(context) {
            return new Promise((resolve, reject) => {
                console.log('create initlead init');
                axios.get('services/hubspot/crm/deals/<str:dealID>/associations/company/info')
                    .then(response => {
                        console.log(response)
                        this.state.currentCompany = response.data;
                    })
                    .catch(error => {
                        console.log(error);
                        return Promise.reject(error);
                    })
            axios.get('/services/google/drive/file/create/initlead')
                    .then(response => {
                        console.log('upload initlead:')
                        console.log(response.data)
                        this.state.currentSlide = response.data;
                    })
                    .catch(error => {
                        console.log(error);
                        return Promise.reject(error);
                    })
            })
        },
        createInitLead(context) {
            return new Promise((resolve, reject) => {
                console.log('create initlead');
                context.dispatch('prepareForInitLead').then(response => {
                    const slide = SlideAPI(this.state.huspotToken.access_token, this.state.currentSlide.id)
                    slide.updatePresentaion(
                        this.state.currentDeal.properties.description,
                        this.state.currentDeal.properties.deal_summary,
                        this.state.currentDeal.properties.lead_overview_1,
                        this.state.currentDeal.properties.lead_overview_2,
                        this.state.currentCompany.properties.name
                        ).then(response => {
                            console.log(response.data);
                            return Promise.resolve(response.data);
                        }).catch(error => {
                            console.log(error)
                            return Promise.reject(error);
                        })
                })
            })
        }
    }
})

export default store