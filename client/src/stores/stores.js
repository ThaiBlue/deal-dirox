import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import FormData from 'form-data'


Vue.use(Vuex)
axios.defaults.baseURL = 'https://api.deal.dirox.dev'


export const store = new Vuex.Store({
    state: {
        // token:localStorage.getItem('access_token') || null,
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
        retriveToken(context, credentials) {
            return new Promise((resolve, reject) => {
                const form = new FormData();
                form.append('user_id', credentials.username);
                form.append('password', credentials.password);
                axios.post('/accounts/user/login', form)
                    .then(response => {
                        // const token = response.data.access_token
                        // localStorage.setItem('access_token', token)
                        // context.commit('retriveToken', token)
                        console.log(response)
                        console.log('Here ?')
                        resolve(response)
                    })

                    .catch(error => {
                        console.log(error)
                        console.log('error here')
                        reject(error)
                    })
            })
        }
    }
})

export default store