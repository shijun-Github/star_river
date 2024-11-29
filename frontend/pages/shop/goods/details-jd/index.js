
import time_tool from '../../utils/time_tool'
import produce_sign from '../../utils/produce_sign'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    goods_detail:{},
    goods_detail_home:{},
    coupon_link: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const goods_info = JSON.parse(options.goods_info)
    var skuIds = [goods_info.skuId]
    this.get_goods_detail(skuIds)
  },

  get_goods_detail: function (skuIds) {
    this.isLoading = true
    var data_params =  {
      // 系统参数
      'appKey':'65b0bc2864fba',
      'version':'v1.0.0',
      // 业务参数
      'skuIds':skuIds[0]
    }
    data_params['signRan'] = produce_sign.dataoke_sign(data_params)
    wx.request({
      url: 'https://openapi.dataoke.com/api/dels/jd/goods/get-details',
      method:'GET',
      header :{'Content-Type': 'application/json'},
      data : data_params,
      success: res => {
        this.setData({
          goods_detail: res.data.data[0],
        })
      }
    })
  },

  collect_goods:function(params){
    const materialUrl = "https://" +  this.data.materialUrl
    // wx.navigateToMiniProgram({
    //   appId: 'wx91d27dbf599dff74',
    //   path: 'pages/union/proxy/proxy?spreadUrl=' + materialUrl,
    //   success(res) {
    //     console.log("success--", res)
    //   },
    //   fail:function(e){
    //     console.log("fail--", e)
    //   }
    // })
    // wx.navigateToMiniProgram({
    //   appId: 'wx91d27dbf599dff74',
    //   path: 'pages/union/proxy/proxy?spreadUrl=' + materialUrl,
    //   success(res) {
    //     console.log("success--", res)
    //   },
    //   fail:function(e){
    //     console.log("fail--", e)
    //   }
    // })
  },

  buy_now: function (params) {
    const data_params = {
      'appKey':'65b0bc2864fba',
      'version':'v1.0.0',
      'materialId':this.data.goods_detail.materialUrl,
      'unionId':2034194664,
      'pid':'2034194664_4101236210_3100922957'
    }
    data_params['signRan'] = produce_sign.dataoke_sign(data_params)
    wx.request({
      url: 'https://openapi.dataoke.com/api/dels/jd/kit/promotion-union-convert',  
      method:'GET',header :{'Content-Type': 'application/json'},
      data:data_params,
      success: res => {
        // 跳转到优惠券链接
        wx.navigateToMiniProgram({
          appId: 'wx91d27dbf599dff74',
          path: 'pages/union/proxy/proxy?spreadUrl=' + res.data.data.shortUrl,
          success(res) {
            console.log("success--", res)
          }
        })
      }
    })
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

  }
})