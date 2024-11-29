import time_tool from '../../utils/time_tool'
import produce_sign from '../../utils/produce_sign'

Page({
  data:{
    // 搜索也刚刚进来时的初始数据
    searchIcon: 'https://ico.dongtiyan.com/tu-99.png', 
    // 点击搜索后得到的数据
    goods_list:[],  
    goods_list_tmp:[],  
    goods_order_list:[
      {'id':'', 'name':'综合'},
      // {'id':'price_0', 'name':'价格↓'},
      {'id':'price_1', 'name':'价格↑'},
      {'id':'commissionShare_0', 'name':'优惠券↓'},
    ],
    current_order:'',
    current_order_flag:'',
    current_order_sort:'',

    page_index:1,
    page_size:30,
    sort_type:0,
    search_word:'牛奶'
  },

  //监听input中的  search_word
  handleSubmit:function(e){
    //把监听的input的值添加到data里面
    this.setData({
      search_word : e.detail.value
    })
    console.log("handleSubmit search_word", this.data.search_word)
  },

  searchbegin:function (e) {
    this.setData({
      goods_list: [],
      page_index:1,
      current_order:'',
      current_order_flag:'',
      current_order_sort:'',
    })
    this.get_goods_list()
  },

  // 获取商品列表
  get_goods_list(){
    this.get_goods_list_jd_p()
    // return new Promise(resolve => {
    //   // 将异步任务按照顺序执行
    //   this.get_goods_list_jd().then(() => {
    //     // 当 1 完成后，执行 2
    //     return this.get_goods_list_pdd();
    //   }).then(() => {
    //     // 执行完异步任务1和异步任务2后的逻辑
    //     this.filter_goods()
    //   })
    //   resolve()
    // })
  },

  get_goods_list_jd_p(){
    const data_params = {
      'appKey':'65b0bc2864fba',
      'version':'v1.0.0',
      'keyword':this.data.search_word,
      'sortName':this.data.current_order,
      'sort': this.data.current_order_sort,
      'pageId': this.data.page_index,
      'pageSize' :this.data.page_size,
    }
    data_params['signRan'] = produce_sign.dataoke_sign(data_params)
    wx.request({
      url: 'https://openapi.dataoke.com/api/dels/jd/goods/search',  
      method:'GET',
      header :{'Content-Type': 'application/x-www-form-urlencoded'},
      data:data_params,
      success: res => { 
        const goods_list_ori = res.data.data.list
        const goods_list_deal = []
        for (var i in goods_list_ori) {
          const goods_info = goods_list_ori[i]
          goods_list_deal.push({'platform':'jd', 'goods_info': goods_info})
        }
        this.setData({
          goods_list: [...this.data.goods_list, ...goods_list_deal]
        }) 
        console.log('-+++++++++-', this.data.goods_list)
      }
    })

  },


  filter_goods(){
    
    // 对列表做些规则--筛选排序等
    // 按照 字段排序：降序（从大到小）
    const asc_compare_price = (a, b) => a.goods_info.goods_coupon_price - b.goods_info.goods_coupon_price;
    const desc_compare_price = (a, b) => b.goods_info.goods_coupon_price - a.goods_info.goods_coupon_price;

    const asc_compare_coupon_discount = (a, b) => a.goods_info.coupon_discount - b.goods_info.coupon_discount;
    const desc_compare_coupon_discount = (a, b) => b.goods_info.coupon_discount - a.goods_info.coupon_discount;
    
    if (this.data.current_order == 'price'){
      var order_list = []
      if (this.data.current_order_sort == 'desc'){
        order_list = this.data.goods_list_tmp.slice().sort(desc_compare_price)
      } else{
        order_list = this.data.goods_list_tmp.slice().sort(asc_compare_price)
      }
      this.setData({
        goods_list_tmp: order_list,
      })
    } 
    if (this.data.current_order == 'commissionShare') {
      var order_list = []
      if (this.data.current_order_sort == 'desc'){
        order_list = this.data.goods_list_tmp.slice().sort(desc_compare_coupon_discount)
      }
      this.setData({
        goods_list_tmp: order_list,
      })
    } 

    const t = this.data.goods_list_tmp
    const tt = []
    for (var i in t) {
      const goods = t[i]
      if (goods['goods_info']['actual_commission'] < 1.0 ){  // 佣金小于1元的过滤掉
        continue
      }
      tt.push(goods)
    }
    this.setData({
      goods_list: [...this.data.goods_list, ...tt]
    })
    // 已完goods_list_tmp 立马置空释放
    this.setData({
      goods_list_tmp: [],
    })
  },


  get_goods_list_jd(){
    return new Promise(resolve => {
      const data_params = {
        'appKey':'65b0bc2864fba',
        'version':'v1.0.0',
        'keyword':this.data.search_word,
        'sortName':this.data.current_order,
        'sort': this.data.current_order_sort,
        'pageId': this.data.page_index,
        'pageSize' :this.data.page_size,
      }
      data_params['signRan'] = produce_sign.dataoke_sign(data_params)
      wx.request({
        url: 'https://openapi.dataoke.com/api/dels/jd/goods/search',  
        method:'GET',
        header :{'Content-Type': 'application/x-www-form-urlencoded'},
        data:data_params,
        success: res => { 
          console.log('---------------', res)
          const goods_list_ori = res.data.data.list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            // const couponUseStartTime = goods['couponList'][0]['useStartTime']
            // const couponUserEndTime = goods['couponList'][0]['useEndTime']
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
              'goods_main_image': goods['whiteImage'],
              'goods_price': goods['price'],
              'coupon_discount': goods['couponList'].length ? goods['couponList'][0]['discount']:0,
              'goods_coupon_price': goods['lowestCouponPrice'], // 商品券后价格
              'actual_commission': goods['actualPrice'] * goods['commissionShare']
            }
            
            goods_list_deal.push({'platform':'jd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          }) 
          resolve()
        }
      })
    })
  },

  get_goods_list_pdd(){
    return new Promise(resolve => {
      var wx_params = {
        //公共参数
        "type": 'pdd.ddk.goods.search',
        'client_id': 'bdb697eba7534d25a9d4df355e2ac269',
        'access_token': '0bf1abb7a680467fb73bed23868362c3267b3766',
        'timestamp': ((Date.parse(new Date()))/1000).toString(),
        // 用户参数：具体不同条件的
        'pid': '38846732_276520589',
        'keyword': decodeURIComponent(encodeURIComponent(this.data.search_word)),
        'with_coupon': true,  //是否只返回优惠券的商品，false返回所有商品，true只返回有优惠券的商品
        'page_size': this.data.page_size,
        'page': this.data.page_index,
        'use_customized': true,
        'range_list':'[{"range_id":3,"range_from":500,"range_to":500000}, {"range_id":6,"range_from":100,"range_to":500000}, {"range_id":19,"range_from":1000,"range_to":500000}]',
        // 'sort_type': this.data.current_channel,
      }
      wx_params['sign'] = produce_sign.pdd_sign(wx_params)
      wx.request({
        url: 'https://gw-api.pinduoduo.com/api/router',
        method:'POST',
        header:{'content-type': 'application/json'},
        data:wx_params,
        success: res => {
          const goods_list_ori = res.data.goods_search_response.goods_list
          const goods_list_deal = []
          for (var i in goods_list_ori) {
            const goods = goods_list_ori[i]
            const goods_info = {
              'goods_id': goods['goods_sign'],
              'goods_name': goods['goods_name'],
              'goods_mall': goods['mall_name'],
              'goods_main_image': goods['goods_thumbnail_url'],
              'goods_price': goods['min_group_price']/100,
              'coupon_discount': goods['coupon_discount']/100,
              'goods_coupon_price': (goods['min_group_price'] - goods['coupon_discount'])/100 // 商品券后价格
            }
            goods_info['actual_commission'] = goods_info['goods_coupon_price'] * (goods['promotion_rate']/1000)
            goods_list_deal.push({'platform':'pdd', 'goods_info': goods_info})
          }
          this.setData({
            goods_list_tmp: [...this.data.goods_list_tmp, ...goods_list_deal]
          })
          resolve()
        },
      }) 
    }) 
  },


  // 用户点击某个order
  select_order:function(e){
    const select_order_sort_id = e.target.dataset.id
    console.log("当前激活的选项卡 select_order：", e, select_order_sort_id)
    // 切换选项卡，需要重置的数据
    if (select_order_sort_id == ''){
      this.setData({
        goods_list: [],
        current_order_sort: '',
        current_order: '',
        current_order_flag: '',
        page_index:1,
      })
    } else if (select_order_sort_id == 'price_0'){
      this.setData({
        goods_list: [],
        current_order_sort: 'desc',
        current_order: 'price',
        current_order_flag: 'price_0',
        page_index:1,
      })
    } else if (select_order_sort_id == 'price_1'){
      this.setData({
        goods_list: [],
        current_order_sort: 'asc',
        current_order: 'price',
        current_order_flag: 'price_1',
        page_index:1,
      })
    } else if (select_order_sort_id == 'commissionShare_0'){
      this.setData({
        goods_list: [],
        current_order_sort: 'desc',
        current_order: 'commissionShare',
        current_order_flag: 'commissionShare_0',
        page_index:1,
      })
    }  else if (select_order_sort_id == 'commissionShare_1'){
      this.setData({
        goods_list: [],
        current_order_sort: 'asc',
        current_order: 'commissionShare',
        current_order_flag: 'commissionShare_1',
        page_index:1,
      })
    } 
    else {
      this.setData({
        goods_list: [],
        current_order_sort: '',
        current_order: '',
        current_order_flag: '',
        page_index:1,
      })
    }
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
  },
  // goto_goods_detail:function (params) {
  //   const item = params.currentTarget.dataset.goods_detail_home
  //   console.log("00000000000000", item)
  //   if (item.platform == 'jd') {
  //     var skuId = String(item.goods_info.goods_id)
  //     var materialUrl = item.goods_info.material_url
  //     var priceInfo = JSON.stringify({'goods_price': item.goods_info.goods_price, 'coupon_discount': item.goods_info.coupon_discount, 'goods_coupon_price': item.goods_info.goods_coupon_price})
  //     wx.navigateTo({
  //       url: '/pages/goods/goods/details-jd/index?skuId=' + skuId + '&priceInfo=' + priceInfo + '&materialUrl=' + materialUrl
  //     })
  //   }
  //   if (item.platform == 'pdd') {
  //     const goods_sign = item.goods_info.goods_id
  //     wx.navigateTo({
  //       url: '/pages/goods/goods/details-pdd/index?goods_sign=' + goods_sign,
  //     })
  //   }
  // },

   //底部触发
  onReachBottom: function () {
    // 页码自增
    this.setData({
      goods_list_tmp: [],
    })
    this.data.page_index += 1
    // 请求下一页数据
    console.log("--------------", this.data.page_index)
    this.get_goods_list()
  },

  onPullDownRefresh: function () {
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

  // 获取滚动条当前位置
  onPageScroll: function (e) {
    if (e.scrollTop > 100) {
      this.setData({
        floorstatus: true
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