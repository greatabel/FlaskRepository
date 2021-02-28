(function( w ) {
    /*
     * constructor { Bird } 鸟构造函数
     * param { ctx: Context } 绘图环境
     * param { img: Image } 鸟图
     * param { widthFrame: number } 一排的帧数
     * param { heightFrame: number } 一列的帧数
     * param { x: number } 鸟的起始x轴坐标
     * param { y: number } 鸟的起始y轴坐标
     * */
    function Birds( ctx,birddown, birdmid, birdup, x, y ) {

        this.ctx = ctx;
        this.img= [birddown,birdmid,birdup]
        this.x = x;
        this.y = y;
        this.currentFrame = 0;
        // 一个小鸟的宽和高
        this.width = this.img[0].width;
        this.height = this.img[0].height;


        // 小鸟的下落速度
        this.speed = 0;

        // 加速度
        this.speedPlus = 0.2;

        // 上升时挥动翅膀
        this.up = false;
        //挥动翅膀的间隔
        this.t = 0
        this.tend=4
    }

    // 给原型扩展方法
    Birds.prototype = {

        constructor: Birds,

        // 绘制鸟
        draw: function() {

            // 当下落速度为1的时候，旋转10度
            //var baseRadian = Math.PI / 180 * 10;
            //var maxRadian = Math.PI / 180 * 45;

            // 根据速度计算旋转的弧度
            //var rotateRadian = baseRadian * this.speed;

            // 限制最大旋转角度为70度
            //rotateRadian = rotateRadian >= maxRadian? maxRadian : rotateRadian;

            this.ctx.save();

            /*
             * 1、平移到小鸟的中心点
             * 2、然后根据下落的速度旋转坐标系
             * 3、绘制小鸟，但是绘制的x和y坐标变为负的宽高一半。
             * */

            //this.ctx.rotate( rotateRadian );
            this.ctx.drawImage( this.img[this.currentFrame],this.x , parseInt(this.y));
            this.ctx.restore();
        },
        // 更新下一帧的数据
        update: function() {

            // 绘制下一帧
            if (++this.t == this.tend){
                this.t=0
                if (this.up){
                    this.currentFrame++
                    if (this.currentFrame> 2){
                        this.currentFrame = 0
                        this.up = false;
                    };
                }else{
                    
                    this.currentFrame = 0
                };
                
            }
            // 让小鸟不断下落
            this.y += this.speed;

            // 刷新下落数度
            this.speed += this.speedPlus;

        }
    }
    // 工厂模式
    w.getBirds = function(  ctx,birddown, birdmid, birdup, x, y) {
        return new Birds(  ctx,birddown, birdmid, birdup, x, y );
    };
}( window ));