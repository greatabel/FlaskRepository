function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // 获取该房屋的详细信息
    // 获取该房屋的详细信息
    $.get('/api/v1.0/houses/' + houseId, function (resp) {
        if (resp.errno == "0") {
            var html = template("house-image-tmpl", {"img_urls": resp.data.house.img_urls, "price": resp.data.house.price})
            $(".swiper-container").html(html)

            // 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            html = template("house-detail-tmpl", {"house": resp.data.house})
            $('.detail-con').html(html)

            // 判断当前登录用户是否是该房屋的房东，如果不是就显示预定按钮
            if (resp.data.user_id != resp.data.house.user_id){
                // 显示预定按钮
                $(".book-house").show()
                $(".book-house").attr("href", "/booking.html?hid=" + resp.data.house.hid)
            }
        }else{
            alert(resp.errmsg)
        }
    })
})