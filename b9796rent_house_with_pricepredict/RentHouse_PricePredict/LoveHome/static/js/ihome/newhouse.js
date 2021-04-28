function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // 在页面加载完毕之后获取区域信息
    $.get('/api/v1.0/areas', function (resp) {
        if (resp.errno == '0'){
            // for (var i=0; i<resp.data.length; i++){
            //     var aid = resp.data[i].aid
            //     var aname = resp.data[i].aname
            //     $('#area-id').append('<option value="' + aid + '">'+ aname +'</option>')
            // }
            // 通过模板生成要显示的HTML
            var html = template("areas-tmpl", {'areas': resp.data})
            // 设置到指定的标签里面
            // $('#area-id').html(html)
            // $('#lbl_predict').val("1000");
            // var predict = Math.floor(Math.random() *  1000);
            // $('#lbl_predict').html("<label >"+predict +"</label>");

        }else{
            alert(resp.errmsg)
        }
    })

 


    // 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (e) {
        // 阻止默认提交
        e.preventDefault()

        var params = {}
        // serializeArray() 会生成当前表单所需要提交的数据列表
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value
        })

        var facilities = []
        // 取到checkbox、取到选中的、取到name=facility
        // 遍历数据列表或对象数据用map
        // 遍历界面上的标签用each
        $(':checkbox:checked[name=facility]').each(function (index, x) {
            facilities[index] = x.value
        })
        params['facility'] = facilities
        // console.log(params)

        $.ajax({
            url: '/api/v1.0/houses',
            type: 'post',
            contentType: 'application/json',
            headers: {
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == '0'){
                    // 隐藏房屋基本信息的表单
                    $('#form-house-info').hide()
                    // 显示上传房屋图片的表单
                    $('#form-house-image').show()
                    // 设置图片表单中要上传房屋的id
                    $('#house-id').val(resp.data.house_id)
                }
            }
        })

    })

    // 处理图片表单的数据
    $('#form-house-image').submit(function (e) {
        // 阻止默认提交
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/api/v1.0/house/image',
            type: 'post',
            headers: {
                'X-CSRFTOKEN': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    // 将上传成功的图片显示在界面上
                    $('.house-image-cons').append('<img src="' + resp.data.image_url + '">')
                }else{
                    alert(resp.errmsg)
                }
            }
        })
        
    })

})