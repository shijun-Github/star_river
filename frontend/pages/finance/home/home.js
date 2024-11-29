// pages/finance/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    channel_list:[ 
      {'id':12254, 'name':'开户教程'},
      {'id':10, 'name':'🔥 基金基础知识教程'}, 
      {'id':23, 'name':'如何场内申购'},
      {'id':23, 'name':'如何场外购买'}, 
      {'id':24, 'name':'如何场外转场内'}, 
      {'id':25, 'name':'如何场内卖出'}],
    item_list: [],
    page_index:1,
    page_size:12,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      item_list: [],
      page_index: 1
    })
    this.get_item_list()
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {
    // 回到头部
    wx.pageScrollTo({
      scrollTop: 0
    })
    // 手动控制回弹
    wx.stopPullDownRefresh()
    // 下拉刷新，需要重置的数据
    this.onLoad()
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    // 页码自增
    this.data.page_index += 1
    // 请求下一页数据
    this.get_item_list()
  },

  // 获取物品列表信息
  get_item_list: function (cb){
    wx.request({
      url: 'https://85910d51p2.zicp.fun/finance/get_fund_data',  
      // url: 'https://8f5910u512.vicp.fun/finance/get_fund_data',  
      method:'POST',
      header :{'content-type': 'application/json'},
      data: {
        "user_id": "dkafa12e2j", 
        "page_index": this.data.page_index, 
        "page_size": this.data.page_size, 
        "sort_type": 0
      },
      success: res => {
        const item_list_deal = res.data.res
        console.log("test==============+++++++++", item_list_deal)
        this.setData({
          item_list: [...this.data.item_list, ...item_list_deal]
        }) 
      }
    })
  },


  // 获取滚动条当前位置
  onPageScroll: function (e) {
    if (e.scrollTop >= 0) {
      this.setData({
        floorstatus: true,
        scrollTop: e.scrollTop
      });
    } else {
      this.setData({
        floorstatus: false
      });
    }
  },

  //回到顶部
  go_top: function (e) {  // 一键回到顶部
    if (wx.pageScrollTo) {
      wx.pageScrollTo({
        scrollTop: 0
      })
      this.setData({
        video_list: [],
        page_index: 1
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
      })
    }
  },
})