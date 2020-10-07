import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import FormData from 'form-data'
import moment from 'moment'
import DriveAPI from '../assets/js/DriveAPI'

Vue.use(Vuex)
axios.defaults.baseURL = 'https://api.deal.dirox.dev'
// axios.defaults.baseURL = 'http://127.0.0.1:8000'

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
        selectFunctionCache: '',
        newFolderName: ''
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
        logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('expiration_time');
        },
        authenticate(context, credentials) {
            /* 
                send authenticate request to backend server 
            */            
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('user_id', credentials.username);
                form.append('password', credentials.password);
                axios.post('/accounts/user/authorize', form)
                    .then(response => {
                        //parse user info from response
                        localStorage.setItem('access_token', response.data.access_token)
                        localStorage.setItem('expiration_time', response.data.expiration_time)
                        context.dispatch('fetchProfile');
                        resolve(response);
                    })
                    .catch(err => {
                        window.alert("Login fail. Wrong user id or password. Please try again!!!")
                        reject(err);
                    })
            })
        },
        fetchProfile() {
            return new Promise((resolve, reject) => {
                
                var config = {
                    url: 'https://api.deal.dirox.dev/accounts/user/profile',
                    method: 'get',
                    headers: {
                        'Authorization': 'Bearer '+ localStorage.access_token
                    }
                }
                axios(config)
                .then(response => {
                    this.state.profile = response.data;
                })
                .catch(err => {
                    
                })
            })
        },
        async retrieveFolderMetaData(context, payload) {
            /* Return name and url of the Drive folder 
            payload = {
                folder_id: string,
                deal_id: string
            }
             */
            try {
                await context.dispatch('fetchAccessToken', 'google');
            } catch (err) {
                console.log(err)
            }

            var config = {
                url: 'https://www.googleapis.com/drive/v3/files/' + payload.folder_id + '?fields=*',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer ' + this.state.googleToken.access_token
                }
            }

            try {
                var res = await axios(config);

                if (res.data.trashed) {
                    this.state.folderCacheData = {
                        id: '',
                        name: '',
                        url: ''
                    };
                    context.dispatch('updateCache', {
                        dealID: payload.deal_id,
                        folderID: '',
                        status: ''
                    });
                } else {
                    this.state.folderCacheData = {
                        id: res.data.id,
                        name: res.data.name,
                        url: res.data.webViewLink
                    }
                }
            } catch (err) {
                this.state.folderCacheData = {
                    id: '',
                    name: '',
                    url: ''
                };
            }

        },
        async fetchDeals(context) {
            /* 
                retrive deals and cache from backend server
            */

            try {
                var config = {
                    url: 'https://api.deal.dirox.dev/services/hubspot/crm/deals/makeoffer/all',
                    method: 'get',
                    headers: {
                        'Authorization': 'Bearer '+ localStorage.access_token
                    }
                }
                
                var response = await axios(config)

                response.data.results.forEach(async (item, index) => {
                    var cache = response.data.caches.filter(el => el.deal_id == item.id)[0]; // [0] is unpack the single element array
                    if (cache === undefined) {
                        this.state.folderCacheData = {
                            id: '',
                            name: '',
                            url: ''
                        }
                    } else {
                        await context.dispatch('retrieveFolderMetaData', {folder_id: cache.folder_id, deal_id: cache.deal_id})
                    }
                    this.state.deals.push({
                        id: item.id,
                        projectname: item.properties.dealname,
                        stage: 'Make Offer',
                        startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                        enddate: moment(item.properties.closedate).format('DD/MM/YYYY'),
                        status: (cache === undefined || cache.folder_id === '' || this.state.folderCacheData.id === '') ? '' : cache.status,
                        folder: this.state.folderCacheData
                    })
                });

            } catch (err) {
                console.log(err)
            }

        },
        fetchAccessToken() {
            /*
                fetch access token from backend server
            */
           
            var config = {
                url: 'https://api.deal.dirox.dev/services/google/auth/token',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            }

            return new Promise((resolve, reject) => {
                axios(config)
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
                    if(item.ownedByMe) {
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
                    parentID: ID of the parent folder,
                    subFolder: array
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
                await context.dispatch('retrieveFolderMetaData', {folder_id: response.data.id, deal_id: this.state.currentDeal.id});

                var index = this.state.deals.indexOf(this.state.currentDeal);

                this.state.deals[index].folder = this.state.folderCacheData;
                this.state.deals[index].status = 'folder-created';
                
                // this.state.folder.push(response.data);

                if (folderInfo.subFolder.includes('00. Customer documents')) {
                    try {
                        drive.createFolder('00. Customer documents', [response.data.id]);
                    } catch (err) {
                        console.log(response)
                    }
                }
                if (folderInfo.subFolder.includes('01. Proposal')) {
                    try {
                        drive.createFolder('01. Proposal', [response.data.id]);
                    } catch (err) {
                        console.log(err)
                    }
                }
                if (folderInfo.subFolder.includes('02. Contract')) {
                    try {
                        drive.createFolder('02. Contract', [response.data.id]);
                    } catch (err) {
                        console.log(err)
                    }
                }

            } catch (err) {
                console.log(err);
            }
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
                       
            try {
                const form = new FormData();
                form.append('deal_id', this.state.currentDeal.id);
                form.append('parentID', this.state.currentFolderId);
                
                var config = {
                    url: 'https://api.deal.dirox.dev/services/google/drive/file/create/initlead',
                    method: 'post',
                    headers: {
                        'Authorization': 'Bearer '+ localStorage.access_token
                    },
                    data: form
                };
                var response = await axios(config)
                // get index of current deal
                var index = this.state.deals.indexOf(this.state.currentDeal);
                this.state.deals[index].status = 'transfer-to-ba';
                context.dispatch('updateCache', {
                    dealID: this.state.deals[index].id,
                    folderID: this.state.deals[index].folder.id,
                    status: 'transfer-to-ba'
                })
                window.alert("Transfer to BA successed")

            } catch (err) {
                window.alert("Transfer to BA failed")
                console.log(err)
            }

        },
        assignSlideID(ID) {
            /* asign current selected SideID actions */
            this.state.currentSlideID = ID;
        },
        assignCurrentFolderID(ID) {
            /* assign current selected ID actions */
            this.state.currentFolderId = ID;
        },
        fetchGoogleAccountInfo() {
            /* Fetch service infomation or registered google account email info */
            
            var config = {
                url: 'https://api.deal.dirox.dev/services/google/info',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            }

            return new Promise((resolve, reject) => {
                axios(config)
                    .then(res => {
                        this.state.googleAccountEmail = res.data.emailAddress;
                        resolve(res);
                    })
                    .catch(err => {
                        this.state.profile.service.google.is_available = false;
                        reject(err);
                    })
            })
        },
        fetchHubspotAccountInfo() {
            /* Fetch service infomation or registered hubspot account email info */
            
            var config = {
                url: 'https://api.deal.dirox.dev/services/hubspot/info',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            }

            return new Promise((resolve, reject) => {
                axios(config)
                    .then(res => {
                        this.state.hubspotAccountEmail = res.data.user;
                        resolve(res);
                    })
                    .catch(err => {
                        this.state.profile.service.hubspot.is_available = false;
                        reject(err);
                    })
            })
        },
        updateCache(payload) {
            /* update cache from both client and server side */
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('status', payload.status);
                form.append('folder_id', payload.folderID);
                form.append('deal_id', payload.dealID);
                
                var config = {
                    url: 'https://api.deal.dirox.dev/accounts/setting/cache',
                    method: 'post',
                    headers: {
                        'Authorization': 'Bearer '+ localStorage.access_token
                    },
                    data: form
                };
                
                axios(config)
                    .then(res => {
                        resolve(res);
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err);
                    })
            })
        },
        googleCredentialRevoke() {
            /* Remove access right for this app */
            
            var config = {
                url: 'https://api.deal.dirox.dev/services/google/auth/token/revoke',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            };

            return new Promise((resolve, reject) => {
                axios(config)
                    .then(res => {
                        this.state.profile.service.google.is_available = false;
                        resolve(res);
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err);
                    })
            })
        },
        hubspotCredentialRevoke() {
            /* Remove access right for this app */
            
            var config = {
                url: 'https://api.deal.dirox.dev/services/hubspot/auth/token/revoke',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            };

            return new Promise((resolve, reject) => {
                axios(config)
                    .then(res => {
                        this.state.profile.service.hubspot.is_available = false;
                        resolve(res);
                    })
                    .catch(err => {
                        console.log(err);
                        reject(err);
                    })
            })
        },
        updateNewFolderName(name) {
            // Cache new folder name that typed from Create folder popup
            this.state.newFolderName = name;
        },
        resetSelect() {
            // reset all selection on deal page
            this.state.currentDeal = {};
            this.state.selectFunctionCache = '';
        },
        registerService(context, service) {
            /* 
                Register third party service for this app
            */
           
            if(!['google', 'hubspot'].includes(service)) {
                throw new Error('service must be google or hubspot');
            }
            
            var config = {
                url: 'https://api.deal.dirox.dev/accounts/' + service + '/auth',
                method: 'get',
                headers: {
                    'Authorization': 'Bearer '+ localStorage.access_token
                }
            };

            return new Promise((resolve, reject) => {
                axios(config)
                    .then(res => {
                        // console.log()
                        window.location.replace(res.data.redirect_url)
                        resolve(res);
                    })
                    .catch(err => {
                        console.log(err);
                        reject(err);
                    })
            })

        },
    }
})

export default store
