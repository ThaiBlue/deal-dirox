import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import FormData from 'form-data'
import moment from 'moment'


Vue.use(Vuex)
axios.defaults.baseURL = 'https://api.deal.dirox.dev'
axios.defaults.withCredentials = true

export const store = new Vuex.Store({
    state: {
        // token:localStorage.getItem('access_token') || null,
        profile: {},
        deals: []
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
        // user_id: test
        // password: w7crD9pqCM8
        authenticate(context, credentials) {
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('user_id', credentials.username);
                form.append('password', credentials.password);
                axios.post('/accounts/user/login', form)
                    .then(response => {
                        // const token = response.data.access_token
                        // localStorage.setItem('access_token', token)
                        // context.commit('retriveToken', token)

                        //parse user info from response
                        this.state.profile = response.data;
                        resolve(response);
                    })

                    .catch(error => {
                        console.log(error);
                        console.log('error here');
                        reject(error);
                    })
            })
        },
        
        fetchDeals(context) {
            return new Promise((resolve, reject) => {
                //Fetch data from server 
                // moment(item.properties.start_date).format('DD/MM/YYYY')
                axios.get('/services/crm/hubspot/deals/makeoffer/all', { withCredentials: true }).then(response => {
                    response.data.results.forEach(item => {
                        this.state.deals.push({
                            id: item.id,
                            projectname: item.properties.dealname,
                            status: 'Make Offer',
                            startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                            enddate: moment(item.properties.closedate).format('DD/MM/YYYY')
                        })
                    });
                })
            })
        }

    }
})

export default store