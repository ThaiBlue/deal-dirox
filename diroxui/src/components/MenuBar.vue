<template>
    <div class="menubar">
        <div class="header">
            <img src="../assets/menu-icon.png" width="52" >
            <div class="options">
                <div class="home">
                    <img src="../assets/home-icon.png" width="52">
                    <label>Home</label>
                </div>

                <div class="sent">
                    <img src="../assets/sent-icon.png" width="46">
                    <label>Send Mail</label>    
                </div>

                <div class="user">
                    <img src="../assets/user-icon.png" width="52">
                    <label>Profile</label>
                </div>
            </div>
        </div>

        <div class="setting">
            <img src="../assets/setting-icon.png" width="56">
            <label class="setting-label">Setting</label>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MenuBar'
}
</script>

<style scoped>
    .menubar {
        background-color: #EEEEEE;
        border-radius: 0 25px 25px 0;
        box-shadow: 5px 4px 13px 0 rgba(0, 0, 0, 0.64);
        width: 239px;
        height: 834px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .setting {
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        margin-bottom: 23px;
    }

    label {
        color: #000000;
        font-family: UTM;
        font-size: 27px;
        line-height: 36.89px;
        text-align: left;
    }

    .home, .sent, .user {
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    .options {
        height: 234px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .header {
        height: 321px;
        margin-top: 37px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
</style>