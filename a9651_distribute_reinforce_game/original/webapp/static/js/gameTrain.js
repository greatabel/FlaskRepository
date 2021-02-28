(function( w ) {
    /*
     * constructor { Scene } 游戏场景
     * param { ctx: Context } 绘图环境
     * param { imgObj: Object } 创建角色所需的图像资源
     * */
    function Scene( ctx, imgObj ) {

        this.ctx = ctx;
        this.imgObj = imgObj;
        this._init();
        this._initRoles();
    }

    Scene.prototype = {

        constrcutor: Scene,
        // 初始化
        _init: function() {

            // 该场景所需的所有角色
            this.backgraound = [];
            this.roles = [];
            this.other = [];
            this.pipe = [];
            this.scose = null;
            this.bird = null;

        },
        // 创建场景所需的所有角色
        _initRoles: function() {

            // 背景2个
            for ( var i = 0; i < 3; i++ ) {
                this.backgraound.push( getSky( this.ctx, this.imgObj.sky, 3 ) );
            }


            // 管道6个
            for ( var i = 0; i < 3; i++ ) {
                this.pipe.push( getPipe( this.ctx, this.imgObj.pipeDown, this.imgObj.pipeUp, 100, this.imgObj.land.height, 2 ) );
            }

            // 大地4个
            for ( var i = 0; i < 2; i++ ) {
                this.roles.push( getLand( this.ctx, this.imgObj.land, 3 ) );
            }

            // 创建鸟
            this.bird = getBird( this.ctx,  this.imgObj.birddown, this.imgObj.birdmid, this.imgObj.birdup,  57, 244 );

            //分数
            this.scose =  getScore( this.ctx,this.imgObj.zero,this.imgObj.one,this.imgObj.two,this.imgObj.three,this.imgObj.four,this.imgObj.five,this.imgObj.six,this.imgObj.seven,this.imgObj.eight,this.imgObj.nine);

        },

        // 让所有的角色开始表演( 开始游戏 )
        draw: function() {
            this.ctx.reward = 0.1
            // 每次绘制新的场景画面时，判断小鸟有没有碰撞，如果有，通知所有听众。



            // 先清除上一次绘制的6个管道路径，
            // 然后再按照新的位置绘制新路径
            this.ctx.beginPath();
            this.backgraound.forEach( function( backgraound ) {
                backgraound.update();
                backgraound.draw();
            } );
            
            //管道
            this.pipe.forEach( function( pipe,index ) {
                pipe.random = webdata[5][index]
                pipe.update();
                pipe.draw( );
            } );
            
            //大地
            this.roles.forEach( function( role ) {
                role.update();
                role.draw();
            } );
            
            //小鸟
            this.bird.update();
            this.bird.draw();
            w = this.bird.width / 4;
            h = this.bird.height / 4;
            var birdCoreX1 = this.bird.x + w;
            var birdCoreY1 = this.bird.y + h;
            var birdCoreX2 = this.bird.x + w*3;
            var birdCoreY2 = this.bird.y + h;
            var birdCoreX3 = this.bird.x + w;
            var birdCoreY3 = this.bird.y + h*3;
            var birdCoreX4 = this.bird.x + w*3;
            var birdCoreY4 = this.bird.y + h*3;
            // 如果小鸟撞向管道，或者飞出天空，或者duang~duang~duang，那么游戏结束
            if ( this.ctx.isPointInPath( birdCoreX1, birdCoreY1 ) || this.ctx.isPointInPath( birdCoreX2, birdCoreY2 ) || this.ctx.isPointInPath( birdCoreX3, birdCoreY3 ) || this.ctx.isPointInPath( birdCoreX4, birdCoreY4 )
                || birdCoreY3 < 0
                || birdCoreY1 > (this.ctx.canvas.height - this.imgObj.land.height) ){

                this.ctx.reward = -1;
                this.ctx.sorce = 0;
                this.bird.x = 57;
                this.bird.y = 244;
                this.pipe.forEach( function( pipe,index ) {
                    pipe.x = 200 + pipe.width * 2.5 * ( index  );
                } );
            }

            // 小鸟没有死亡，才继续绘制
            console.log(this.ctx.reward)
                
            //获取上传图片base64
            var imgbase64 = this.ctx.cvs.toDataURL("image/jpeg",1);
            //图片大小改为80x80
            dealImage(imgbase64,80,80, function useImg(base64) {
                Ajax.post("train","base64="+base64+"&reward="+this.ctx.reward,function(data){
                    var jsarr=JSON.parse( data );
                    webdata = jsarr;
                })
            });
            if (webdata[this.ctx.flag][0]==0 && webdata[this.ctx.flag][1]==1){
                this.bird.up = true;
                this.bird.speed = -2.5;
            }
            
            //分数
            this.scose.draw();

        }
    };

    // 工厂
    w.getGameScene = function( ctx, imgObj ) {
        return new Scene( ctx, imgObj );
    }
}( window ));