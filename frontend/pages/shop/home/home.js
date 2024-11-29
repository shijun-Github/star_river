// pages/home/home.js

import time_tool from '../utils/time_tool'
import produce_sign from '../utils/produce_sign'

Page({
  /**
   * 页面的初始数据
   */
  data: {
    goods_list:[], 
    goods_list_tmp:[], 
    goods_channel_list:[ 
      {'id':2, 'name':'精选卖场'}, 
      {'id':10, 'name':'9.9包邮'}, 
      {'id':22, 'name':'实时热销榜'}, 
      {'id':25, 'name':'超市'},
      {'id':28, 'name':'美妆穿搭'},
      {'id':153, 'name':'历史最低价商品榜'}
    ],

    current_channel: 2,
    page_index:1,
    page_size:30,
    swiper_item_list: ['https://cdn-we-retail.ym.tencent.com/tsr/home/v2/banner1.png', 
    'https://cdn-we-retail.ym.tencent.com/tsr/home/v2/banner2.png', 
    'https://cdn-we-retail.ym.tencent.com/tsr/home/v2/banner3.png', 
    'https://cdn-we-retail.ym.tencent.com/tsr/home/v2/banner4.png', 
    'https://cdn-we-retail.ym.tencent.com/tsr/home/v2/banner5.png'],
    tab_list:[{name:11, url:'../images/00.png'}, {name:22, url:'../images/01.png'}, 
    {name:9.9 , url:'../images/02.png'}, {name:44, url:'../images/03.png'}, 
    {name:55, url:'../images/04.png'}, {name:55, url:'../images/05.png'}, 
    {name:66, url:'../images/06.png'}, {name:77, url:'../images/07.png'}],
    scroll_top: 0, //滚动条高度

    // 定义顶部栏- 
    page_show:false,
    navHeight: '',
    menuButtonInfo: {},
    searchMarginTop: 0, // 搜索框上边距
    searchWidth: 0, // 搜索框宽度
    searchHeight: 0 ,// 搜索框高度
  },

  //控制回到顶部按钮的显示与消失


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      goods_list: [],
      goods_list_tmp: [],
      page_index:1,
    })

    getApp().get_user_info_self().then(() => {
      // 执行完异步任务1和异步任务2后的逻辑
      const t = getApp().globalData
      console.log('00000000000000000000000000000', t, t.userInfo)
      this.get_goods_list()  // 获取列表
      })

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

  test(){
    // 等个性化上线了再用下面的方法
    wx.request({
      url: 'https://85910d51p2.zicp.fun/search/goods_search',  
      method:'POST',
      header :{'Content-Type': 'application/json'},
      header :{'Content-Type': 'application/json'},
      data: {
        "search_word": "牛奶", "page_size": 20, "page_index": 1, "sort_type": 0
      },
      success: res => {
        console.log("test==============+++++++++", res)
      }
    })
  },

  // 获取商品列表
  get_goods_list: function (cb){
    return new Promise(resolve => {
      const select_ch_id = this.data.current_channel
      this.get_goods_list_jd_p(select_ch_id)
      
      // if (select_ch_id == 23){
      //   // 将异步任务按照顺序执行
      //   this.get_goods_list_jd().then(() => {
      //     // 当 1 完成后，执行 2
      //     return this.get_goods_list_pdd();
      //   }).then(() => {
      //     // 执行完异步任务1和异步任务2后的逻辑
      //     this.filter_goods()
      //   })
      // }
      // if (select_ch_id == 10){
      //   this.get_goods_list_jd_9_9().then(() => {
      //     this.filter_goods()
      //   })
      // }
      // if (select_ch_id == 11){
      //   this.get_goods_list_jd_discount_brand().then(() => {
      //     this.filter_goods()
      //   })
      // }
      resolve()
    })

    // // 等个性化上线了再用下面的方法
    // wx.request({
    //   url: 'http://118.178.231.195:443/recommend/home_recommend',  
    //   method:'POST',
    //   header :{'Content-Type': 'application/x-www-form-urlencoded'},
    //   header :{'Content-Type': 'application/json'},
    //   data: {
    //     "page_index": this.data.page_index, 
    //     "page_size": this.data.page_size
    //   },
    //   success: res => {
    //     this.setData({
    //       goods_list: [...this.data.goods_list, ...res.data.res_]
    //     }) 
    //   }
    // })
  },

  get_goods_list_jd_p: function (cb){
    return new Promise(resolve => {
      var data_params =  {
        // 系统参数
        'appKey':'65b0bc2864fba',
        'version':'v1.0.0',
        // 业务参数
        'eliteId': cb,
        'pageIndex': this.data.page_index, 
        'pageSize': this.data.page_size,
      }
      data_params['signRan'] = produce_sign.dataoke_sign(data_params)
      data_params['globalData'] = getApp().globalData
      console.log("data_params===========+++++++++", data_params, data_params.globalData.userInfo)
      wx.request({
        url: 'https://openapiv2.dataoke.com/open-api/jd-jingfen-goods',
        method:'GET',
        header :{'Content-Type': 'application/json'},
        data : data_params,
        success: res => {
          const goods_list_deal = []
          if (res.data.msg !== '成功'){
            console.log("刷到底了")
            goods_list_deal.push({'platform':'jd', 'goods_info': {'skuName':'本页内容已经刷完，看看其他栏目'}})
            console.log("到底了+++", goods_list_deal)
          } else{
            const goods_list_ori = res.data.data.list
            console.log("test==000000000000000+++", goods_list_ori[0])
            const t = getApp().globalData
            console.log("test==1111111111111111111+++", t)
            for (var i in goods_list_ori) {
              const goods = goods_list_ori[i]
              // 过滤无优惠的内容
              const coupon_info = goods['couponInfo']['couponList']
              if (coupon_info.length == 0 || coupon_info[0]['discount'] < 5) {
                continue
              }
              goods_list_deal.push({'platform':'jd', 'goods_info': goods})
            }
          }
          this.setData({
            goods_list: [...this.data.goods_list, ...goods_list_deal]
          }) 
        },
      })
      resolve()
    })
  },

  get_goods_list_jd: function (cb){
    return new Promise(resolve => {
      var data_params =  {
        // 系统参数
        'appKey':'65b0bc2864fba',
        'version':'v1.0.0',
        // 业务参数
        'pageId': this.data.page_index, 
        'pageSize': this.data.page_size,
      }
      data_params['signRan'] = produce_sign.dataoke_sign(data_params)

      wx.request({
        url: 'https://openapi.dataoke.com/api/dels/jd/column/list-real-ranks',
        method:'GET',
        header :{'Content-Type': 'application/json'},
        // header :{'Content-Type': 'application/x-www-form-urlencoded'},
        data : data_params,
        success: res => {
          const goods_list_ori = res.data.data.list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            // const couponUseStartTime = goods['couponUseStartTime']
            // const couponUserEndTime = goods['couponUserEndTime']
            // const current_time = time_tool.timestamp2time(new Date())
            // // 将无法使用的优惠券过滤掉
            // if (current_time <= couponUseStartTime || current_time >= couponUserEndTime) {
            //   continue
            // }
            const goods_info = {
              'goods_id': goods['skuId'],
              'material_url': goods['materialUrl'],
              'goods_name': goods['skuName'],
              'goods_mall': goods['shopName'],
              'goods_main_image': goods['picMain'],
              'goods_price': goods['originPrice'],
              'coupon_discount': goods['couponAmount'],
              'goods_coupon_price': goods['actualPrice'], // 商品券后价格
              'is_free_freight_risk': goods['isFreeFreightRisk'],
              'goods_comment_share': goods['goodsCommentShare'],
              'actual_commission': goods['actualPrice'] * goods['commissionShare']
            }
            goods_list_deal.push({'platform':'jd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          }) 
        },
      })
      resolve()
    })
  },

  get_goods_list_jd_9_9(){
    return new Promise(resolve => {
      var data_params =  {
        // 系统参数
        'appKey':'65b0bc2864fba',
        'version':'v1.0.0',
        // 业务参数
        'pageId': this.data.page_index, 
        'pageSize': this.data.page_size,
      }
      data_params['signRan'] = produce_sign.dataoke_sign(data_params)

      wx.request({
        url: 'https://openapi.dataoke.com/api/dels/jd/column/list-nines',
        method:'GET',
        header :{'Content-Type': 'application/json'},
        data: data_params,
        success: res => {
          const goods_list_ori = res.data.data.list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            // const couponUseStartTime = goods['couponUseStartTime']
            // const couponUserEndTime = goods['couponUserEndTime']
            // const current_time = time_tool.timestamp2time(new Date())
            // // 将无法使用的优惠券过滤掉
            // if (current_time <= couponUseStartTime || current_time >= couponUserEndTime) {
            //   continue
            // }
            const goods_info = {
              'goods_id': goods['skuId'],
              'material_url': goods['materialUrl'],
              'goods_name': goods['skuName'],
              'goods_mall': goods['shopName'],
              'goods_main_image': goods['picMain'],
              'goods_price': goods['originPrice'],
              'coupon_discount': goods['couponAmount'],
              'goods_coupon_price': goods['actualPrice'], // 商品券后价格
              'is_free_freight_risk': goods['isFreeFreightRisk'],
              'goods_comment_share': goods['goodsCommentShare'],
              'actual_commission': goods['actualPrice'] * goods['commissionShare']
            }
            goods_list_deal.push({'platform':'jd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          }) 
          resolve()
        },
      })
    })
  },

  get_goods_list_jd_discount_brand: function (cb){
    return new Promise(resolve => {
      var data_params =  {
        // 系统参数
        'appKey':'65b0bc2864fba',
        'version':'v1.0.0',
        'v': '1.0',
        // 业务参数
        'pageId': this.data.page_index, 
        'pageSize': this.data.page_size,
      }
      data_params['signRan'] = produce_sign.dataoke_sign(data_params)

      wx.request({
        url: 'https://openapi.dataoke.com/api/dels/jd/column/list-discount-brand',
        method:'GET',
        header :{'Content-Type': 'application/json'},
        data: data_params,
        success: res => {
          const goods_list_ori = res.data.data.list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            // const couponUseStartTime = goods['couponUseStartTime']
            // const couponUserEndTime = goods['couponUserEndTime']
            // const current_time = time_tool.timestamp2time(new Date())
            // // 将无法使用的优惠券过滤掉
            // if (current_time <= couponUseStartTime || current_time >= couponUserEndTime) {
            //   continue
            // }
            const goods_info = {
              'goods_id': goods['skuId'],
              'material_url': goods['materialUrl'],
              'goods_name': goods['skuName'],
              'goods_mall': goods['shopName'],
              'goods_main_image': goods['picMain'],
              'goods_price': goods['originPrice'],
              'coupon_discount': goods['couponAmount'],
              'goods_coupon_price': goods['actualPrice'], // 商品券后价格
              'is_free_freight_risk': goods['isFreeFreightRisk'],
              'goods_comment_share': goods['goodsCommentShare'],
              'actual_commission': goods['actualPrice'] * goods['commissionShare']
            }
            goods_list_deal.push({'platform':'jd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          }) 
          resolve()
        },
      })
    })
  },

  get_goods_list_pdd: function (cb) {
    return new Promise(resolve => {
      var wx_params = {
        //公共参数
        "type": 'pdd.ddk.goods.recommend.get',
        'client_id': 'bdb697eba7534d25a9d4df355e2ac269',
        'access_token': '0bf1abb7a680467fb73bed23868362c3267b3766',
        'timestamp': ((Date.parse(new Date()))/1000).toString(),

        // 用户参数：具体不同条件的
        'goods_img_type': 1,
        'offset':this.data.page_index*this.data.page_size, 
        'limit':this.data.page_size,
        'pid': '38846732_276520589',
      }
      wx_params['sign'] = produce_sign.pdd_sign(wx_params)
      wx.request({
        url: 'https://gw-api.pinduoduo.com/api/router',
        method:'POST',
        header:{'content-type': 'application/json'},
        data:wx_params,
        success: res => {
          const goods_list_ori = res.data.goods_basic_detail_response.list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            const goods_info = {
              'goods_id': goods['goods_sign'],
              'goods_name': goods['goods_name'],
              'goods_mall': goods['mall_name'],
              'serv_txt': goods['serv_txt'], 
              'goods_main_image': goods['goods_thumbnail_url'],
              'goods_price': goods['min_group_price']/100,
              'coupon_discount': goods['coupon_discount']/100,
              'goods_coupon_price': (goods['min_group_price'] - goods['coupon_discount'])/100// 商品券后价格
            }
            goods_info['actual_commission'] = goods_info['goods_coupon_price'] * (goods['promotion_rate']/1000)
            goods_list_deal.push({'platform':'pdd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          })
          resolve()  // 要在赋值完成后再返回值，最好紧跟，因为服务没有返回值时，是不会等任务结束再执行下面的代码
        },
      })
      // resolve() //在赋值完成后再返回值，最好紧跟，因为服务wx.request({})没有返回值，不会等任务结束再执行下面代码   
    })
  },

  filter_goods(){
    return new Promise(resolve => {
      const t = this.data.goods_list_tmp
      const tt = []
      for (var i in t) {
        const goods = t[i]
        if (goods['goods_info']['actual_commission'] < 1.0 ){  //券小于5元的商品过滤掉
          continue
        }
        tt.push(goods)
      }
      // 将本次请求的结果打乱后赋值给 goods_list
      this.setData({
        goods_list: [...this.data.goods_list, ...tt.sort(() => Math.random() - 0.5)]
      }) 
      // 已完goods_list_tmp 立马置空释放
      this.setData({
        goods_list_tmp: [],
      })
      resolve()
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
      goods_list: [],
      goods_list_tmp:[],
      current_channel: e.target.dataset.id,
      page_index:1,
    })
    this.get_goods_list() // 重新发起数据请求
  },

  // 去商品详情页
  goto_goods_detail:function (params) {
    const item = params.currentTarget.dataset.goods_detail_home
    if (item.platform == 'jd') {
      wx.navigateTo({
        url: '/pages/shop/goods/details-jd/index?goods_info=' + JSON.stringify({'skuId': item.goods_info.skuId})
      })
    }
    if (item.platform == 'pdd') {
      const goods_sign = item.goods_info.goods_id
      wx.navigateTo({
        url: '/pages/shop/goods/details-pdd/index?goods_sign=' + goods_sign,
      })
    }
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
      goods_list: [],
      goods_list_tmp: [],
      page_index: 1
    })
    // 重新发起数据请求
    this.get_goods_list().then(() => {
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
    this.get_goods_list()
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