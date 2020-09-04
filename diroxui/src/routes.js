import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
import store from "./stores/stores"


// Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'home',
        component: LoginScreen
    },

    {
        path: '/deal',
        name: 'deal',
        component: DealPage,
        meta: {
            requiresAuth: true
        }
    }
]

// routes.beforeEach((to, from, next) => {
//     console.log(to)
//     next()
// })

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