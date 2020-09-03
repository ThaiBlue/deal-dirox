import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router'
import routes from "./routes"
import uielement from "./uielement"
import store from "./stores/stores"
import Vuelidate from 'vuelidate'


Vue.config.productionTip = false
Vue.use(Vuelidate)
Vue.use(VueRouter)





const router = new VueRouter({
    routes,
    mode: 'history'
})


new Vue({
    router: router, 
    uielement,
    store,
    render: h => h(App),
}).$mount('#app')
