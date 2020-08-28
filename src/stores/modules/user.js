import axios from 'axios'


export default{
    state: {},
    getters: {},
    mutations: {},
    actions: {
        retriveToken(context, credentials) {
            axios.post('/deal', {
                username: credentials.username,
                password: credentials.password
            })
                .then(response => {
                    console.log(response)
                })

                .catch(error => {
                    console.log(error)
                })
        }
    }
}