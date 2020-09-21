<template>
    <el-table class="table" :data="tableData" highlight-current-row border @current-change="handleCurrentChange"
        height="200">
        <el-table-column prop="no" label="No." type="index" width="60"></el-table-column>
        <el-table-column prop="id" label="ID" width="132"></el-table-column>
        <el-table-column prop="projectname" label="Project Name" width="204" show-overflow-tooltip></el-table-column>
        <el-table-column prop="stage" label="Stage" width="128"></el-table-column>
        <el-table-column prop="startdate" label="Start Date" width="136"></el-table-column>
        <el-table-column prop="enddate" label="End Date" width="136"></el-table-column>
        <el-table-column label="Folder" width="136" show-overflow-tooltip>
            <template slot-scope="scope">
                <el-button type="text" size="small" @click.native.prevent="currentFolderURL(scope.$index)">
                    {{currentFolderName(scope.$index)}} </el-button>
            </template>
        </el-table-column>
        <el-table-column prop="status" label="Status" width="154">
            <template slot-scope="scope">
                <el-select v-model="tableData[scope.$index].status" @change="onChangeStatus(scope.$index)" placeholder="Status">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
    </el-table>
</template>
<script>
    export default {
        name: 'Table',
        data() {
            return {
                tableData: this.$store.state.deals,
                options: [{
                    value: 'folder-created',
                    label: 'Folder Created'
                }, {
                    value: 'transfer-to-ba',
                    label: 'Transfered to BA'
                }, {
                    value: 'proposal-made',
                    label: 'Proposal made'
                }, {
                    value: 'contract-made',
                    label: 'Contract made'
                }, {
                    value: 'won',
                    label: 'Won'
                }]
            }
        },
        methods: {
            onChangeStatus(index) {
                this.$store.dispatch('updateCache', {
                        dealID: this.$store.state.deals[index].id,
                        folderID: this.$store.state.deals[index].folder.id,
                        status: this.$store.state.deals[index].status
                    })
            },
            currentFolderURL(index) {
                return window.open(this.tableData[index].folder.url, "_blank");
            },
            currentFolderName(index) {
                return this.tableData[index].folder.name
            },
            handleCurrentChange(val) {
                this.$store.dispatch('assignCurrentDeal', val);
            }
        },
        mounted() {
            if (this.$store.state.deals[0] === undefined && this.$store.state.isLoged) {
                this.$store.dispatch('fetchDeals');
            }
        }
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