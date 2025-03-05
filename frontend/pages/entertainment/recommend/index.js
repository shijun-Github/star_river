//index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    q_videos: [], //视频
    q_videoIndex: 0, //视频index   0,1
    q_yjz: true, //是否允许预加载  false, true
    page_index:1,
    page_size:8,
    video_type:[0, 3, 10]  // '短剧类型：0-短剧 2-合集 3-影视剧 10-电影',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 隐藏
    wx.hideLoading()
    const url_pre = getApp().globalData.apiUrl
    wx.request({
      url: url_pre + 'video/recommend',
      // url: 'https://8f5910u512.vicp.fun/entertainment/haokan_video',
      method:'POST',
      header :{'content-type': 'application/json'},
      data: {
        "user_id": "dkafa12e2j",
        "page_index": this.data.page_index,
        "page_size": this.data.page_size,
        "video_type": this.data.video_type
      },
      success: res => {
        console.log("33333333333333333333333333", typeof(res), res)
        const vdieo_list_deal = res.data.res.data
        console.log("33333333333333333333333333", typeof(vdieo_list_deal), vdieo_list_deal)
        // var array = this.data.q_videos.concat(from_home_item).concat(vdieo_list_deal) //concat() 方法：用于连接两个或多个数组,并返回一个新数组
        var array = vdieo_list_deal
        this.setData({
          q_videos: array, //视频
          q_yjz: vdieo_list_deal.length < 3 ? false : true, //是否允许预加载
        })
      }
    })
  },


  //动态更新当前视频下标
  q_swiperBindchange: function (e) {
    console.log('当前视频下标：', e.detail.current)
    console.log('当前：', e.detail)
    this.setData({
      q_videoIndex: e.detail.current
    })
    // 当加载的视频还剩1个未被滑到时加载下一页
    if (this.data.q_videos.length - (e.detail.current + 1) == 1 && this.data.q_yjz) {
      this.q_yjzVideos() //预加载视频
    }
  },

  //预加载视频
  q_yjzVideos: function () {
    console.log('预加载视频')
    // 页码自增
    this.data.page_index += 1
    const url_pre = getApp().globalData.apiUrl
    wx.request({
      url: url_pre + 'video/recommend',
      // url: 'https://8f5910u512.vicp.fun/entertainment/haokan_video',
      method:'POST',
      header :{'content-type': 'application/json'},
      data: {
        "user_id": "dkafa12e2j",
        "page_index": this.data.page_index,
        "page_size": this.data.page_size,
        "video_type": this.data.video_type
      },
      success: res => {
        const vdieo_list_deal = res.data.res.data
        var array = this.data.q_videos.concat(vdieo_list_deal) //concat() 方法：用于连接两个或多个数组,并返回一个新数组
        console.log("array======", array)
        this.setData({
          q_videos: array, //视频
          q_yjz: vdieo_list_deal.length < 3 ? false : true, //是否允许预加载
        })
      }
    })
  },
})

