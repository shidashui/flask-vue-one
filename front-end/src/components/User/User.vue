<template>
   <section>
    <!-- 用户信息    -->
     <div v-if="user" class="container">
       <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
         <div class="row">
           <div class="col-sm-3 g-mb-40 g-mb-0--lg">

<!--             User Image-->
             <div class="g-mb-20">
               <img v-if="user._links.avatar" class="img-fluid w-100" v-bind:src="user._links.avatar" alt="Image Description">
             </div>
<!--             User Image-->

<!--             Actions-->
             <router-link v-if="$route.params.id == sharedState.user_id" v-bind:to="{name: 'SettingProfile'}"
                          class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
               <i class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
             </router-link>

             <button v-if="!user.is_following && $route.params.id != sharedState.user_id" v-on:click="onFollowUser($route.params.id)"
                     class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
               <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> Follow
             </button>

             <button v-if="user.is_following && $route.params.id != sharedState.user_id" v-on:click="onUnfollowUser($route.params.id)"
                     class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
               <i class="icon-user-unfollow g-pos-rel g-top-1 g-mr-5"></i> Unfollow
             </button>

             <button v-if="$route.params.id == sharedState.user_id" v-on:click="onDeleteUser($route.params.id)"
                     class="btn btn-block u-btn-outline-red g-rounded-50 g-py-12 g-mb-10">
               <i class="icon-ban g-pos-rel g-top-1 g-mr-5"></i> Delete Your Account
             </button>
<!--             end actions-->
           </div>

           <div class="col-sm-9">

<!--             tab nav-->
             <ul class="nav nav-tabs g-mb-20">
               <li class="nav-item">
                 <router-link v-bind:to="{name:'UserOverview'}" v-bind:active-class="'active'" class="nav-link" v-bind:class="isUserOverView">
                   Overview <span class="u-label g-font-size-11 g-bg-primary g-rounded-20 g-px-10">
                   <i class="icon-layers g-pos-rel g-top-1 g-mr-8"></i>
                 </span>
                 </router-link>
               </li>
               <li class="nav-item">
                 <router-link v-bind:to="{name:'UserFollowers'}" v-bind:active-class="'active'" class="nav-link">
                   Followers <span class="u-label g-font-size-11 g-bg-pink g-rounded-20 g-px-10">{{user.followers_count}}</span>
                 </router-link>
               </li>
               <li class="nav-item">
                 <router-link v-bind:to="{ name: 'UserFollowing' }" v-bind:active-class="'active'" class="nav-link">
                   Following <span class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10">{{ user.followeds_count }}</span>
                 </router-link>
               </li>
               <li class="nav-item">
                 <router-link v-bind:to="{ name: 'UserPostsList' }" v-bind:active-class="'active'" class="nav-link">
                   Posts <span class="u-label g-font-size-11 g-bg-purple g-rounded-20 g-px-10">{{ user.posts_count }}</span>
                 </router-link>
               </li>
               <li class="nav-item">
                 <router-link v-bind:to="{ name: 'UserFollowedsPostsList' }" v-bind:active-class="'active'" class="nav-link">
                   FollowingPosts <span class="u-label g-font-size-11 g-bg-blue g-rounded-20 g-px-10">{{ user.followed_posts_count }}</span>
                 </router-link>
               </li>

               <li class="nav-item">
                 <router-link v-bind:to="{ name: 'UserCommentsList' }" v-bind:active-class="'active'" class="nav-link">
                   Comments <span class="u-label g-font-size-11 g-bg-deeporange g-rounded-20 g-px-10">{{ user.comments_count }}</span>
                 </router-link>
               </li>
             </ul>

             <!-- 嵌套的子路由出口 -->
             <router-view></router-view>
           </div>
         </div>
       </div>
     </div>

     <!-- 当前登录的用户发表新博客文章 -->
     <div class="container">

       <div v-if="sharedState.is_authenticated && $route.params.id == sharedState.user_id" class="card border-0 g-mb-15">
<!--         panel header-->
         <div class="card-header d-flex align-items-center justfy-content-between g-bg-gray-light-v5 border-0 g-mb-15">
           <h3 class="h6 mb-0">
             <i class="icon-fire g-pos-rel g-top-1 g-mr-5"></i> Publish New Post
           </h3>
           <div class="dropdown g-mb-10 g-mb-0--md">
            <span class="d-block g-mr-minus-5 g-pa-5">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
           </div>
         </div>
         <!--           end panel header-->
       </div>

       <form v-if="sharedState.is_authenticated && $route.params.id == sharedState.user_id" @submit.prevent="onSubmitAdd" class="g-mb-40">
         <div class="form-group" v-bind:class="{'u-has-error-v1': postForm.titleError}">
           <input typeof="text" v-model="postForm.title" class="form-control" id="post_title" placeholder="标题">
           <small class="form-control-feedback" v-show="postForm.titleError">{{postForm.titleError}}</small>
         </div>

         <div class="form-group">
           <input type="text" v-model="postForm.summary" class="form-control" id="post_summary" placeholder="摘要">
         </div>

         <div class="form-group">
           <textarea v-model="postForm.body" class="form-control" id="postform_body" rows="5" placeholder="内容"></textarea>
           <small class="form-control-feedback" v-show="postForm.bodyError">{{postForm.bodyError}}</small>
         </div>

         <button type="submit" class="btn btn-primary">Submit</button>
       </form>
     </div>
   </section>
