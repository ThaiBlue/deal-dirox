<template>
    <div class="component">
        <div class="search-box">
            <input type="text" class="search" placeholder="Search...">
            <button type="submit"><img src="../assets/icon-search.png" alt="search-icon" width="42" height="42"></button>
        </div>
        <el-dropdown :hide-on-click="false">
            <div class="filter">
                <label>Filter</label>
                <img src="../assets/icon-filter.png" alt="filter-icon" width="33">
            </div>
            <el-dropdown-menu>
                <div class="item">
                    <el-dropdown-item ><label>Project Name</label><input type="text"></el-dropdown-item>
                    <el-dropdown-item ><label>Start Date</label><input type="text"></el-dropdown-item>
                    <el-dropdown-item ><label>End Date</label><input type="text"></el-dropdown-item>
                    <el-dropdown-item ><label>Deal Owner</label><input type="text"></el-dropdown-item>
                    <el-dropdown-item ><label>Company</label><input type="text"></el-dropdown-item>
                </div>
                <div class="button">
                    <el-dropdown-item><button style="background-color: #ED8383">Clear All</button></el-dropdown-item>
                    <el-dropdown-item><button style="background-color: #8ED99E">Appy</button></el-dropdown-item>
                </div>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<script>
export default {
    name: 'FilterVue'
}
</script>

<style>
    .el-dropdown-menu__item{
        display: flex;
        flex-direction: column;
        width: 227px;
        height: 77px;
        justify-content: space-between;
    }
    
    .el-dropdown-menu__item input{
        background-color: #F1F1F1;
        border: 1px solid #979797;
        border-radius: 5px;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        width: 227px;
        height: 45px;
        outline: none;
        padding-left: 10px;
    }

    .el-dropdown-menu__item label{
        color: #000000;
        font-family: UTM;
        font-size: 16px;
        line-height: 21.86px;
        width: 124px;
        text-align: left;
    }

    .el-dropdown-menu__item button{
        border-radius: 10px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        width: 161px;
        height: 43px;
        outline: none;
        cursor: pointer;
    }

</style>

<style scoped>
    .component {
        width: 667px;
        display: flex;
        justify-content: space-between;
    }
    div.search-box button{
        background-color:transparent;
        border: none;
        cursor: pointer;
        overflow: hidden;
    }


    .search-box {
        display: flex;
        width: 486px;
        height: 59px;
        justify-content: space-around;
        background-color: #FFFFFF;
        border: 1px solid #E6E6E6;
        border-radius: 29.5px;
        box-shadow: 3px 4px 6px 0 rgba(0, 0, 0, 0.5);
    }
    .search {
        border: hidden;
        width: 348px;
        outline: none;
    }

    ::-webkit-input-placeholder { /* Chrome/Opera/Safari */
        color: #B4B4B4;
        font-family: UTMAvo;
        font-size: 21px;
        line-height: 28.69px;
    }
    ::-moz-placeholder { /* Firefox 19+ */
        color: #B4B4B4;
        font-family: UTMAvo;
        font-size: 21px;
        line-height: 28.69px;
    }


    .filter{    
        background-color: #FFFFFF;
        border: 1px solid #E6E6E6;
        border-radius: 29.5px;
        box-shadow: 3px 4px 6px 0 rgba(0, 0, 0, 0.5);
        width: 133px;
        height: 59px;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
        cursor: pointer;

    }

    .label {
        color: #000000;
        font-family: UTM;
        font-size: 24px;
        line-height: 32px;
        text-align: center;
    }

    .el-dropdown-menu {
        width: 964px;
        height: 270px;
        margin-left: 500px;
        /* margin: 0 auto; */
        background-color: #FFFFFF;
        border: 5px solid #E8E8E8;
        border-radius: 30px;
        box-shadow: 0 3px 10px 0 rgba(0, 0, 0, 0.5);
        /* align-items: center; */
        border: 1px solid black
    }

    .item {
        display: flex;
        flex-wrap: wrap;
    }

    .button {
        display: flex;
        flex-direction: row;
        float: right;
        margin-top: 20px
    }

</style>