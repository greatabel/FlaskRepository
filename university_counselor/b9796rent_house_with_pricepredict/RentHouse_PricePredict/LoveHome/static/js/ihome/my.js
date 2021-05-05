function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击推出按钮时执行的函数
function logout() {

    $.ajax({
        url: '/api/v1.0/session',
        type: 'delete',
        headers: {
            'X-CSRFTOKEN': getCookie('csrf_token')
        },
        success: function (resp) {
            location.href='/'
        }
    })
}

$(document).ready(function(){

    // 在页面加载完毕向后端查询用户的信息
    $.get('/api/v1.0/user', function (resp) {
        if (resp.errno == '0') {
            // 获取用户头像
            // $('#user-avatar').attr('src', resp.data.avatar_url)
            $('#user-avatar').attr('src', 'http://localhost:5000/static/images/head0.jpg')

            $('#user-name').html(resp.data.name)
            $('#user-mobile').html(resp.data.mobile)
        } else if(resp.errno == '4101'){  // 用户未登录时返回的错误状态码
            location.href = '/'
        }else {
            alert(resp.errmsg)
        }
    })
})
