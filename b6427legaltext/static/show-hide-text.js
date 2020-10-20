/*------------ Show / Hide Text ------------*/
function showHideText(sSelector, options) {
    // Def. options
    var defaults = {
        charQty     : 100,
        ellipseText : "...",
        moreText    : "更多",
        lessText    : "更少"
    };

    var settings = $.extend( {}, defaults, options );

    var s = this;

        s.container = $(sSelector);
        s.containerH = s.container.height();

        s.container.each(function() {
            var content = $(this).html();

            if(content.length > settings.charQty) {

                var visibleText = content.substr(0, settings.charQty);
                var hiddenText  = content.substr(settings.charQty, content.length - settings.charQty);

                var html = visibleText
                         + '<span class="moreellipses">' +
                           settings.ellipseText
                         + '</span><span class="morecontent"><span>' +
                           hiddenText
                         + '</span><a href="" class="morelink">' +
                           settings.moreText
                         + '</a></span>';

                $(this).html(html);
            }

        });

        s.showHide = function(event) {
            event.preventDefault();
            if($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(settings.moreText);

                $(this).prev().fadeToggle('fast', function() {
                    $(this).parent().prev().fadeIn();
                });
            } else {
                $(this).addClass("less");
                $(this).html(settings.lessText);

                $(this).parent().prev().hide();
                $(this).prev().fadeToggle('fast');
            }
        }

        $(".morelink").bind('click', s.showHide);
}
/*------------------------------------------*/
