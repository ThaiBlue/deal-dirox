<template>
  <div class="container">
      <router-link to="/"></router-link>
      <router-link to="/deal"></router-link>
      <!-- <router-link to="/logout"></router-link> -->
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
    body {
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
    }
</style>


