<template>
    <div class="logo-body-login">
        <img class="main-logo" src="../assets/img/logo-main.png" alt="logo-main" width="202">
        <div class="body-login">
            <h1 class="login-to-deal-dirox">LOGIN</h1>
            <form action="#" class="form-login" @submit.prevent="login">
                <div class="email-login">
                    <label for="email">Email or Username</label>
                    <input type="email" class="email-box" onkeypress="onkeypressEmailField(event)"
                        placeholder="Type your Email or Username here" v-model="username">
                </div>

                <div class="password-login">
                    <label for="password">Password</label>
                    <input type="password" class="password-box" onkeypress="onkeypressPasswordField()" placeholder="Type your password here"
                        v-model.trim="password">
                </div>
            </form>
            <button type="submit" class="button" @click.prevent="login()">LOGIN</button>
        </div>
    </div>
</template>

<script>
    export default {
        data: () => ({
            username: '',
            password: '',
            error: false
        }),

        methods: {
            login() {
                this.$store.dispatch('authenticate', {
                    username: this.username,
                    password: this.password
                })
                    .then(res => {
                        this.$router.push('/deal');
                })
                    .catch(err => {
                        console.log(err);
                })
            },
            onkeypressEmailField(event) {
                if (event.key === "Enter") {
                    console.log("dev me")
                }
            },
            onkeypressPasswordField() {
                console.log("dev me")
            }
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

    .email-login {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 475px;
        height: 85px;
    }

    label {
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
        outline: none;
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
        outline: none;
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
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .body-login {
        /* border: 1px solid black; */
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 400px;
        /* width: 500px; */
        align-items: center;
        justify-content: space-between;
    }

    .logo-body-login {
        margin-top: 56px;
        height: 710px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
</style>