<template>
    <div class="container">
        <router-link to="/"></router-link>
        <router-link to="/deal"></router-link>
        <router-view></router-view>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
        name: 'app',
    }
</script>

<style>
    body {
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
        height: 100vh;
        /* overflow: hidden; */
    }
</style>