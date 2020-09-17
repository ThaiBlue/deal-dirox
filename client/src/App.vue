<template>
    <div class="container">
        <router-link to="/"></router-link>
        <router-link to="/deal"></router-link>
        <router-link to="/dmeohieusaonokhongchayduoc"></router-link>
        <!-- <router-link to="/popup"></router-link> -->
<<<<<<< HEAD
        <router-link to="/setting"></router-link>
    <router-view></router-view>
  </div> 
=======
        <router-view></router-view>
    </div>
>>>>>>> 17cdfbf3befa2c484a06898ebc706f8276d153b8
</template>
<script>
    import axios from 'axios'
    export default {
        name: 'app',
        components: {},
        computed: {
            // loggedIn() {
            //     return this.$store.getters.loggedIn
            // }
        },
    }
</script>
<style>
    body {
        height: 100vh;
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
    }
</style>