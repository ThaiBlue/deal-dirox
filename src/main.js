import Vue from 'vue';
import App from './App.vue';
import router from "./router"
import uielement from "./uielement"
import store from "./stores/stores"
// import axios from 'axios'
import Vuelidate from 'vuelidate'

Vue.config.productionTip = false
Vue.use(Vuelidate)
// axios.defaults.baseURL = 'http://localhost:8080'

new Vue({
    router,
    uielement,
    store,
    render: h => h(App),
}).$mount('#app')
