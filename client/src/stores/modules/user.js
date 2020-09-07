import axios from 'axios'
import FormData from 'form-data'
// import { resolve, reject } from 'core-js/fn/promise'
axios.defaults.baseURL = 'https://api.deal.dirox.dev'

const store = [{
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
                        // console.log(error)
                        console.log('error here')
                        reject(error)
                    })
            })
        }
    }
}]

export default store

// eslint-disable-next-line no-unused-vars
// LOGIN: ({commit}, payload) => {
//     return new Promise((resole, reject) => {
//         axios.post('/accounts/user/login', payload)
            // .then(({data, status}) => {
            //     if (status === 200) {
            //         resolve(true)
            //     }
            // })

            // .catch(error => {
            //     reject(error)
            // })

        