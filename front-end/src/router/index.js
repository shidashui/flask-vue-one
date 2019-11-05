import Vue from 'vue'
import Router from 'vue-router'
// 测试与后端连通性
import Ping from '@/components/Ping'
// 首页
import Home from "../components/Home";
// 用户认证：注册与登录
import Login from "../components/Auth/Login";
import Register from "../components/Auth/Register";
//用户个人主页
import User from "../components/Profile/User";
import Overview from "../components/Profile/Overview";
import Followers from "../components/Profile/Followers";
import Following from "../components/Profile/Following";
import UserPostsList from "../components/Profile/Posts";
import UserFollowedsPostsList from "../components/Resources/PostsResource";
//用户个人设置
import Settings from "../components/Settings/Settings";
import Profile from "../components/Settings/Profile";
import Account from "../components/Settings/Account";
import Email from "../components/Settings/Email";
//博客详情页
import PostDetail from "../components/PostDetail";
import UserCommentsList from "../components/Comment/UserCommentsList";




Vue.use(Router)

const router = new Router({
  routes: [
    {
      path:'/',
      name:'Home',
      component:Home,
      meta:{
        requiresAuth:true
      }
    },
    // 博客文章详情页
    {
      path:'/post/:id',
      name:'PostDetail',
      component:PostDetail
    },
    {
      path:'/login',
      name:'Login',
      component:Login
    },
    {
      path:'/register',
      name:'Register',
      component:Register
    },
    {
      path:'/user/:id',
      // name:'User',
      component:User,
      children:[
        // Overview will be rendered inside User's <router-view>
        // when /user/:id is matched
        // 注意： 要有默认子路由，父路由不能指定 name
        {path: '', component: Overview},
        {path: 'overview', name: 'UserOverview', component: Overview},

        // Followers will be rendered inside User's <router-view>
        //         // when /user/:id/followers is matched
        {path: 'followers', name: 'UserFollowers', component: Followers},

        // Following will be rendered inside User's <router-view>
        // when /user/:id/following is matched
        {path: 'following', name: 'UserFollowing', component:Following},

        // UserPostsList will be rendered inside User's <router-view>
        // when /user/:id/posts is matched
        {path: 'posts', name: 'UserPostsList', component:UserPostsList},

        // UserFollowedsPostsList will be rendered inside User's <router-view>
        // when /user/:id/followeds-posts is matched
        {path: 'followeds-posts', name: 'UserFollowedsPostsList', component: UserFollowedsPostsList},

        {path: 'comments', name: 'UserCommentsList', component: UserCommentsList}
      ],
      meta:{
        requiresAuth:true
      }
    },
    {
      path:'/settings',
      component:Settings,
      children: [
        {path: '', component: Profile},
        {path: 'profile', name: 'SettingProfile', component: Profile},
        {path: 'account', name: 'SettingAccount', component: Account},
        {path: 'emial', name: 'SettingEmail', component: Email},
        {path: 'notification', name: 'SettingNotification', component: Notification}
      ],
      meta:{
        requiresAuth:true
      }
    },
    {
      path:'/ping',
      name:'Ping',
      component:Ping
    }
  ]
})

router.beforeEach((to, from, next) =>{
  const token = window.localStorage.getItem('codershui-token')
  if (to.matched.some(record =>record.meta.requiresAuth)&&(!token||token===null)){
    Vue.toasted.show('Please log in to access this page.', { icon: 'fingerprint' })
    next({
      path:'/login',
      query:{redirect: to.fullPath}
    })
  } else if (token && to.name == 'Login'){
    //用户已登录，再次访问登陆页面不让访问
    next({
      path:from.fullPath
    })
  } else if (to.matched.length === 0){ //要前往的路由不存在时
    // console.log('here')
    // console.log(to.matched)
    Vue.toasted.error('404: Not Found', {icon:'fingerprint'})
    if (from.name){
      next({
        name:from.name
      })
    }else{
      next({
        path:'/'
      })
    }
  } else {
    next()
  }
})

export default router
