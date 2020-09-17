import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
// import popup from "./components/PopupSelectFolder"
<<<<<<< HEAD
import test from "./components/test"
import setting from "./components/Settings"

=======
// import test from "./components/test"
>>>>>>> 17cdfbf3befa2c484a06898ebc706f8276d153b8

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

<<<<<<< HEAD
    {
        path: '/dmeohieusaonokhongchayduoc',
        component: test
    },


    {
        path: '/setting',
        component: setting
    }
=======
    // {
    //     path: '/dmeohieusaonokhongchayduoc',
    //     component: test
    // }
>>>>>>> 17cdfbf3befa2c484a06898ebc706f8276d153b8
]


export default routes
