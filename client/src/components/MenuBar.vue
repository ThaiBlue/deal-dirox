<template>
    <div class="setting">
        <img @click.prevent="show" src="../assets/img/setting-icon.png" width="56">
        <modal name = "modal-setting" :width="741" :height="741">
            <Settings />
        </modal>

    </div>
</template>

<script>
import Settings from "./Settings"
export default {
    name: 'MenuBar',
    components: {
        Settings
    },
    methods: {
        show () {
            this.$modal.show('modal-setting')
        }
    }
}
</script>

<style>
    .vm--container .vm--modal{
        border-radius: 42px;
    }
</style>

<style scoped>
    .setting {
        cursor: pointer;
        /* margin-top: 64%; */
    }
</style>