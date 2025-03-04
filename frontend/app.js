App({
  globalData: {
    userInfo: {openid:null},
     /*   'http://127.0.0.1:8588/'   这种本地地址写法，是无法进行真机调试的
    https://85910d51p2.zicp.fun/  //请求域名  */   
    // apiUrl: 'http://127.0.0.1:8588/'
    apiUrl: 'http://10.1.30.237:8588/'
    // apiUrl: 'http://192.168.0.111:8588/
    // apiUrl: 'http://192.168.1.15:8588/'
  },
  onLaunch: function () {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // 登录， 暂时先不开发
    // this.get_user_info_self()
  },

  get_user_info_self: function (argument) {
    var that = this;
    return new Promise(function(resolve, reject){
      if (!that.globalData.userInfo.openid) {
        wx.login({
          success: res_log => {
            console.log('get_----1111111111111+++++++', res_log)
            // 发送 res.code 到后台换取 openId, sessionKey, unionId
            that.http('user/get_wx_login_code', {code:res_log.code}).then(res_info=>{
              console.log('get_----22222222222222222222+++++++', res_info)
              that.globalData.userInfo = res_info.data
            })
          }
        })
      } else {
            console.log('get_----user_info_self+++++++')
      }
      resolve()
    })
  },

  http: function (url, data='', method="POST") { //封装http请求
    const currency = {
      openid: this.globalData.openid
    }
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.apiUrl + url,
        data: Object.assign(currency,data),
        method: method,
        success: function (res) {
          if(res.statusCode != 200){
            wx.showModal({
              title: '提示',
              content: res.data.message,
              success: function (res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          }
          resolve(res)
        },
        fail: function (res) {
          reject(res);
        },
        complete: function () {
          console.log('complete,--+++++----');
        }
      })
    })
  }
})