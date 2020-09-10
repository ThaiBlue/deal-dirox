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
                service must be 'google' or 'hubspot'
            */
            return new Promise((resolve, reject) => {
                axios.get('/services/' + service + '/auth/token')
                    .then(response => {
                        this.state.googleToken = response.data;
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
                this.$store.dispatch('fetchAccessToken', 'google')
                    .then(response => {
                        const drive = new DriveAPI(this.$store.state.googleToken.access_token)
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
                this.$store.dispatch('fetchAccessToken')
                    .then(response => {
                        const drive = new DriveAPI(this.$store.state.googleToken.access_token)
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
        createInitLead(context) {
            return new Promise((resolve, reject) => {
                exec()
                function init() {
                    this.$store.dispatch('fetchAccessToken', 'hubspot')
                        .then(response => {
                            this.state.huspotToken = response.data;
                            const hubspot = new HubspotAPI(response.data.access_token);
                            hubspot.getCompanyInfo(this.$store.state.currentDeal.id)
                                .then(response => {
                                    this.state.currentCompany = response;
                                })
                                .catch(error => {
                                    console.log(error);
                                    reject(error);
                                })
                        })
                        .catch(error => {
                            console.log(error);
                            reject(error);
                        })
                    axios.get('/services/google/drive/file/create/initlead')
                        .then(response => {
                            this.state.currentSlide = response.data;
                        })
                        .catch(error => {
                            console.log(error);
                            reject(error);
                        })
                }
                async function exec() {
                    await init()
                    const slide = SlideAPI(this.$store.state.huspotToken.access_token, this.$store.state.currentSlide.id)
                    slide.updatePresentaion(
                        this.$store.state.currentDeal.properties.description,
                        this.$store.state.currentDeal.properties.deal_summary,
                        this.$store.state.currentDeal.properties.lead_overview_1,
                        this.$store.state.currentDeal.properties.lead_overview_2,
                        this.$store.state.currentCompany.properties.name
                    ).then(response => {
                        console.log(response.data);
                        resolve(response.data);
                    }).catch(error => {
                        console.log(error)
                        reject(error)
                    })
                }
            })
        }
    }
})

export default store