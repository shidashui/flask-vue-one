export default {
  debug:true,
  state:{
    // is_new: false,
    is_authenticated: window.localStorage.getItem('codershui-token')?true:false,
    //用户登陆后，就算刷新页面也能再次计算出user_id
    user_id: window.localStorage.getItem('codershui-token')?JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1])).user_id:0,
    user_name: window.localStorage.getItem('codershui-token') ? JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1])).user_name : '',
    // 用户登录后，就算刷新页面也能再次计算出 user_avatar
    // 后端传 URL 必须先用 base64 编码，所以这里还要多进行一次 atob 解码 base64 字符串
    user_avatar: window.localStorage.getItem('codershui-token') ? atob(JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1])).user_avatar) : ''
  },
  //被vue-toasted插件替换
  // setNewAction (){
  //   if (this.debug){console.log('setNewAction triggered')}
  //   this.state.is_new = true
  // },
  // resetNotNewAction (){
  //   if (this.debug){console.log('resetNotNewAction triggered')}
  //   this.state.is_new = false
  // },
  loginAction(){
    if(this.debug){console.log('loginAction triggered')}
    this.state.is_authenticated = true
    const payload = JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1]))
    this.state.user_id = payload.user_id
    this.state.user_name = payload.user_name
    this.state.user_avatar = atob(payload.user_avatar)
  },
  logoutAction(){
    if (this.debug) {console.log('logoutAction triggered')}
    window.localStorage.removeItem('codershui-token')
    this.state.is_authenticated = false
    this.state.user_id = 0
    this.state.user_name = ''
    this.state.user_avatar = ''
  }
}
