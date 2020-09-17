<template>
  <div class="container">
        <router-link to="/"></router-link>
        <router-link to="/deal"></router-link>
        <router-link to="/dmeohieusaonokhongchayduoc"></router-link>
        <!-- <router-link to="/popup"></router-link> -->
        <router-link to="/setting"></router-link>
    <router-view></router-view>
  </div> 
</template>

<script>
export default {
    name: 'app',
    components: {
    
    },
    computed: {
        // loggedIn() {
        //     return this.$store.getters.loggedIn
        // }
    }
}


</script>

<style>
    body{
        height: 100vh;
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
    }
</style>


