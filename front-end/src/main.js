// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
//导入css文件
//import bootstrap css and js files
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
//bootstrap-markdown 编辑器需要的样式
import './assets/bootstrap-markdown/css/bootstrap-markdown.min.css'
import './assets/bootstrap-markdown/css/custom.css'
import './assets/icon-awesome/css/font-awesome.min.css' //编辑器上的按钮图标使用font-awesome
// markdown 样式
import './assets/markdown-styles/github-markdown.css'
// 自定义 css 文件
import './assets/core.css'
import './assets/custom.css'
// 图标
import './assets/icon-line/css/simple-line-icons.css'
import './assets/icon-material/material-icons.css'
//消息插件
import VueToasted from 'vue-toasted'
//导入配置了全局拦截器后的axios
import axios from './http'
// 导入 moment.js 用来格式化 UTC 时间为本地时间
import moment from 'moment'




Vue.use(VueToasted,{
  //主题样式 primary、outline、bubble、
  theme:"bubble",
  //显示再页面哪个位置
  position:"top-center",
  //显示时长（毫秒）
  duration:3000,
  //支持的图标集合
  iconPack:'material',  // set your iconPack, defaults to material. material|fontawesome|custom-class
  //执行的动作
  action:{
    text:'Cancel',
    onClick:(e,toastObject)=>{
      toastObject.goAway(0)
    }
  }
})

// register the vue-sweetalert2 plugin on vue
import VueSweetalert2 from 'vue-sweetalert2'
Vue.use(VueSweetalert2)


// 使用 highlight.js 高亮代码。 vue-router 从 Home 页路由到 Post 页后，会重新渲染并且会移除事件
// 注册自定义指令，后续在组件中使用 v-highlight
import hljs from 'highlight.js'
// 样式文件，浅色：default, atelier-dune-light  深色：atom-one-dark, atom-one-dark-reasonable, monokai
import 'highlight.js/styles/atom-one-dark-reasonable.css'
Vue.directive('highlight',function (el) {
  let blocks = el.querySelectorAll('pre code');
  blocks.forEach((block)=>{
    hljs.highlightBlock(block)
  })
})

Vue.config.productionTip = false

//将$axios挂载到prototype上，在组件中可以直接使用this.$axios访问
Vue.prototype.$axios = axios
// 将 $moment 挂载到 prototype 上，在组件中可以直接使用 this.$moment 访问
Vue.prototype.$moment = moment

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})