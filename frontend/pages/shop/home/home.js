import time_tool from '../utils/time_tool'
import produce_sign from '../utils/produce_sign'

Page({
  /**
   * 页面的初始数据
   */
  data: {
    item_list_l:[],
    item_list_r:[],
    channel_list:[
      {'id':2, 'name':'精选卖场'},
      {'id':10, 'name':'9.9包邮'},
      {'id':22, 'name':'实时热销榜'},
    //   {'id':25, 'name':'超市'},
      {'id':28, 'name':'美妆穿搭'},
      {'id':153, 'name':'历史最低价商品榜'}
    ],
    current_channel: 2,
    page_index:1,
    page_size:10,
    scroll_top: 0, //滚动条高度

    // 定义顶部栏-
    page_show:false,
    navHeight: '',
    menuButtonInfo: {},
    searchMarginTop: 0, // 搜索框上边距
    searchWidth: 0, // 搜索框宽度
    searchHeight: 0 ,// 搜索框高度
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      item_list_l:[],
      item_list_r:[],
      page_index:1
    })
    this.func_get_item_list()  // 获取列表

    // getApp().get_user_info_self().then(() => {   // 执行完异步任务1和异步任务2后的逻辑
    //   const t = getApp().globalData
    //   console.log('00000000000000000000000000000', t.user_info)
    //   this.func_get_item_list()  // 获取列表
    //   })

    // 自定义首页顶部
    var systeminfo=wx.getSystemInfoSync()
    //console.log(systeminfo.windowHeight)
    this.setData({
      movehight:systeminfo.windowHeight,
      movehight2:systeminfo.windowHeight-100
    })
    this.setData({
      menuButtonInfo: wx.getMenuButtonBoundingClientRect()
    })
    console.log(this.data.menuButtonInfo)
    const { top, width, height, right } = this.data.menuButtonInfo
    wx.getSystemInfo({
      success: (res) => {
        const { statusBarHeight } = res
        const margin = top - statusBarHeight
        this.setData({
          navHeight: (height + statusBarHeight + (margin * 2)),
          searchMarginTop: statusBarHeight + margin, // 状态栏 + 胶囊按钮边距
          searchHeight: height,  // 与胶囊按钮同高
          searchWidth: right - width -40// 胶囊按钮右边坐标 - 胶囊按钮宽度 = 按钮左边可使用宽度
        })
      }
    })
  },

  func_get_item_list: function (cb){
    // const url_pre = 'https://85910d51p2.zicp.fun'
    const url_pre = getApp().globalData.apiUrl
    console.log('99999-----+++++++++++++++')
    console.log(this.data)
    console.log('99999-----+++++++++++++++')
    wx.request({
      url: url_pre + 'goods/home/recommend',
      method:'POST',
      header :{'Content-Type': 'application/json'},
      data : {
        'channel': this.data.current_channel,
        'page_index': this.data.page_index,
        'page_size': this.data.page_size
      },
      success: res => {
        const item_list_batch = res.data.res_data
        console.log("---------12345678900000000000", typeof(res.data), res.data)
        if (item_list_batch.length in [null, 0]){
            wx.showModal({
                title: '提示',
                content: '本频道已经没有内容，切换到其他频道看看'
              })
        }
        var t_l = []
        var t_r = []
        for (var i = 0; i < item_list_batch.length; i++) {
          if (i % 2 === 0) {
            t_l.push(item_list_batch[i]);
          } else {
            t_r.push(item_list_batch[i]);
          }
        }
        this.setData({
          item_list_l: [...this.data.item_list_l, ...t_l],
          item_list_r: [...this.data.item_list_r, ...t_r]
        })
      }
    })
  },

  // 去搜索页
  goto_search_page(e) {
    wx.navigateTo({
      url: '/pages/shop/goods/search/index',
    })
  },

  // 用户点击某个channel
  select_channel:function(e){
    // 切换选项卡，需要重置的数据
    this.setData({
      item_list_l:[],
      item_list_r:[],
      current_channel: e.target.dataset.id,
      page_index:1,
    })
    this.func_get_item_list() // 重新发起数据请求
  },

  // 去商品详情页
  goto_goods_detail:function (params) {
    const item = params.currentTarget.dataset.goods_detail_home
    wx.navigateTo({
    url: '/pages/shop/goods/details-jd/index?goods_info=' + JSON.stringify({'skuId': item.item_id})
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
    // 下拉刷新，需要重置的数据
    this.setData({
      item_list_l:[],
      item_list_r:[],
      page_index: 1
    })
    // 重新发起数据请求
    this.func_get_item_list().then(() => {
      // 当 1 完成后，执行 2
      wx.stopPullDownRefresh()
    })
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    // 页码自增
    this.data.page_index += 1
    // 请求下一页数据
    this.func_get_item_list()
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

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
    } else {
      wx.showModal({
        title: '提示',
        content: '当前微信版本过低，无法使用该功能，请升级到最新微信版本后重试。'
      })
    }
  },
})