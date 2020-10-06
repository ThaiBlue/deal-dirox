import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router'
import routes from "./routes"
import uielement from "./uielement"
import { store } from "./stores/stores"
import Vuelidate from 'vuelidate'
import VModal from 'vue-js-modal'
import axios from 'axios'
import moment from 'moment'

Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(VueRouter)
Vue.use(VModal)

const router = new VueRouter({
    routes,
    mode: 'history'
})

var navigated = false

router.beforeEach((to, from, next) => {
    if(!navigated) {
        navigated = true
        if (localStorage.credential !== undefined) {
            if(moment.utc(localStorage.credential.expiration_time)<moment().utc()) {
                next('/');
            } else {
                next('/deal');
            }
        } else {
            next('/');
        }
    } else {
        next()
    }
})

new Vue({
    router: router,
    uielement,
    store: store,
    render: h => h(App),
}).$mount('#app')