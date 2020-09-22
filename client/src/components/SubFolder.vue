<template>
    <div class="create-sub-folder">
        <div class="header">
            <label for="">Create Sub Folder</label>
            <img src="../assets/img/close.svg" width="19" class="close">
        </div>
        <div class="main">
            <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" 
                @change="handleCheckAllChange" class="check-all">
                    Check all
            </el-checkbox>
            <div style="margin: 15px 0;"></div>
            <el-checkbox-group v-model="checkedFolder" 
                @change="handlecheckedFolderChange" class="sub-folder">
                <el-checkbox v-for="folder in folders" :label="folder"
                    :key="folder">
                        {{folder}}
                </el-checkbox>
            </el-checkbox-group>
        </div>
        <div class="footer">
            <el-button class="create" type="success" v-on:click="onclickCreate()">Create Sub Folder</el-button>
            <el-button class="skip" type="info" v-on:click="onclickSkip()">Skip</el-button>
        </div>
    </div>
</template>

<script>
    const folderOption = ['00. Customer documents', '01. Proposal', '02. Contract'];
    export default {
        data() {
            return {
                checkAll: false,
                checkedFolder: ['00. Customer documents', '01. Proposal', '02. Contract'],
                folders: folderOption,
                isIndeterminate: true
            };
        },

        methods: {
            handleCheckAllChange(val) {
                this.checkedFolder = val ? folderOption : [];
                this.isIndeterminate = false;
            },

            handlecheckedFolderChange(value) {
                let checkedCount = value.length;
                this.checkAll = checkedCount === this.folders.length;
                this.isIndeterminate = checkedCount > 0 && checkedCount < this.folders.length;
            },
            onclickCreate() {
                this.$store.dispatch('createFolder', {name: this.$store.state.newFolderName, parentID: [this.$store.state.currentFolderId], subFolder: this.checkedFolder});
            },
            onclickSkip() {
                this.$store.dispatch('createFolder', {name: this.$store.state.newFolderName, parentID: [this.$store.state.currentFolderId], subFolder: []});
            }
        }
    };
</script>

<style>
    .el-checkbox__label{
        /* font-family: ABeeZee;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 21px;
        text-align: left;
        color: #000000; */
    }


</style>

<style scoped>
    .create-sub-folder {
        width: 496px;
        height: 462px;
        border: 1px solid #979797;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: space-around;
        box-sizing: border-box;
        background: #FFFFFF;
    }

    .header {
        width: 496px;
        text-align: center;
    }

    .close {
        float: right;
        /* margin-right: 20px; */
    }

    label {
        font-family: ABeeZee;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 21px;
        text-align: left;

        color: #000000;
    }

    .main {
        display: flex;
        flex-direction: column;
        border: 1px solid #979797;
        width: 496px;
        align-items: center;
        height: 317px;
        font-family: ABeeZee;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 21px;
        text-align: left;
        color: #000000;
    }

    .sub-folder {
        height: 129px;
        width: 257px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }

</style>