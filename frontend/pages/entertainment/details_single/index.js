//index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    q_videos: [], //视频
    q_videoIndex: 0, //视频index
    q_yjz: false, //是否允许预加载
    page_index:20,
    page_size:3,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 隐藏
    wx.hideLoading()
    const from_home_item = [{
      "title": options.title,
      "url": options.url
    }]
    
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
        const vdieo_list_deal = res.data.res
        var array = this.data.q_videos.concat(from_home_item).concat(vdieo_list_deal) //concat() 方法：用于连接两个或多个数组,并返回一个新数组
        this.setData({
          q_videos: array, //视频
          q_yjz: vdieo_list_deal.length < 3 ? false : true, //是否允许预加载
        }) 
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  //动态更新当前视频下标
  q_swiperBindchange: function (e) {
    console.log('当前视频下标：', e.detail.current)
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
    // var videoList = [{
    //   id: '4',
    //   url: "http://sns-1255549670.cos.ap-guangzhou.myqcloud.com/tmp_b0855d9c92f6ce4cd91796e8b1ca39a78bca4d48f524bb06.mp4?0.27723747875520743",
    // }, {
    //   id: '5',
    //   url: "http://sns-1255549670.cos.ap-guangzhou.myqcloud.com/wx982ed8d3473ced2c.o6zAJs8Oghy9CSGBPJEdSoJABPEU.SZVa80OoOknW8750107432d93943f9ce930651ad5ffa.mp4?0.27723747875520743",
    // }]
    // console.log("videoList=========", videoList)
    // var array = this.data.q_videos.concat(videoList) //concat() 方法：用于连接两个或多个数组,并返回一个新数组
    // console.log("array=========", array)
    // this.setData({
    //   q_videos: array, //视频
    //   q_yjz: videoList.length < 3 ? false : true, //是否允许预加载
    // })
    // 页码自增
    this.data.page_index += 1
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
        const vdieo_list_deal = res.data.res
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

