import axios from 'axios'
import store from './store'
import router from './router'
import Vue from 'vue'


//基础配置
axios.defaults.timeout = 5000   //超出时间
axios.defaults.baseURL = 'http://localhost:5000/api'

//add a request interceptor
axios.interceptors.request.use(function (config) {
  //do something before request is sent
  const token = window.localStorage.getItem('codershui-token')
  if (token){
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, function (error) {
  //do something with request error
  return Promise.reject(error)
})

//add a response interceptor
//jwt过期后，再次访问会返回401，用axios自动处理这个错误，不是/login路由全都跳转到此
axios.interceptors.response.use(function (response) {
  //do something with response data
  return response
}, function (error) {
  //do something with response error
  switch (error.response.status) {
    case 401:
      //清除token及已认证等状态
          store.logoutAction()
          //跳转到登陆页
          if (router.currentRoute.path !== '/login'){
            Vue.toasted.error('401:认证失效，请先登陆', {icon:'fingerprint'})
            router.replace({
              path:'/login',
              query:{redirect:router.currentRoute.path},
            })
          }
          break
    case 404:
          Vue.toasted.error('404:Not Found',{icon:'fingerprint'})
          router.back()
          break
  }
  return Promise.reject(error)
})

export default axios
