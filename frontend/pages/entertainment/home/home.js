// pages/entertainment/index/index.js

import time_tool from '../../utils/time_tool'
import produce_sign from '../../utils/produce_sign'


Page({

  /**
   * 页面的初始数据
   */
  data: {
    video_list: [],
    page_index:1,
    page_size:20,
    indexCurrent:null,
},
/**
 * {"video_url": "https://www.douyin.com/?recommend=1"},

{"video_url":"https://v26-web.douyinvod.com/7b0af8cdc67d94e2ada3aaae92d25fc0/6679b94d/video/tos/cn/tos-cn-ve-15/o4mec9gvbAQKSsVcgn9lOCBEDDAD8Aqf4gCIgR/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1184&bt=1184&cs=2&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iXWU9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=11&rc=OTdpOThoOTZnOTw8Zjk1OUBpM3g5Mzc6ZjozcDMzNGkzM0A2X2AuXmFhXjUxY18uM18tYSNlc3FjcjQwanNgLS1kLTBzcw%3D%3D&btag=80000e00008000&cquery=101r_100B_100x_100z_100o&dy_q=1719246116&feature_id=9bcd3da4752f92402ca306ab9cd46f9b&l=20240625002156E44BE522460E3221A243"},
{"video_url":"https://v3-web.douyinvod.com/182c4dbbac5a4c080712472b05e5d6cc/66795680/video/tos/cn/tos-cn-ve-15/osU7CQeG0Qee2tZDBJL6b3VfwE8AXIZXLgG5IA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1145&bt=1145&cs=0&ds=6&ft=LjhJEL998xHtu4kmD0P5XEhX.xiX-F0hxVJE-v4MgbPD-Ipz&mime_type=video_mp4&qs=12&rc=OTU8Njk4OWhlM2g7OjVpNkBpamQ0aXk5cml5czMzNGkzM0BgNC8zYV9hNS8xMGBjNTRiYSNyYWEtMmQ0am9gLS1kLWFzcw%3D%3D&btag=80000e00010000&cquery=100B_100x_100z_100o_100w&dy_q=1719220810&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=20240624172010D3760ACB723537025F0A"},
{"video_url":"https://v26-web.douyinvod.com/648e145e54500247f9e757027825994d/6679b6f8/video/tos/cn/tos-cn-ve-15c001-alinc2/oIj9DEg6QTmcvLASIBRVHCFHjaoOEAfDrGAfFY/?a=6383&ch=224&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=570&bt=570&cs=0&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iX2-9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=12&rc=aTM5NjlkMzk6PDhmNzw7M0BpMzZvdm85cnA2czMzNGkzM0AvMC4wLWItNi4xYS41NV8uYSNuY2NoMmQ0L2hgLS1kLS9zcw%3D%3D&btag=c0000e00008000&cquery=100x_100z_100o_101x_100B&dy_q=1719245516&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=20240625001155ED371111C4C959303339"},
{"video_url":"https://v3-web.douyinvod.com/6435d1098f80f1655fc61b1a4d3ddb0f/6679b80f/video/tos/cn/tos-cn-ve-15c001-alinc2/ocftXlAtxAQMeXr0gxszcCIacAEQZHKffaHIUe/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=288&bt=288&cs=2&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iX-A9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=11&rc=ZDdnZmY0OmQzNThoNzw8ZEBpamx5eG05cmhlczMzNGkzM0AvLTFfLmM0XzYxNC5jNjU1YSNqc3BxMmRrNm9gLS1kLS9zcw%3D%3D&btag=c0000e00028000&cquery=101r_100B_100x_100z_100o&dy_q=1719245706&feature_id=bde0a901f05c9d0ed10d2cb7dcdc4497&l=202406250015061BDCF5C7E1A85E2EBA42&__vid=7383287642412174627"},
{"video_url":"https://v3-web.douyinvod.com/6cf86a608a34fc73f09866cc131ffeb3/6679b85c/video/tos/cn/tos-cn-ve-15/oANBWYvAVJLDqxexPpL9zhf9APAFYsEmgIFE8M/?a=6383&br=687&bt=687&btag=c0000e00008000&cd=0%7C0%7C0%7C3&ch=224&cquery=100o_101x_100B_100x_100z&cr=3&cs=0&cv=1&dr=0&ds=6&dy_q=1719245873&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&ft=LjhJEL998xsnu40mo0P58lZW_3iXS59hxVJEhIaG2vPD-Ipz&is_ssr=1&l=20240625001751261B390E001ECC3001E8&lr=all&mime_type=video_mp4&qs=12&rc=ZzQ1OzczOTVlOmlkO2ZnNUBpamlpdXg5cnI8czMzNGkzM0BhMS80YF4yXzYxYjBgL2FjYSMvbG1sMmRjcmBgLS1kLWFzcw%3D%3D"},
{"video_url":"https://v3-web.douyinvod.com/6122673de44877875d2e74278939e265/6679b94c/video/tos/cn/tos-cn-ve-15/oIgCLEXgmAp2Zj04ADBmzNfYFgyQDIf9rAjMDq/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1088&bt=1088&cs=0&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iXdU9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=12&rc=Ojo7Nzs5Ojw8aDtkaDw3NkBpamszN3Y5cmdxczMzNGkzM0A2YS9jNmNfXzQxYmEuYDNhYSNuX2IwMmQ0bWRgLS1kLTBzcw%3D%3D&btag=c0000e00008000&cquery=100z_100o_101r_100B_100x&dy_q=1719246115&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=2024062500215486E289FAF4481F2FF884"},
{"video_url":"https://v3-web.douyinvod.com/b6f85505d1c8c4e7e123b1043b745e66/6679b950/video/tos/cn/tos-cn-ve-15c001-alinc2/oIQBIBZVAXLKkv9QwSiAElXwIFQZsW2EPPiOi/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=806&bt=806&cs=2&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iXdU9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=11&rc=ZzozOTg7ZGZlaDNlMzc4ZUBpanFyNXc5cjV1czMzNGkzM0A1Yy8zNjQzNi8xLzAuY2M0YSNfXnI1MmQ0Ll5gLS1kLTBzcw%3D%3D&btag=c0000e00008000&cquery=101r_100B_100x_100z_100o&dy_q=1719246115&feature_id=8129a1729e50e93a9e951d2e5fa96ae4&l=2024062500215486E289FAF4481F2FF884&__vid=7373994543982660916"},
{"video_url":"https://v3-web.douyinvod.com/9b899a61bcce1aedf964f68f615d96c2/6679b94c/video/tos/cn/tos-cn-ve-15/oAalD8nt9AAfjRXGf2DgqvBAsAxgyZG6HmbUFB/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1420&bt=1420&cs=2&ds=6&ft=LjhJEL998xsnu40mo0P58lZW_3iXdU9hxVJEhIaG2vPD-Ipz&mime_type=video_mp4&qs=11&rc=aGQ0N2U8Zjs5O2ZlNzY6N0Bpamt0cDk6Zmt0cjMzNGkzM0A0Yl5jYC1gXzAxMWJjYS40YSNebGlgcjRna2JgLS1kLTBzcw%3D%3D&btag=80000e00008000&cquery=100o_101r_100B_100x_100z&dy_q=1719246115&feature_id=9bcd3da4752f92402ca306ab9cd46f9b&l=20240625002155E44BE522460E3221A211&__vid=7358226152827145506"}
 
*/

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      video_list: []
    })
    this.get_video_list_p()
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
      video_list: [],
      page_index: 1
    })
    wx.pageScrollTo({
      scrollTop: 0
    })
    // 重新发起数据请求
    this.get_video_list_p()
    // 手动控制回弹
    wx.stopPullDownRefresh()
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    // 页码自增
    this.data.page_index += 1
    // 请求下一页数据
    this.get_video_list_p()
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },



  /**
   * 下面为自己添加的一些规函数
   */
  get_video_list_p: function (cb){
    var data_params =  {
      // 系统参数
      'appKey':'65b0bc2864fba',
      'version':'v1.0.0',
      // 业务参数
      'eliteId': 130,
      'pageIndex': this.data.page_index, 
      'pageSize': this.data.page_size,
    }
    data_params['signRan'] = produce_sign.dataoke_sign(data_params)
    console.log("test==============+++++++++", data_params)
    wx.request({
      url: 'https://openapiv2.dataoke.com/open-api/jd-jingfen-goods',
      method:'GET',
      header :{'Content-Type': 'application/json'},
      data : data_params,
      success: res => {
        const goods_list_ori = res.data.data.list
        const goods_list_deal = []
        console.log("test==000000000000000+++entertainment--", goods_list_ori[0])
        console.log("test==")
        for (var i in goods_list_ori) {
          const goods = goods_list_ori[i]
          // 过滤无优惠的内容
          const coupon_info = goods['couponInfo']['couponList']
          if (coupon_info.length == 0 || coupon_info[0]['discount'] < 5) {
            continue
          }
          goods_list_deal.push({'platform':'jd', 'goods_info': goods})
        }
        this.setData({
          video_list: [...this.data.video_list, ...goods_list_deal]
        }) 
        console.log("test=1111111111+++", this.data.video_list)
      },
    })
  },

  
  // get_video_list_p:function(p){
  //   // https://haokan.baidu.com/web/video/feed
  //   wx.request({
  //     url: 'https://haokan.baidu.com/web/video/feed',  
  //     method:'POST',
  //     header :{'content-type': 'application/json'},
  //     data: {
  //       "shuaxin_id":Date.parse(new Date()),
  //       'num': '30',
  //     },
  //     success: res => {
  //       console.log("test==============+++++++++", res.data.data)
  //       const vdieo_list_deal = res.data.data.response.videos
  //       this.setData({
  //         video_list: [...this.data.video_list, ...vdieo_list_deal]
  //       }) 
  //     }
  //   })
  // },


  // 获取视频列表信息
  get_video_list: function (cb){
    wx.request({
      url: 'https://85910d51p2.zicp.fun/entertainment/haokan_video',  
      // url: 'https://8f5910u512.vicp.fun/entertainment/haokan_video',  
      method:'POST',
      header :{'content-type': 'application/json'},
      data: {
        "user_id": "dkafa12e2j", 
        "page_index": this.data.page_index, 
        "page_size": this.data.page_size, 
        "sort_type": 0
      },
      success: res => {
        console.log("test==============+++++++++", res)
        const vdieo_list_deal = res.data.res
        this.setData({
          video_list: [...this.data.video_list, ...vdieo_list_deal]
        }) 
      }
    })
  },


  goto_video_detail_page:function (params) {
    const title = params.currentTarget.dataset.video_detail_home.goods_info.vskuName
    const play_url = params.currentTarget.dataset.video_detail_home.goods_info.videoInfo.videoList[0].playUrl

    const item = params.currentTarget.dataset.video_detail_home
    wx.navigateTo({
      url: '/pages/entertainment/details_single/index?title=' + title  + '&url=' +  play_url
    })

    // 如果是系列视频，则去系列视频，如果系列视频播放完则去哪个页面呢？
    // 如果是独立短视频，则去一个页面
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