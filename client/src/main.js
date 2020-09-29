import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router'
import routes from "./routes"
import uielement from "./uielement"
import {
    store
} from "./stores/stores"
import Vuelidate from 'vuelidate'
import VModal from 'vue-js-modal'
import axios from 'axios'

Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(VueRouter)
Vue.use(VModal)

axios.defaults.baseURL = 'https://api.deal.dirox.dev'
// axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true

const router = new VueRouter({
    routes,
    mode: 'history'
})

var navigated = false;

router.beforeEach((to, from, next) => {
    if(!navigated) {
        axios.get('accounts/user/profile')
            .then(res => {
                navigated = true; // resolve navigate infinite looop
                store.state.isLoged = true; //cache login status
                store.state.profile = res.data;
                next('/deal');
            })
            .catch(err => {
                navigated = true;
                next('/');
            })
    } else {
        next();
    }
})

new Vue({
    router: router,
    uielement,
    store: store,
    render: h => h(App),
}).$mount('#app')