export default {
  debug:true,
  state:{
    // is_new: false,
    is_authenticated: window.localStorage.getItem('codershui-token')?true:false,
    //用户登陆后，就算刷新页面也能再次计算出user_id
    user_id: window.localStorage.getItem('codershui-token')?JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1])).user_id:0
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
    this.state.user_id = JSON.parse(atob(window.localStorage.getItem('codershui-token').split('.')[1])).user_id
  },
  logoutAction(){
    if (this.debug) {console.log('logoutAction triggered')}
    window.localStorage.removeItem('codershui-token')
    this.state.is_authenticated = false
    this.state.user_id = 0
  }
}