</template>

<script>
  import store from '../../store'
  // bootstrap-markdown 编辑器依赖的 JS 文件，初始化编辑器在组件的 created() 方法中，同时它需要 JQuery 支持哦
  import '../../assets/bootstrap-markdown/js/bootstrap-markdown.js'
  import '../../assets/bootstrap-markdown/js/bootstrap-markdown.zh.js'
  import '../../assets/bootstrap-markdown/js/marked.js'

    export default {
        name: "User",
      data(){
          return{
            sharedState: store.state,   //各种状态
            user: '',
            postForm: {
              title: '',
              summary: '',
              body: '',
              errors: 0,
              titleError: null,
              bodyError: null
            }
          }
      },
      computed:{
        isUserOverView: function () {
          const tabs = ['UserFollowers', 'UserFollowing', 'UserPostsList', 'UserFollowedPostsList']
          if (tabs.indexOf(this.$route.name) == -1){
            return 'active'
          } else {
            return ''
          }
        }
      },
      methods:{
          getUser(id){
            const path = `/api/users/${id}`
            this.$axios.get(path)
              .then((response)=>{
                this.user = response.data
              })
              .catch((error)=>{
                //eslint-disable-next-line
                console.error(error)
              })
          },

        onFollowUser(id){
            const path = `/api/follow/${id}`
          this.$axios.get(path)
            .then((response)=>{
              this.getUser(id)
            })
            .catch((error)=>{
              console.error(error)
            })
        },

        onUnfollowUser(id){
            const path = `/api/unfollow/${id}`
          this.$axios.get(path)
            .then((response)=>{
              this.getUser(id)
            })
            .catch((error)=>{
              console.error(error)
            })
        },

        onDeleteUser(id){
            this.$swal({
              title: "Are you sure?",
              text: "Please provide your password.",
              input: 'password',
              type: "warning",
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              inputValidator: (value)=>{
                return !value && 'Please provide a valid password.'
              }
            }).then((result)=>{
              if(result.value){
                const path = '/api/tokens'
                //axios实现Basic auth需要在config中设置auth这个属性即可
                this.$axios.post(path, {}, {
                  auth:{
                    'username': this.user.username,
                    'password': result.value
                  }
                }).then((response)=>{
                  const path = `/api/users/${id}`
                  this.$axios.delete(path)
                    .then((response)=>{
                      this.$swal('Deleted', 'You are anonymous now, Goodby!', 'success')
                      store.logoutAction()
                      this.user = ''
                      this.$router.push('/')
                    })
                    .catch((error)=>{
                      console.log(error.response.data)
                    })
                }).catch((error)=>{
                  this.$toasted.error('Invalid password, you cannot delete this account', {icon: 'fingerprint'})
                })
              }else{
                this.$swal('Cancelled', 'Your account is safe :)', 'error')
              }
            })
        },

        onSubmitAdd(e){
            this.postForm.errors = 0

          if(!this.postForm.title){
            this.postForm.errors++
            this.postForm.titleError = 'Title is required.'
          } else {
            this.postForm.titleError = null
          }

          if(!this.postForm.body){
            this.postForm.errors++
            this.postForm.bodyError = 'Body is required.'
            // 给 bootstrap-markdown 编辑器内容添加警示样式，而不是添加到 #post_body 上
            $('.md-editor').closest('.form-group').addClass('u-has-error-v1')  // Bootstrap 4
          } else {
            this.postForm.bodyError = null
            $('.md-editor').closest('.form-group').removeClass('u-has-error-v1')
          }

          if (this.postForm.errors > 0){
            return false
          }

          const path = '/api/posts'
          const payload = {
            title: this.postForm.title,
            summary: this.postForm.summary,
            body: this.postForm.body
          }
          this.$axios.post(path, payload)
            .then((response)=>{
              this.$toasted.success('Successed add a new post.', {icon: 'fingerprint'})
              this.postForm.title = ''
              this.postForm.summary = ''
              this.postForm.body = ''
              // 必须加个动态参数，不然路由没变化的话，UserPostsList 组件不会刷新重新加载博客列表
              this.$router.push({ name: 'UserPostsList', query: { id: response.data.id } })
            })
            .catch((error)=>{
              console.log(error.response.data)
            })
        }
      },
      created(){
          const user_id = this.$route.params.id
        this.getUser(user_id)
        // 初始化 bootstrap-markdown 插件
        $(document).ready(function() {
          $("#postform_body").markdown({
            autofocus:false,
            savable:false,
            iconlibrary: 'fa',  // 使用Font Awesome图标
            language: 'zh'
          })
        })
      },
      //当id变化后重新加载数据
      beforeRouteUpdate(to, from, next){
        // 在当前路由改变，但是该组件被复用时调用
        // 举例来说，对于一个带有动态参数的路径 /foo/:id，在 /foo/1 和 /foo/2 之间跳转的时候，
        // 由于会渲染同样的 Foo 组件，因此组件实例会被复用。而这个钩子就会在这个情况下被调用。
        // 可以访问组件实例 `this`
        next()
        this.getUser(to.params.id)
        $(document).ready(function() {
          $("#postform_body").markdown({
            autofocus:false,
            savable:false,
            iconlibrary: 'fa',  // 使用Font Awesome图标
            language: 'zh'
          })
        })
      }
    }
</script>

<style scoped>

</style>
