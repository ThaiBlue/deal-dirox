import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"

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
    }
]
export default routes
