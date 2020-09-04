<template>
    <div class="container">
        <div class="logo">
            <img class="logo-dirox-new-white" src="../assets/logo-dirox.png" >
            <img class="main-logo" src="../assets/logo-main.png" alt="logo-main" width="202">
        </div>
        <LoginForm />
    </div>
</template>

<script>
import LoginForm from "../components/LoginForm"
export default {
    name: 'LoginScreen',
    components:{
        LoginForm
    }
}
</script>

<style scoped>
    .container{
        height: 1024px;
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);

    }
    .logo {
        /* border: 1px solid white; */
        margin-top: 56px;
        width: 680px;
        display: flex;
        justify-content: space-between;
    }
    .logo-dirox-new-white {
        width: 203px;
        height: 152px;
        /* margin-left: 25px;
        margin-top: 29px */
    }

    .main-logo{
        /* margin-top: 56px; */
    }
</style>