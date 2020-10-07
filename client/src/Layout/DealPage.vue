<template>
    <div class="container">
        <div class="bar">
            <div class="filtertableimageoption">
                <div class="filterimagetable">
                    <div class="filterimage">
                        <FilterVue />
                        <img src="../assets/img/logo-with-shadow.png" alt="logo-dirox" width="85" height="161">
                    </div>
                    <Table />
                </div>
                <Option />
            </div>
        </div>
    </div>
</template>

<script>
import MenuBar from "../components/MenuBar"
import Table from "../components/Table"
import FilterVue from "../components/Filter"
import Option from "../components/Option"
import moment from 'moment'

export default {
    name: 'DealPage',
    components: {
        Table,
        FilterVue,
        Option
    },
    mounted() {
        window.setTimeout(() => { localStorage.removeItem('access_token'); localStorage.removeItem('expiration_time');  this.$router.push('/')}, 
        moment.utc(localStorage.expiration_time).diff(moment.utc()));
    },

}

</script>

<style>
    body {
        overflow-x: auto;
        width: 120vh;
        margin: 0 auto;
    }
</style>

<style scoped>
    img {
        float: right;
    }


    .filterimage{  /* Class with Filter and Image */
        width: 1168px;
        height: 112px;  
        display: flex;
        justify-content: space-between;
    }


    .filterimagetable{ /* Class with (Filter and Image) and Table  */
        display: flex;
        width: 1168px;
        height: 892px;
        flex-direction: column;
        justify-content: space-between;
    }


    .filtertableimageoption{ /* Class with (Filter and Image Table) and Option  */
        height: 962px;
        width: 1168px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }


    .bar{
        width: 1168px;
        /* margin: 0 auto; */
        display: flex;
        flex-direction: row-reverse;
        justify-content: space-between;
        align-items: center;
    }
</style>