<template>
    <el-table class="table" :data="tableData">
        <el-table-column prop="no" label="No." type="index" width="180">
        </el-table-column>
        <el-table-column prop="id" label="ID" width="120">
        </el-table-column>
        <el-table-column prop="projectname" label="Project Name" width="250">
        </el-table-column>
        <el-table-column prop="status" label="Status" width="120">
        </el-table-column>
        <el-table-column prop="startdate" label="Start Date" width="120">
        </el-table-column>
        <el-table-column prop="enddate" label="End Date" width="120">
        </el-table-column>
    </el-table>
</template>
<script>
    export default {
        name: 'Table',
        data() {
            return {
                tableData: []
            }
        },
        mounted() {
            const axios = require('axios');
            const moment = require('moment');
            //Fetch data from server 
            // moment(item.properties.start_date).format('DD/MM/YYYY')
            axios.get('https://api.deal.dirox.dev/hubspot/deals/makeoffer/all').then(response => {
                response.data.results.forEach(item => {
                    this.tableData.push(
                        {
                            id:item.id,
                            projectname: item.properties.dealname,
                            status: 'Make Offer',
                            startdate: moment(item.properties.start_date).format('DD/MM/YYYY'),
                            enddate: moment(item.properties.closedate).format('DD/MM/YYYY')
                        }
                    )
                });
            })
        },
    }
</script>
<style>
    .has-gutter tr th {
        background-color: rgba(255, 255, 255, 0.72);
    }

    .el-table__header {
        margin: 0 auto;
    }

    .el-table__body {
        margin: 0 auto;
    }
</style>
<style scoped>
    .el-table {
        background-color: #FFFFFF - 72%;
        border-radius: 25px;
        width: 1168px;
        max-height: 724px;
        overflow: scroll;
        -ms-overflow-style: none;
        /* IE and Edge */
        scrollbar-width: none;
        /* Firefox */
    }

    .el-table::-webkit-scrollbar {
        display: none;
    }
</style>
