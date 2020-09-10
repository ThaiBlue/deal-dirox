<template>
    <div class="container" id="wrapper">
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
    }

}

</script>


<style scoped>
    
    
    .container{
        //background-image: linear-gradient(180deg, #1686D3 0%, #0E3B5F 100%);
        margin: 0 auto;
        width: 1440px;
    }


    img {
        //float: right;
        //margin-right: 32px;
        //margin-top: 50px;
        position: absolute;
        right: 30px;
        top: 30px
    }


    .filterimage{  /* Class with Filter and Image */
        width: 1168px;
        height: 112px;  
        display: flex;
        justify-content: space-between;
        align-items: center;
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
        width: 1428px;
        display: flex;
        flex-direction: row-reverse;
        justify-content: space-between;
        align-items: center;
    }
</style>