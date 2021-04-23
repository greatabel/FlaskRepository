function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0'){
            // 设置头像地址
            $('#user-avatar').attr('src', resp.data.avatar_url)
            // 设置昵称
            $('#user-name').val(resp.data.name)
        }else if(resp.errno == '4101'){  // 用户未登录时返回的错误状态码
            location.href = '/'
        }else {
            alert(resp.errmsg)
        }
    })

    // 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (e) {
        e.preventDefault()
        // 使用ajax模拟提交操作，会自动将表单中要提交的参数带上
        $(this).ajaxSubmit({
            url: '/api/v1.0/user/head_image',
            type: 'post',
            headers: {
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    // 显示头像
                    $('#user-avatar').attr('src', resp.data.avatar_url)
                }else if(resp.errno == '4101'){  // 用户未登录时返回的错误状态码
                    location.href = '/'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })

    // 管理用户名修改的逻辑
    $('#form-name').submit(function (e) {
        e.preventDefault()
        // 取用户输入的用户名
        var name = $('#user-name').val()
        if (!name){
            $('.error-msg').show()
            return
        }
        $('.error-msg').hide()
        // 定义用户提交的参数
        var params = {'name': name}
        $.ajax({
            url: '/api/v1.0/user/name',
            type: 'post',
            contentType: 'application/json',
            headers: {
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            data: JSON.stringify(params),
            success:function (resp) {
                if (resp.errno == '0'){
                    showSuccessMsg()
                }else if(resp.errno == '4101'){  // 用户未登录时返回的错误状态码
                    location.href = '/'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })

})

