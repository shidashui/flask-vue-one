<template>
    <div class="container">
      <alert
        v-if="shareState.is_new"
        v-bind:variant="alertVariant"
        v-bind:message="alertMessage">
      </alert>
      <h1>Sign In</h1>
      <div class="row">
        <div class="col-md-4">
          <form @submit.prevent="onSubmit">
            <div class="form-group">
              <label for="username">Username</label>
              <input type="text" v-model="loginForm.username" class="form-control"
                     v-bind:class="{'is-invalid': loginForm.usernameError}" id="username" placeholder="">
              <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.usernameError }}</div>
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" v-model="loginForm.password" class="form-control"
                     v-bind:class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="">
              <div v-show="loginForm.passwordError" class="invalid-feedback">{{loginForm.passwordError}}</div>
            </div>
            <button type="submit" class="btn btn-primary">Sign In</button>
          </form>
        </div>
      </div>

      <br>
      <p>New User? <router-link to="/register">Click to Register!</router-link> </p>
      <p>
        Forgot Your Password?
        <a href="#">Click to Reset It</a>
      </p>
    </div>
</template>

<script>
  import axios from 'axios'
  import Alert from './Alert'
  import store from '../store'

    export default {
        name: "Login",
      components: {Alert},
      data(){
          return{
            shareState: store.state,
            alertVariant: 'info',
            alertMessage: 'Congratulations, you are now a registered user !',
            loginForm:{
              username:'',
              password:'',
              submitted:false,    //是否点击了submit
              errors:0,
              usernameError: null,
              passwordError: null
            }
          }
      },
      methods:{
          onSubmit(e){
            // console.log('teststsetwetstset')
            this.loginForm.submitted = true   //更新状态
            this.loginForm.errors = 0

            if (!this.loginForm.username){
              this.loginForm.errors++
              this.loginForm.usernameError = 'Username required.'
            } else {
              this.loginForm.usernameError = null
            }

            if (!this.loginForm.password) {
              this.loginForm.errors++
              this.loginForm.passwordError = 'Password required'
            } else {
              this.loginForm.passwordError = null
            }

            if (this.loginForm.errors > 0) {
              return false
            }

            const path = 'http://localhost:5000/api/tokens'
            //axios 实现Basic Auth需要再config中设置auth这个属性即可
            axios.post(path, {},{
              auth:{
                'username':this.loginForm.username,
                'password':this.loginForm.password
              }
            }).then((response) => {
              window.localStorage.setItem('codershui-token', response.data.token)
              store.resetNotNewAction()
              store.loginAction()

              if (typeof this.$route.query.redirect == 'undefined') {
                this.$router.push('/')
              } else {
                this.$router.push(this.$route.query.redirect)
              }
            })
              .catch((error)=>{
                //发生错误
                if (error.response.status == 401){
                  this.loginForm.usernameError = 'Invalid username or password.'
                  this.loginForm.passwordError = 'Invalid username or password.'
                } else {
                  console.log('报错')
                  console.log(error.response)
                }
              })
          }
      }
    }
</script>

<style scoped>

</style>
