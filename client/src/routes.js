import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
// import popup from "./components/PopupSelectFolder"
// import test from "./components/test"

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
        // meta: {
        //     requiresAuth: true
        // }
    },

    // {
        
    //     path: '/popup',
    //     name: 'pop-up',
    //     component: popup
    // },

    // {
    //     path: '/dmeohieusaonokhongchayduoc',
    //     component: test
    // }
]


export default routes
