import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"

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
    }
]
export default routes
