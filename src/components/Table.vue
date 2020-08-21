<template>
    <div class="main">
        <el-table
            :data="tableData"
            style="background-color:red">

            <el-table-column
                prop="date"
                label="Date"
                width="180"
                style="">
            </el-table-column>

            <el-table-column
                prop="name"
                label="Name"
                width="180">
            </el-table-column>

            <el-table-column
                prop="address"
                label="Address">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    name: 'Table',
}
</script>

<style scoped>
</style>

        <!-- <el-table>
                <el-table-column
                    label="No."
                    width="66">
                </el-table-column>

                <el-table-column
                    label="ID"
                    width="120">
                </el-table-column>

                <el-table-column
                    label="Project Name"
                    width="250">
                </el-table-column>

                <el-table-column
                    label="Status"
                    width = "120">
                </el-table-column>

                <el-table-column
                    label="Start Date"
                    width = "120">
                </el-table-column>

                <el-table-column
                    label="End Date"
                    width = "120">
                </el-table-column>
        </el-table> -->