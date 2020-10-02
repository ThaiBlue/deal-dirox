import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
import test from "./components/Settings"

const routes = [
    {
        path: '/',
        name: 'home',
        component: LoginScreen,
        meta: {title: 'DEAL@DIROX'}
    },

    {
        path: '/deal',
        name: 'deal',
        component: DealPage,
        meta: {title: 'DEAL'}
        // meta: {
        //     requiresAuth: true
        // }
    },

    {
        path: '/test',
        component:test
    }
]
export default routes
