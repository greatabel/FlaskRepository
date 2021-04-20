// //压缩方法
// function dealImage(base64, w, callback) {
//     var newImage = new Image();
//     var quality = 0.6;    //压缩系数0-1之间
//     newImage.src = base64;
//     newImage.setAttribute("crossOrigin", 'Anonymous');	//url为外域时需要
//     var imgWidth, imgHeight;
//     newImage.onload = function () {
//         imgWidth = this.width;
//         imgHeight = this.height;
//         var canvas = document.createElement("canvas");
//         var ctx = canvas.getContext("2d");
//         if (Math.max(imgWidth, imgHeight) > w) {
//             if (imgWidth > imgHeight) {
//                 canvas.width = w;
//                 canvas.height = w * imgHeight / imgWidth;
//             } else {
//                 canvas.height = w;
//                 canvas.width = w * imgWidth / imgHeight;
//             }
//         } else {
//             canvas.width = imgWidth;
//             canvas.height = imgHeight;
//             quality = 0.6;
//         }
//         ctx.clearRect(0, 0, canvas.width, canvas.height);
//         ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
//         var base64 = canvas.toDataURL("image/jpeg", quality); //压缩语句
//         // 如想确保图片压缩到自己想要的尺寸,如要求在50-150kb之间，请加以下语句，quality初始值根据情况自定
//         // while (base64.length / 1024 > 150) {
//         // 	quality -= 0.01;
//         // 	base64 = canvas.toDataURL("image/jpeg", quality);
//         // }
//         // 防止最后一次压缩低于最低尺寸，只要quality递减合理，无需考虑
//         // while (base64.length / 1024 < 50) {
//         // 	quality += 0.001;
//         // 	base64 = canvas.toDataURL("image/jpeg", quality);
//         // }
//         callback(base64);//必须通过回调函数返回，否则无法及时拿到该值
//     }
// }
//压缩方法
function dealImage(base64, imgWidth, imgHeight,callback) {
    var newImage = new Image();
    newImage.src = base64;
    newImage.setAttribute("crossOrigin", 'Anonymous');	//url为外域时需要
    newImage.width = imgWidth;
    newImage.height = imgHeight;
    newImage.onload = function () {
        var canvas = document.createElement("canvas");
        var ctx = canvas.getContext("2d");
        canvas.width = this.width;
        canvas.height = this.height;
        ctx.drawImage(this, 0, 0, canvas.width, canvas.height);
        var base64 = canvas.toDataURL("image/jpeg",1); //压缩语句
        callback(base64);//必须通过回调函数返回，否则无法及时拿到该值
    }
}
var Ajax={
    get: function(url, fn) {
      // XMLHttpRequest对象用于在后台与服务器交换数据   
      var xhr = new XMLHttpRequest();            
      xhr.open('GET', url, false);
      xhr.onreadystatechange = function() {
        // readyState == 4说明请求已完成
        if (xhr.readyState == 4 && xhr.status == 200 || xhr.status == 304) { 
          // 从服务器获得数据 
          fn.call(this, xhr.responseText);  
        }
      };
      xhr.send();
    },
    // datat应为'a=a1&b=b1'这种字符串格式，在jq里如果data为对象会自动将对象转成这种字符串格式
    post: function (url, data, fn) {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", url, false);
      // 添加http头，发送信息至服务器时内容编码类型
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");  
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
          fn.call(this, xhr.responseText);
        }
      };
      console.log('utils.js data=', data);
      xhr.send(data);
    }
  }