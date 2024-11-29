 // pages/goods/details/index.js
import produce_sign from '../../utils/produce_sign'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    goods_detail:{},
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 根据goods_sign请求接口获取信息
    // ...
    const goods_sign = options.goods_sign

    var wx_params = {
      //公共参数
      'type': 'pdd.ddk.goods.detail',
      'client_id': 'bdb697eba7534d25a9d4df355e2ac269',
      'access_token': '0bf1abb7a680467fb73bed23868362c3267b3766',
      'pid': '38846732_276520589',
      'timestamp': ((Date.parse(new Date()))/1000).toString(),

      // 用户参数：具体不同条件的
      'goods_sign': goods_sign
    }
    wx_params['sign'] = produce_sign.pdd_sign(wx_params)

    wx.request({
      url: 'https://gw-api.pinduoduo.com/api/router',
      method:'POST',
      header:{'content-type': 'application/json'},
      data:wx_params,
      success:res =>{
        this.setData({
          goods_detail: res.data.goods_detail_response.goods_details[0],
        })
      }
    })
  },

  get_sim_goods:function (params) {

    
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  toBuyNow: function(e){
    const goods_sign = e.currentTarget.dataset.goods_sign

    var wx_params = {
      //公共参数
      'type': 'pdd.ddk.goods.promotion.url.generate',
      'client_id': 'bdb697eba7534d25a9d4df355e2ac269',
      'access_token': '0bf1abb7a680467fb73bed23868362c3267b3766',
      'timestamp': ((Date.parse(new Date()))/1000).toString(),

      // 用户参数：具体不同条件的
      'goods_sign': goods_sign,
      'generate_we_app': 'true',
      'p_id': '38846732_276520589',
    }
    wx_params['sign'] = produce_sign.pdd_sign(wx_params)

    wx.request({
      url: 'https://gw-api.pinduoduo.com/api/router',
      method:'POST',
      header:{'content-type': 'application/json'},
      data:wx_params,
      success: res=>{
        wx.navigateToMiniProgram({
          appId: 'wx32540bd863b27570',
          path: res.data.goods_promotion_url_generate_response.goods_promotion_url_list[0].we_app_info.page_path,
          success(res) {
            console.log("success--", res)
          },
          fail:function(e){
            console.log("fail--", e)
          }
        })

      },
      fail:function(e){
        console.log("生成链接fail--", e)
      }

    })
  }

  // ------------------- 下面是js页面的注释（因为js页面没办法写注释）----------------------
  /**
  下面连个字段放到json文件中，则直接将页面顶部内容取消，顶部区域也可以展示页面内容，而不是固定的内容
  "usingComponents":{},
  "navigationStyle": "custom"
   
   */
})