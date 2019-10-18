import Vue from 'vue'
import Router from 'vue-router'
import Ping from '@/components/Ping'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Profile from "../components/Profile";
import EditProfile from "../components/EditProfile";

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
      name:'Profile',
      component:Profile,
      meta:{
        requiresAuth:true
      }
    },
    {
      path:'/edit-profile',
      name:'EditProfile',
      component:EditProfile,
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
    console.log('here')
    console.log(to.matched)
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
