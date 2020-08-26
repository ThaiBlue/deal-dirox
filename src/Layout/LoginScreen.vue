<template>
    <div class="container">
        <div class="header">
            <img class="logo-dirox-new-white" src="../assets/img/logo-dirox.png">
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

    .logo-dirox-new-white {
        width: 203px;
        height: 152px;
        margin-left: 25px;
        margin-top: 29px
    }


</style>