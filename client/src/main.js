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
    if (!navigated) {
        navigated = true; //fix infinite loop cause
        axios.get('accounts/user/profile')
            .then(res => {
                store.state.profile = res.data;
                next('/deal');
            })
            .catch(err => {
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