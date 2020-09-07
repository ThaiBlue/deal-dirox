<template>
    <div class="option">
        <div class="create">
            <button type="submit" v-bind:class="clicked ? 'click' : 'noclick'" v-on:click ="clicked = !clicked">Create InitLead</button>
            <button type="submit" v-bind:class="click ? 'click' : 'noclick'" v-on:click ="click = !click">Create Proposal</button>
            <button type="submit" v-bind:class="changed ? 'click' : 'noclick'" v-on:click ="changed = !changed">Create Contract</button>
        </div>

        <div class="page">
            <el-pagination
                :page-size="2"
                :pager-count="5"
                layout="prev, pager, next"
                :total="10">
            </el-pagination>
        </div>        
    </div>
</template>
<script>
export default {
    name: 'Option',
    data: function (){
        return {
            clicked: false,
            click: false,
            changed: false
        }
    }
}
</script>

<style>
    .option .el-pagination .btn-prev{
        background-color:transparent;
        width: 21px;
        height: 45px;
        color: #FFFFFF;
        /* font-size: 42px; */
    }
    .option .el-pagination .btn-prev i{
        font-size: 42px;
    }

    .option .el-pagination .el-pager li {
        margin-top: 5px;
        background-color: transparent;
        width: 40px;
        height: 45px;
        font-size: 25px;
        /* color: #FFFFFF */
    }

    .option .el-pagination .btn-next{
        background-color: transparent;
        width: 21px;
        height: 45px;
        color: #FFFFFF;
    }

    .option .el-pagination .btn-next i{
        font-size: 42px;
    }

    
</style>

<style scoped>
    .white {
       background-color: white;
       width: 200px;
       height: 200px;  

    }
    .blue {
        width: 200px;
        height: 200px;
        background-color: blue;

    }
    
    /* .create button{
        background-color: #A9A9A9;
        border: 2px solid #FFFFFF;
        border-radius: 13px;
        box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.5);
        width: 239px;
        height: 50px;
        outline: none;
        cursor: pointer;
    } */

    .noclick{
        background-color: #A9A9A9;
        border: 2px solid #FFFFFF;
        border-radius: 13px;
        box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.5);
        width: 239px;
        height: 50px;
        outline: none;
        cursor: pointer;
    }

    .click {
        background-color: #FFCE7A;
        border: 2px solid #FFFFFF;
        border-radius: 13px;
        box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.5);
        width: 239px;
        height: 50px;
        outline: none;
        cursor: pointer;
    }

    .create{
        display: flex;
        /* border: 1px solid black; */
        width: 760px;
        justify-content: space-between;
    }

    .page{
        /* border: 1px solid black; */
        width: 300px;
    }

    .option{
        display: flex;
        justify-content: space-between;
    }

</style>