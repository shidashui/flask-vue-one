import Vue from 'vue'
import Router from 'vue-router'
import Ping from '@/components/Ping'
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Profile from "../components/Profile";

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
      path:'/profile',
      name:'Profile',
      component:Profile,
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
  } else {
    next()
  }
})

export default router
