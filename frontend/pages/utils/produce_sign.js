import md5 from './md5.js'

function sort_json(citys) {
  // citys 为JSON格式
  var obj = {}
  Object.keys(citys).sort().map(item => {
    obj[item] = citys[item]
  })
  return obj
}

// 生成PDD的签名
function pdd_sign (obj){
  // https://www.cnblogs.com/joe235/p/11065591.html
  var key = '1833b600ad4b6f03bebbad4a704e217dba3430b0';  // app_secret
  var timestamp = (Date.parse(new Date()))/1000;
  // var versionNumber = 'app-v1';
  // obj["versionNumber"] = versionNumber;
  obj["timestamp"] = timestamp;
  let { keys, values, entries } = Object;
  let dataArr = [];
  //obj的每个属性和值添加到数组
  for (let [key, value] of entries(obj)) {
    dataArr.push([key + value.toString()]);
  }
  var newStr = dataArr.sort().join(""); //数组排序并转化为字符串
  var sign = key + newStr + key;
  sign = md5.hex_md5(sign).toUpperCase(); //MD5加密并转为大写
  return sign;
}


// 生成jd的签名
function jd_sign (obj){
  // https://www.cnblogs.com/joe235/p/11065591.html
  // appkey：9e49cf64aba20ea1f35f6e8b1497d5cd
  var secretkey = 'd5501a870f9844aab8fde31cf35124cf';  // jd
  var key = secretkey;
  var timestamp = (Date.parse(new Date()))/1000;
  // var versionNumber = 'app-v1';
  // obj["versionNumber"] = versionNumber;
  // obj["timestamp"] = timestamp;
  let { keys, values, entries } = Object;
  let dataArr = [];
  //obj的每个属性和值添加到数组
  for (let [key, value] of entries(obj)) {
    dataArr.push([key + value.toString()]);
  }
  var newStr = dataArr.sort().join(""); //数组排序并转化为字符串
  var sign = key + newStr + key;
  sign = md5.hex_md5(sign).toUpperCase(); //MD5加密并转为大写
  return sign;
}


// 生成jd的签名
function dataoke_sign (obj){
  var secretkey = '2ae8b46c6b3655819cbc1ceab81341d1';  // 大淘客
  obj['key'] = secretkey;
  obj['nonce'] = Math.floor(Math.random() * 100000) + 300000;
  obj["timer"] = (Date.parse(new Date()));
  obj["timer"] 
  var sign = 'appKey='+obj['appKey'] + '&timer='+obj['timer'] + '&nonce='+obj['nonce'] + '&key='+obj['key']
  sign = md5.hex_md5(sign).toUpperCase(); //MD5加密并转为大写
  return sign;
}

module.exports =  {
  pdd_sign: pdd_sign,
  jd_sign: jd_sign,
  dataoke_sign: dataoke_sign,
  sort_json: sort_json
} 