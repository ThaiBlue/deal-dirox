import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
import popup from "./components/Popup"
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

    {
        path: '/test',
        name: 'pop-up',
        component: popup
    },

    // {
    //     path: '/popup',
    //     component: test
    // }
]


export default routes
