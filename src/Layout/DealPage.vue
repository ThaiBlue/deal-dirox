<template>
    <div class="container">
        <!-- <MenuBar /> -->
        <img src="../assets/logo-dirox.png" alt="logo-dirox" width="119">
        <Table />
    </div>
</template>

<script>
// import MenuBar from "../components/MenuBar"
import Table from "../components/Table"
export default {
    name: 'DealPage',
    components: {
        // MenuBar,
        Table,
    },
}

</script>

<style scoped>
    .container{
        height: 1024px;
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
    }

    img {
        float: right;
    }
</style>