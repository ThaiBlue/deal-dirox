import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
import Success from "./components/SuccessPopUp"
import Settings from "./components/Settings"
import test from "./components/test"

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
        component: test
    },

    {
        path: '/hello',
        component: Success
    }
]
export default routes
