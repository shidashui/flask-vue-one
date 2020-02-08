<template>
    <div class="container">
      <h1>Register</h1>
      <div class="row">
        <div class="col-md-4">
          <form @submit.prevent="onSubmit">
            <div class="form-group" v-bind:class="{'u-has-error-v1': registerForm.usernameError}" >
              <label for="username">Username</label>
              <input type="text" v-model="registerForm.username" class="form-control" id="username" placeholder="">
              <small class="form-control-feedback" v-show="registerForm.usernameError">{{ registerForm.usernameError }}</small>
            </div>

            <div class="form-group" v-bind:class="{'u-has-error-v1': registerForm.emailError}" >
              <label for="email">Email address</label>
              <input type="email" v-model="registerForm.email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="">
              <small v-if="!registerForm.emailError" id="emailHelp" class="form-text text-muted">
                We'll never share your email with anyone else.
              </small>
              <small class="form-control-feedback" v-show="registerForm.emailError">{{ registerForm.emailError }}</small>
            </div>

            <div class="form-group"  v-bind:class="{'u-has-error-v1': registerForm.passwordError}" >
              <label for="password">Password</label>
              <input type="password" v-model="registerForm.password" class="form-control" id="password" placeholder="">
              <small class="form-control-feedback" v-show="registerForm.passwordError">{{ registerForm.passwordError }}</small>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </div>
</template>

<script>
    export default {
        name: "register",
      data(){
          return{
            registerForm:{
              username:'',
              email:'',
              password:'',
              submitted:false,  //是否点击了submit按钮
              errors:0,         //表单是否在前端通过，0表示没有错误，验证通过
              usernameError:null,
              emailError:null,
              passwordError:null
            }
          }
      },
      methods:{
          onSubmit(e){
            this.registerForm.submitted = true    //先更新状态
            this.registerForm.errors = 0

            if (!this.registerForm.username) {
              this.registerForm.errors++
              this.registerForm.usernameError = 'Username required.'
            } else {
              this.registerForm.usernameError = null
            }

            if (!this.registerForm.email) {
              this.registerForm.errors++
              this.registerForm.emailError = 'Email required.'
            } else if (!this.validEmail(this.registerForm.email)){
              this.registerForm.errors++
              this.registerForm.emailError = 'Valid email required.'
            } else {
              this.registerForm.emailError = null
            }

            if (!this.registerForm.password){
              this.registerForm.errors++
              this.registerForm.passwordError = 'Password required.'
            } else {
              this.registerForm.passwordError = null
            }

            if (this.registerForm.errors > 0){
              //表单验证没有通过，不继续往下执行，即不会通过axios调用后端api
              return false
            }

            const path = '/api/users'
            const payload = {
              confirm_email_base_url: window.location.href.split('/', 4).join('/') + '/unconfirmed/?token=',
              username: this.registerForm.username,
              email: this.registerForm.email,
              password: this.registerForm.password
            }
            this.$axios.post(path,payload)
              .then((response) =>{
                this.$toasted.success('A confirmation email has been sent to you by email.', { icon: 'fingerprint' })
                //成功后跳转到login页面
                this.$router.push('/login')
              })
              .catch((error) => {
                for (var field in error.response.data.message) {
                  if (field == 'username'){
                    this.registerForm.usernameError = error.response.data.message.username
                  } else if(field == 'email'){
                    this.registerForm.emailError = error.response.data.message.email
                  } else if(field == 'password') {
                    this.registerForm.passwordError = error.response.data.message.password
                  }
                }
              })
          },

        validEmail: function (email) {
          var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(email);
        }
      }
    }
</script>

<style scoped>

</style>
