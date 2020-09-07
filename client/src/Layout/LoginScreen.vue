<template>
    <div class="container">
        <div class="form-logo">
            <img class="logo-dirox-new-white" src="../assets/img/logo-dirox.png" >
            <LoginForm />
        </div>
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
        /* width: 1439px; */

    }

    .logo-dirox-new-white {
        width: 203px;
        height: 152px;
        /* border: 1px solid black */

    }

    .form-logo{
        display: flex;
        width: 1100px;
        justify-content: space-between;
        /* justify-content: cen; */
        /* border: 1px solid white;
        width: 960px;
        display: flex;
        justify-content: space-between; */
    }


</style>