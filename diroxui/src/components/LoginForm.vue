<template>
  <div class="body">
    <h1 class="login-to-deal-dirox">LOGIN TO DEAL@DIROX</h1>
    <form action="#" class="form-login" @submit.prevent="login">
        <div class="email-login">
            <label for="email">Email or Username</label>
            <input type="email" class="email-box" placeholder="Type your Email or Username here" v-model="username">
        </div>
        <div class="password-login">
            <label for="password">Password</label>
            <input type="password" class="password-box" placeholder="Type your password here" v-model.trim="password">
        </div>
        <!-- ^([a-z]+)[.]([a-z]+)@(dirox[.]net|synexser[.]com) -->
        <!-- <el-alert
            title="Email or Password is incorrect"
            type="error"
            center
            show-icon
            @close="error"
            :model=error
            >
        </el-alert> -->

        <!-- <el-alert
            title="success alert"
            type="success"
            show-icon>
        </el-alert> -->
    </form>
    <!-- <router-link to="/deal"><button type="submit" class="button">LOGIN</button></router-link> -->
    <button type="submit" class="button" @click.prevent="login()">LOGIN</button>

  </div>
</template>

<script>
export default {
    name: 'LoginForm',


    data: () => (
        {
            username: '',
            password: '',
            error: false
        }
    ) ,

    methods: {
        login () {
            // console.log(this.$store)
            this.$store.dispatch("retriveToken",{
                username: this.username,
                password: this.password
            })
                .then(response => {
                    console.log('Here ?')
                    // this.$router.push({name: 'deal'})
                    this.$router.push('/deal')
                })

                .catch(error => {
                    this.error = true
                    // console.log(error)
                    console.log('error here')
                    // reject(error)
                })
        },

        
    }

}
</script>

<style scoped>
    .login-to-deal-dirox {
        color: #FFFFFF;
        font-family: 'UTMAvoBold';
        font-size: 36px;
        line-height: 52.75px;
        text-align: center;
    }

    .email-login{
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 475px;
        height: 85px;
    }

    label{
        color: #FFFFFF;
        font-family: UTMAvoBold;
        font-size: 16px;
        line-height: 23px;
        text-align: left;
    }

    .email-box {
        background-color: #FFFFFF;
        border: 1px solid #979797;
        border-radius: 10px;
        box-shadow: 3px 4px 8px 0 rgba(0, 0, 0, 0.5), inset 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        width: 475px;
        height: 50px;
        padding-left: 10px;
    }

    .password-login {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 475px;
        height: 85px;
    }

    .password-box {
        background-color: #FFFFFF;
        border: 1px solid #979797;
        border-radius: 10px;
        box-shadow: 3px 4px 8px 0 rgba(0, 0, 0, 0.5), inset 0 2px 4px 0 rgba(0, 0, 0, 0.5);
        width: 475px;
        height: 50px;
        padding-left: 10px;
    }

    .button {
        color: #FFFFFF;
        font-family: UTMAvoBold;
        font-size: 18px;
        line-height: 26.38px;
        text-align: center;
        background-color: #FFCE7A;
        border: 1px solid #FEDEA5;
        border-radius: 11px;
        box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.5);
        width: 191px;
        height: 53px;
        outline: none;
        cursor: pointer;
    }

    .form-login {
        height: 192px;
        /* width: 475px; */
        /* border: 1px solid white; */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .body {
        display: flex;
        flex-direction: column;
        align-items: center;
        /* border: 1px solid black; */
        height: 425px;
        justify-content: space-between;
    }

</style>