
Page({

  /**
   * 页面的初始数据
   */
  data: {
    video_info:{},
    video_list:[],
    page_index:1,
    page_size:8,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log("single==============+++++++++", options.id)
    this.get_single_video_info()
  },

  // 获取单个视频
  get_single_video_info: function (cb){
    const video_list_size = this.data.video_list.length
    console.log("video_list_size======", video_list_size)
    if (video_list_size > 0){
      this.setData({
        video_info: this.data.video_list[1]
      })
    } else {
      this.get_video_list()
    }
  },


  // 获取视频列表信息
  get_video_list: function (cb){
    wx.request({
      // url: 'https://85910d51p2.zicp.fun/video/haokan_video',
      url: 'https://8f5910u512.vicp.fun/video/haokan_video',
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
        console.log("vdieo_list_deal======", vdieo_list_deal)
        this.setData({
          video_list: [...this.data.video_list, ...vdieo_list_deal],
          video_info: vdieo_list_deal[0]
        }) 
        console.log("video_info: vdieo_list_deal[0]======", this.data.video_info)
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