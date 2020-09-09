import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router'
import routes from "./routes"
import uielement from "./uielement"
import {store} from "./stores/stores"
import Vuelidate from 'vuelidate'
import VModal from 'vue-js-modal'


Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(VueRouter)
Vue.use(VModal)


const router = new VueRouter({
    routes,
    mode: 'history'
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        // const authUser = JSON.parse(window.localStorage.getItem('authUser'))
        next({name: 'home'})
        // if (authUser && authUser.access_token) {
        //     next()
        // } else {
        //     next({name: 'home'})
        // }
    }
    next()
})

new Vue({
    router: router, 
    uielement,
    store:store,
    render: h => h(App),
}).$mount('#app')
