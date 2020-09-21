<template>
    <div class="settings">
        
        <div class="top">
            <label class="setting-label">SETTING</label>
            <img class="close" src="../assets/img/close.svg">
        </div>

        <div class="middle">
            <div class="hubspot-account">
                <div class="hubspot">
                    <img src="../assets/img/hubspot-img.svg" alt="">
                    <div class="hubspot-label">
                        <label class="setting-label">HubSpot Account</label>
                        <div class="gmail">{{mail}}</div>
                    </div>
                </div>
                <el-button type="danger">Disconnect</el-button>

            </div>

            <div class="drive-account">
                <div class="drive">
                    <img src="../assets/img/drive.svg" alt="">
                    <div class="drive-label">
                        <label class="setting-label">Google Drive Account</label>
                        <div class="gmail">{{mail}}</div>
                    </div>
                </div>
                <el-button class="success" type="success">Connect</el-button>
            </div>
        </div>

        <div class="Feature">
        </div>

        <div class="button-setting">
            <el-button  class="cancel" type="info">Cancel</el-button>
            <el-button class="save" type="success">Save</el-button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            mail: 'tien.tran@dirox.net',
        }
    },
}
</script>


<style scoped>
    .settings {
        width: 741px;
        height: 741px;
        border: 1px solid #979797;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: space-around;
        box-sizing: border-box;
        background: #FFFFFF;
    }
    
    .top {
        width: 635px;
        text-align: center;
    }

    .close {
        float: right;
    }

    .setting-label {
        font-family: UTM;
        font-size: 30px;
        line-height: 35px;
        color: #000000;
    }


    .middle {
        height: 314px;
        width: 635px;
        border: 1px solid #979797;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        border-left: none;
        border-right: none;
    }



    .hubspot-account {
        background: #DAF5FF;
        border: 1px solid #A1DCF2;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 30px;
        width: 635px;
        height: 100px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    
    .drive-account{
        background: #DAF5FF;
        border: 1px solid #A1DCF2;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 30px;
        width: 635px;
        height: 100px;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    .hubspot {
        width: 341px;
        height: 85px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .drive {
        width: 415px;
        height: 85px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .hubspot-label {
        display: flex;
        flex-direction: column;
    }

    .drive-label {
        display: flex;
        flex-direction: column;
    }

    .gmail {
        background: #FFFFFF;
        border: 1px solid #979797;
        box-sizing: border-box;
        border-radius: 12px;
        width: 202px;
        height: 26px;
        display: flex;
        justify-content: space-around;
    }



    .el-button {
        height: 40px;
        width: 130px;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 17px;
    }

    .success {        
        height: 40px;
        width: 130px;
        border: 1px solid #A3E470;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 17px;
    }

    .Feature {
        width: 625px;
        height: 142px;
    }

    .cancel {
        width: 160px;
        border: 1px solid #DCDADA;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 17px;
        height: 49px;
    }

    .save {
        border: 1px solid #A3E470;
        box-sizing: border-box;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.5);
        border-radius: 17px;
        width: 160px;
        height: 49px;
    }


</style>