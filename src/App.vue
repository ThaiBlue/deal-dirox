<template>
  <div class="container">
    <!-- <LoginScreen /> -->
    <DealPage />
  </div>  
</template>

<script>
// import LoginScreen from "./Layout/LoginScreen"
import DealPage from "./Layout/DealPage"
export default {
  name: 'app',
  components: {
    // LoginScreen,
    DealPage
  }
}
</script>

<style scoped>
  /* .container{
        height: 1024px;
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);

  } */
</style>
