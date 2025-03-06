//index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    q_videos: [], //视频
    q_videoIndex: 0, //视频index   0,1
    q_yjz: true, //是否允许预加载  false, true
    page_index:0,
    page_size:800,
    video_type:[0, 3, 10],  // '短剧类型：0-短剧 2-合集 3-影视剧 10-电影',
    showEpisodePanel: false,  // 新增：控制选集面板显示
    swiperCurrent: 0,  // 新增：Swiper 当前项
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 隐藏
    wx.hideLoading()
    const url_pre = getApp().globalData.apiUrl
    console.log("detail_single 1111111111111111111", typeof(options), options)
    const item_info = JSON.parse(options.item_info)
    console.log("detail_single 2222222222222222222", typeof(item_info), item_info)
    wx.request({
      url: url_pre + '/video/search/func_get_video_series_info_by_item_id',
      // url: 'https://8f5910u512.vicp.fun/video/haokan_video',
      method:'POST',
      header :{'content-type': 'application/json'},
      data: {
        "user_id": "dkafa12e2j",
        "page_index": this.data.page_index,
        "page_size": this.data.page_size,
        "item_info": item_info
      },
      success: res => {
        const video_list_deal = res.data.res.data   // 内容中不要有空值，哪怕是在不用的key里面，容易报错
        console.log("detail_single  33333333333333333333333333", typeof(video_list_deal), video_list_deal)
        var array = this.data.q_videos.concat(video_list_deal) //concat() 方法：用于连接两个或多个数组,并返回一个新数组 .concat(item_list_demo)
        console.log("detail_single  4444444444444444444444444", typeof(array), array)
        this.setData({
          q_videos: array, //视频
        })
      }
    })
  },

  //动态更新当前视频下标
  q_swiperBindchange: function (e) {
    console.log('当前视频下标：', e.detail.current)
    console.log('当前：', e.detail)
    this.setData({
      q_videoIndex: e.detail.current,
    })
    // // 当加载的视频还剩1个未被滑到时加载下一页
    // if (this.data.q_videos.length - (e.detail.current + 1) == 1 && this.data.q_yjz) {
    //   this.q_yjzVideos() //预加载视频
    // }
  },

  // 切换面板（阻止冒泡）
  toggleEpisodePanel: function() {
      this.setData({
        showEpisodePanel: !this.data.showEpisodePanel,
        isVideoLoaded: true
      });
    },

  // 切换剧集（跳到你想看的某一集）
  selectEpisode: function(e) {
    const index = e.currentTarget.dataset.index;
    if (index < 0 || index >= this.data.q_videos.length) {
      wx.showToast({ title: '无效的剧集', icon: 'none' });
      return;
    }
    this.setData({
      q_videoIndex: index,
      swiperCurrent: index,  // 同步 Swiper 位置
      showEpisodePanel: false
    }, () => {
      // 确保视图更新后强制视频刷新
      const videoCtx = wx.createVideoContext('videoPlayer', this);
      videoCtx.seek(0);
      videoCtx.play();
    });
  },

  // 切换到下一集
  onVideoEnded: function() {
    const next_index = (this.data.q_videoIndex + 1)
    if (next_index < this.data.q_videos.length) {
      this.setData({
        q_videoIndex: next_index,
        swiperCurrent: next_index,  // 同步 Swiper 位置
      });
      this.videoContext = wx.createVideoContext('myVideo');  // 确保视图更新后强制视频刷新
      this.videoContext.play();
    } else {
      wx.showToast({ title: '全剧终', icon: 'success', duration: 5000});
    }
  },
})

