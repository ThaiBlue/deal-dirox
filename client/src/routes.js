import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
import SubFolder from "./components/SubFolder"

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
        path: '/sub',
        component: SubFolder
    }

]
export default routes
