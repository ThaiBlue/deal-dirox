<template>
    <div class="popup" @exit="hide1">
        <img class="close" src="../assets/img/close_pop_up_icon.svg" @click="hide" >
        <div class="main">
            <img src="../assets/img/checked.svg" alt="">
            <label>Folders created successfully!</label>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            opened: false
        }
    },
    methods: {
        hide() {
            // this.opened = false
            this.$modal.hide('sub-folder-create') 
            this.$modal.hide('modal-folder-create')
        },

        hide1() {
            console.log('Here ?')
            // this.opened = true
            this.$modal.hide('sub-folder-create') 
            this.$modal.hide('modal-folder-create')
        }
    },
}
</script>

<style scoped>
    .popup {
        width: 733px;
        height: 266px;
        background: #FFFFFF;
        border: 1px solid #D3D3D3;
        box-sizing: border-box;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5);
    }

    .close {
        float: right;
        margin: 13.25px;
        cursor: pointer;
    }

    .main {
        /* border: 1px solid black; */
        width: 297px;
        height: 266px;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        margin: 0 auto;
    }
</style>