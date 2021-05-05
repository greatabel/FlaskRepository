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

$(document).ready(function(){
    // 查询用户的实名认证信息
    $.get('/api/v1.0/user/auth', function (resp) {
        if (resp.errno == '0'){
            if (resp.data.real_name && resp.data.id_card){
                // 设置数据
                $('#real-name').val(resp.data.real_name)
                $('#id-card').val(resp.data.id_card)

                // 设置输入框不可用，并隐藏保存按钮
                $('#real-name').attr('disabled', true)
                $('#id-card').attr('disabled', true)
                $('.btn-success').hide()
            }

        }else if (resp.errno == '4101'){
            location.href = '/'
        }else{
            alert(resp.errmsg)
        }
        
    })


    // 管理实名信息表单的提交行为
    $('#form-auth').submit(function (e) {
        // 阻止默认提交
        e.preventDefault()
        // 取出表单中的值
        var real_name = $('#real-name').val()
        var id_card = $('#id-card').val()

        // 判断是否有值
        if (!(real_name && id_card)){
            $('.error-msg').show()
            return
        }
        $('.error-msg').hide()

        var params = {
            'real_name': real_name,
            'id_card': id_card
        }

        // 发起请求
        $.ajax({
            url: '/api/v1.0/user/auth',
            type: 'post',
            contentType: 'application/json',
            headers: {
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == '0'){
                    // 设置输入框不可用
                    $('#real-name').attr('disabled', true)
                    $('#id-card').attr('disabled', true)
                    // 隐藏保存按钮
                    $('.btn-success').hide()
                }else if (resp.errno == '4101'){
                    location.href ='/'
                }else{
                    alert(resp.errmsg)
                }
            }
        })

    })
})