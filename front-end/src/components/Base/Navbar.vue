<template>
  <section>
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px">
        <div class="navbar-brand">
          <router-link to="/" class="navbar-brand">
            <img src="../../assets/logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
            Copy by
          </router-link>
          <a href="http://localhost:8080" class="g-text-underline--none--hover">CoderShui</a>
        </div>

          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                  aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
              <li class="nav-item active">
                <router-link to="/" class="nav-link">Home <span class="sr-only">(current)</span> </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/ping" class="nav-link">Ping</router-link>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled" href="#">Explore</a>
              </li>
            </ul>

            <form  v-if="shareState.is_authenticated" class="form-inline navbar-left mr-auto">
              <input class="form-control mr-sm-2" type="search" placeholder="Search">
              <!--暂时先禁止提交，后续实现搜索再改回 type=“submit" -->
              <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
            </form>

            <ul v-if="shareState.is_authenticated" class="nav navbar-nav navbar-right">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <img v-bind:src="shareState.user_avatar"> {{shareState.user_name}}
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <router-link v-bind:to="{path: `/user/${shareState.user_id}`}" class="dropdown-item">Your profile</router-link>
                  <router-link v-bind:to="{name: 'SettingProfile'}" class="dropdown-item">Settings</router-link>
                  <div class="dropdown-divder"></div>
                  <a v-on:click="handlerLogout" class="dropdown-item" href="#" >Sign Out</a>
                </div>
              </li>
            </ul>


            <ul v-else class="nav navbar-nav navbar-right">
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Sign in</router-link>
              </li>
            </ul>
          </div>

      </nav>
    </div>
  </section>
</template>

<script>
  import store from '../../store'

    export default {
        name: "Navbar",
      data(){
          return {
            shareState: store.state
          }
      },
      methods:{
          handlerLogout(e){
            store.logoutAction()
            this.$toasted.show('You have been logged out.', { icon: 'fingerprint' })
            this.$router.push('/login')
          }
      }
    }
</script>

<style scoped>

</style>
