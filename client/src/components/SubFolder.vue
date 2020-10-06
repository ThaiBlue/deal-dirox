<template>
    <div class="create-sub-folder">
        <div class="header">
            <label for="">Create Sub Folder</label>
            <img src="../assets/img/close.svg" v-on:click='onclickClose()' width="19" class="close">
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
            <el-button  class="create" type="success" @click="onclickCreate()">Create Sub Folder</el-button>
            <el-button  class="skip" type="info" @click="onclickSkip()">Skip</el-button>
            <modal name = 'success' :width="733" :height="266">
                <Success />
            </modal>
        </div>
    </div>
</template>

<script>
    import Success from "./SuccessPopUp"
    const folderOption = ['00. Customer documents', '01. Proposal', '02. Contract'];
    export default {
        components: {
            Success
        },
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
                // this.$modal.hide('sub-folder-create');
                this.$modal.show('success');
                this.$store.dispatch('createFolder', {name: this.$store.state.newFolderName, parentID: [this.$store.state.currentFolderId], subFolder: this.checkedFolder});
            },

            onclickSkip() {
                // this.$modal.hide('sub-folder-create');
                this.$modal.show('success');
                this.$store.dispatch('createFolder', {name: this.$store.state.newFolderName, parentID: [this.$store.state.currentFolderId], subFolder: []});
            },

            onclickClose() {
                this.$modal.hide('sub-folder-create');
            }
        }
    };
</script>

<style>
    .el-checkbox .el-checkbox__label{
        font-family: ABeeZee;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 21px;
        text-align: left;
        color: #000000;
    }

</style>

<style scoped>
    label {
        font-family: ABeeZee;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 21px;
        text-align: left;
        color: #000000;
    }

    .create-sub-folder {
        width: 496px;
        height: 462px;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: space-around;
        box-sizing: border-box;
        background: #FFFFFF;
        border-radius: 15px;
    }

    .header {
        width: 496px;
        text-align: center;
    }

    .close {
        float: right;
        cursor: pointer;
        margin-right: 20px;
    }


    .main {
        display: flex;
        flex-direction: column;
        border: 1px solid #979797;
        border-left: none;
        border-right: none;
        width: 496px;
        align-items: center;
        height: 317px;
    }
    .check-all {
        margin-top: 22px;
    }

    .sub-folder {
        height: 129px;
        width: 257px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }

    .skip {
        width: 155px;
    }

    .footer {
        margin-bottom: 10px;
        width: 496px;
        display: flex;
        justify-content: space-around;
    }

</style>