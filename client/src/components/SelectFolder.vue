<template>
    <div class="create-folder">
        <div class="header">
            <label class="title">SELECT FOLDER</label>
        </div>
        <div class="body-popup">
            <div class="left">
                <el-tree :data="data" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
            </div>
            <div class="right">
                <div class="name-folder"></div>
                <div class="folder"></div>
                <div class="folder-name">
                    <div class="search-folder">
                        <label class="search">Folder name:</label>
                        <input type="text" placeholder="Folder name" class="input-folder">
                    </div>

                    <div class="button-folder">
                        <!-- <button class="create" type="submit" v-on:click="">Create</button> -->
                        <button class="cancel" type="submit">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    // name: 'Popup',
    data() {
        return {
            data: [{label: 'Drive', children:this.$store.state.folder}],
            defaultProps: {
                children: 'children',
                label: 'label'
            }
        };
    },
    methods: {
        handleNodeClick(data) {
            this.$store.dispatch('assignCurrentFolderID', data.id);
        }
    }
}
</script>

<style scoped>
    .create-folder{
        width: 1028px;
        height: 690px;
        border-radius: 10px;
        border: solid 1px #979797;
        background-color: #ffffff;
    }


    .header {
        height: 49px;
        border-bottom: 1px solid black;
        text-align: center;
        margin-top: 8px;
    }

    
    .body-popup {
        height: 639px;
        display: flex;
    }

    
    .left{
        height: 630px;
        width: 273px;
    }

    .title {
        width: 184px;
        height: 32px;
        font-family: UTM-Avo;
        font-size: 24px;
        font-weight: normal;
        font-stretch: normal;
        font-style: normal;
        line-height: normal;
        letter-spacing: normal;
        color: #141414;
    }

    .right {
        height: 630px;
        border: 1px solid red;
        width: 753px;
    }


    .name-folder{
        height: 56px;
        border: 1px solid black;
    }


    .folder {
        height: 485px;
        border: 1px solid blue;
    }


    .folder-name {
        height: 80px;
        display: flex;
        justify-content: space-around;
    }


    .search-folder {
        width: 424px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
    }


    .search {
        font-family: UTM-Avo;
        font-size: 17.5px;
        font-weight: normal;
        font-stretch: normal;
        font-style: normal;
        line-height: normal;
        letter-spacing: normal;
        color: #0b0b0b;
    }


    .input-folder {
        width: 424px;
        height: 37px;
        border-radius: 8px;
        border: solid 1px #979797;
        padding-left: 10px;
        outline: none;
    }


    .button-folder {
        width: 263px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    

    .create {
        width: 124px;
        height: 45px;
        border-radius: 10px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        border: solid 1px #add2b5;
        background-color: #8ed99e;
        cursor: pointer;
        outline: none;
    }


    .cancel {
        width: 124px;
        height: 45px;
        border-radius: 10px;
        border: solid 1px #979797;
        background-color: #979797; 
        cursor: pointer;
        outline: none;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
    }
</style>