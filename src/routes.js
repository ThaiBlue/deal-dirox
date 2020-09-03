// import Vue from 'vue';
// import VueRouter from 'vue-router';
import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"


// Vue.use(VueRouter)

const routes = [
    {path: '/', component: LoginScreen},
    {path: '/deal', component: DealPage}
]

export default routes
// export default new VueRouter({
//     mode: 'history',
//     base: process.env.BASE_URL,
//     routes:[
//         {
//             path: '/',
//             name: 'login',
//             component: LoginScreen,
//         },
        
//         {
//             path: '/deal',
//             name: 'deal',
//             component: DealPage,
//             meta: {
//                 requiresAuth: true
//             }
//         },

//     ]
// })