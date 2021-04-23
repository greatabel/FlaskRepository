function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = ""
var preImageCodeId = ""
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 生成图片的UUID（图片编号）
    imageCodeId = generateUUID()
    // 生成URL
    var url = '/api/v1.0/image_code?cur_id=' + imageCodeId + '&pre_id=' + preImageCodeId
    // 给图片验证码的img标签设置URL
    $('.image-code>img').attr('src', url)
    // 记录当前这一次的图片编码，以便下一次请求时使用
    preImageCodeId = imageCodeId
}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    var params = {
        'mobile': mobile,
        'image_code': imageCode,
        'imageCode_id': imageCodeId
    }

    $.ajax({
        url: '/api/v1.0/sms_code',
        type: 'post',
        data: JSON.stringify(params),
        headers:{
            'X-CSRFTOKEN': getCookie('csrf_token')
        },
        contentType: 'application/json',
        success: function (resp) {
            if (resp.errno == '0'){
                // 表示发送成功，进入倒计时
                var num = 60
                var t = setInterval(function () {
                    if (num == 0){
                        // 表示倒计时完成,清除定时器
                        clearInterval(t)
                        // 重置验证码
                        $(".phonecode-a").html('获取验证码')
                        // 把点击事件重新添加
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }else{
                        // 表示正在倒计时，设置倒计时的秒数
                        $(".phonecode-a").html(num + '秒')
                    }
                    num = num - 1
                }, 1000)
            }else {
                // 添加点击事件
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
                // 重新生成图片验证码
                generateImageCode()
                alert(resp.errmsg)
            }
        }
    })


}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // 注册的提交(判断参数是否为空)
    $('.form-register').submit(function (e) {
        // 组织默认的提交操作
        e.preventDefault()
        // 取值
        var mobile = $('#mobile').val()
        var phonecode = $('#phonecode').val()
        var password = $('#password').val()
        var password2 = $('#password2').val()

        if (!mobile){
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return
        }
        // if (!phonecode){
        //     $("#phone-code-err span").html("请填写短信验证码！");
        //     $("#phone-code-err").show();
        //     return
        // }
        if (!password){
            $("#password-err span").html("请填写密码！");
            $("#password-err").show();
            return
        }
        if (password2 != password){
            $("#password2-err span").html("两次密码不一致");
            $("#password2-err").show();
            return
        }
        var params = {
            'mobile': mobile,
            'phonecode': phonecode,
            'password': password
        }
        $.ajax({
            url: '/api/v1.0/users',
            type: 'post',
            data: JSON.stringify(params),
            headers:{
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            contentType: 'application/json',
            success: function (resp) {
                if (resp.errno == '0'){ // 注册成功,进入主页
                    location.href = '/'
                }else {
                    $("#password2-err span").html(resp.errmsg);
                    $("#password2-err").show();
                }
            }
        })
    })

})
