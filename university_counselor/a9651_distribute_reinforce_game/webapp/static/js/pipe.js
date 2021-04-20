(function( w ) {
    /*
     * 管道的特点：
     * 1、成对出现，所以x轴可以共享，但是y轴不共享
     * 2、上下管道之间的路径固定，可以由用户指定
     * 3、管道的高度是随机生成的，随机生成上管道的高度，下管道就可以计算了
     * 4、当管道走出画布，从右边出来时，高度需要重新随机生成
     * */

    /*
     * constructor { Pipe } 管道
     * param { ctx: Context } 绘图环境
     * param { imgDown：Image } 口朝下的管道，在画布的上面
     * param { imgUp：Image } 口朝上的管道，在画布的下面
     * param { space：number } 上下管道的间距
     * param { landHeight：number } 大地的高度
     * param { speed：number } 速度
     * */
    function Pipe( ctx, imgDown, imgUp, space, landHeight, speed ) {

        this.ctx = ctx;
        this.imgDown = imgDown;
        this.imgUp = imgUp;
        this.space = space;
        this.landHeight = landHeight;
        this.speed = speed;

        // 管道最小高度
        this.minHeight = 110;

        // 管道默认的宽高
        this.width = this.imgDown.width;
        this.height = this.imgDown.height;

        Pipe.len++;
        this.x = parseInt(300 + this.width * 2.8* ( Pipe.len - 1 ))-this.width;
        this.y = 0;
        this.random = randomh[Pipe.len-1];

        // 初始化管道的坐标
        this._init();
    }

    // 管道实例的数量
    Pipe.len = 0;

    // 扩展原型方法
    util.extend( Pipe.prototype, {

        // 初始化管道的坐标
        _init: function() {

            // 上面管道的y轴坐标 = 随机生成的高度 - 管道默认的高度
            this.downY = -this.random*10

            // 下面管道的y轴坐标 = 随机生成的高度 + 上下管道的间隔
            this.upY =430-this.random*10;
        },

        // 绘制管道
        draw: function() {
            this.ctx.drawImage( this.imgDown, this.x, this.downY );
            this.ctx.drawImage( this.imgUp, this.x, this.upY );
            this._drawPath();
        },

        // 根据管道的宽高和坐标绘制对应的路径
        _drawPath: function() {
            this.ctx.rect( this.x, this.downY, this.width, this.height );
            this.ctx.rect( this.x, this.upY, this.width, this.height );
        },

        // 更新下一帧的数据
        update: function() {

            this.x -= this.speed;

            // 管道走出画布，向右拼接，同时重新生成高度
            if ( this.x <= -this.width ) {
                this._init();
                this.x += parseInt(this.width * 2.8* Pipe.len);
            }

            if (81==this.x+this.width||this.x+this.width==82){
                this.ctx.sorce++;
                this.ctx.reward=1;
            }
        }

    } );

    // 工厂模式
    w.getPipe = function( ctx, imgDown, imgUp, space, landHeight, speed ) {
        return new Pipe( ctx, imgDown, imgUp, space, landHeight, speed );
    };
}( window ));
