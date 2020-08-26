<template>
    <div class="container" :style="{backgroundColor: color}" id="wrapper">
        <div class="bar">
            <div class="filtertableimageoption">
                <div class="filterimagetable">
                    <div class="filterimage">
                        <FilterVue />
                        <img src="../assets/logo-dirox.png" alt="logo-dirox" width="119" height="112">
                    </div>
                    <Table />
                </div>
                <Option />
            </div>
            <MenuBar />
        </div>
    </div>
</template>

<script>
import MenuBar from "../components/MenuBar"
import Table from "../components/Table"
import FilterVue from "../components/Filter"
import Option from "../components/Option"
export default {
    name: 'DealPage',
    components: {
        MenuBar,
        Table,
        FilterVue,
        Option
    },
    data (){
        return {
            color: 'linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%)'
        }
    }
}

</script>

<style>
    body {
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
    }
</style>
<style scoped>
    
    
    .container{
        /* height: 1024px; */
        background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
        /* align-items: center; */
        margin: 0 auto;
        /* max-width: 1024px; */
        /* margin-left: auto;
        margin-right: auto; */
        /* max-width: 1880px; */
        width: 1440px;
    }

    img {
        float: right;
        margin-right: 32px;
    }


    .filterimage{  /* Class with Filter and Image */
        width: 1168px;
        height: 112px;  
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    .filterimagetable{ /* Class with (Filter and Image) and Table  */
        /* border: 1px solid black; */
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
        width: 1428px;
        display: flex;
        flex-direction: row-reverse;
        justify-content: space-between;
        align-items: center;
    }
</style>