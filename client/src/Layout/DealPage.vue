<template>
    <el-row>
        <el-col :md="3" :lg="2" :xl="0">
            <!-- <span>left</span> -->
        </el-col>

        <el-col :md="18" :lg="20" :xl="24">
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
        </el-col>

        <el-col :md="3" :lg="2" :xl="0">
            <!-- <span>right</span> -->
        </el-col>
    </el-row>
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
    }
}

</script>

<style>
    body {
        /* overflow-x: auto; */
        /* width: 1440px; */
        width: 100%;
        margin: 0 auto;
    }
    
    .el-row {
        display: flex;
        justify-content: space-between;
        flex-direction: row;
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
        margin: 0 auto;
        display: flex;
        flex-direction: row-reverse;
        justify-content: space-between;
        align-items: center;
        /* border: 1px solid red; */
        margin-top: 10px;
        /* display: block; */
        /* margin-left: auto; */
        /* margin-right: auto; */
    }
</style>