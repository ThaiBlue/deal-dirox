<template>
    <div class="option">
        <div class="create">
            
            <el-select v-model="value" placeholder="Choose Action" >
                <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                >
                </el-option>
            </el-select>
            <div class="button-apply">
                <button @click.prevent="show" class="apply">Apply</button>
                <modal name="modal-login" :height="690" :width="1028">
                    <Popup />
                </modal>
                <modal name="modal-select" :height="690" :width="1028">
                    <SelectFolder />
                </modal>
            </div>
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
import Popup from "./Popup"
import SelectFolder from "../components/SelectFolder"

export default {
    name: 'Option',
    components: {
        Popup,
        SelectFolder
    },
    data() {
        return {
            options: [
                {  
                    value: 'Create Transfer to Production',
                    label: 'Create Transfer to Production'
                }, 
                {
                    value: 'Create Contract',
                    label: 'Create Contract'
                }, 
                {
                    value: 'Create Proposal',
                    label: 'Create Proposal'
                }, 
                {
                    value: 'Create Transfer to BA',
                    label: 'Create Transfer to BA'
                }, 
                {
                    value: 'Create Folder',
                    label: 'Create Folder'
                },
            ],

            value: '',

            showModal: true
        }
    },
    methods: {
        async show() {
            await this.$store.dispatch('resetFolder');
            this.$store.dispatch('fetchFolder');
            this.$modal.show('modal-login');
        },

        hide() {
            this.$modal.hide('modal-login');
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


    .page{
        width: 300px;
    }


    .option{
        display: flex;
        justify-content: space-between;
    }


    .create{
        width:602px;
        height: 40px;
        display: flex;
        justify-content: space-between;
    }

    .el-select {
        width: 424px;
        height: 52px;
    }

    .apply {
        width: 148.5px;
        height: 40px;
        border-radius: 10px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        border: solid 1px #979797;
        background-color: #cacaca;
        cursor: pointer;
        outline: none;
    }

    .model-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 98;
        background-color: rgba(0, 0, 0, 0.3);
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 2s;
    }


    .fade-enter,
    .fade-leave-to {
        opacity: 0;
    }
</style>