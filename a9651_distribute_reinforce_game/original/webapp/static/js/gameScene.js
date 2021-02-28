(function( w ) {
    /*
     * constructor { Scene } 游戏场景
     * param { ctx: Context } 绘图环境
     * param { imgObj: Object } 创建角色所需的图像资源
     * */
    function Scene( ctx, imgObj ) {

        this.ctx = ctx;
        this.imgObj = imgObj;

        // 听众队列
        this.listeners = [];

        // 该场景所需的所有角色
        this.backgraound = [];
        this.roles = [];
        this.other = [];
        this.pipe = []
        this.scose ;
        this.bird ;
        this._initRoles();
    }

    Scene.prototype = {

        constrcutor: Scene,

        // 创建场景所需的所有角色
        _initRoles: function() {

            this.birddown = [this.imgObj.birddown1,this.imgObj.birddown2,this.imgObj.birddown3,this.imgObj.birddown4,this.imgObj.birddown5]
            this.birdmid = [this.imgObj.birdmid1,this.imgObj.birdmid2,this.imgObj.birdmid3,this.imgObj.birdmid4,this.imgObj.birdmid5]
            this.birdup = [this.imgObj.birdup1,this.imgObj.birdup2,this.imgObj.birdup3,this.imgObj.birdup4,this.imgObj.birdup5]


            // 背景2个
            this.backgraound.push( getSky( this.ctx, this.imgObj.sky, 3 ) );
            this.backgraound.push( getSky( this.ctx, this.imgObj.sky, 3 ) );

            // 管道6个
            for ( var i = 0; i < 3; i++ ) {
                this.pipe.push( getPipe( this.ctx, this.imgObj.pipeDown, this.imgObj.pipeUp, 110, this.imgObj.land.height, 2 ) );
            }

            // 大地4个
            for ( var i = 0; i < 2; i++ ) {
                this.roles.push( getLand( this.ctx, this.imgObj.land, 3 ) );
            }

            // 创建鸟
            this.bird = getBird( this.ctx,  this.birddown[this.ctx.bird_id], this.birdmid[this.ctx.bird_id], this.birdup[this.ctx.bird_id],  57, 244 );

            // 其他鸟
            for ( var i = 0; i < 5; i++ ) {
                if (i!=this.ctx.bird_id){
                    this.other.push( getBirds( this.ctx, this.birddown[ i], this.birdmid[ i], this.birdup[ i],  57, 244 ) );
                }
            }
            //分数
            this.scose =  getScore( this.ctx,this.imgObj.zero,this.imgObj.one,this.imgObj.two,this.imgObj.three,this.imgObj.four,this.imgObj.five,this.imgObj.six,this.imgObj.seven,this.imgObj.eight,this.imgObj.nine);

        },

        // 添加听众
        addListener: function( listener ) {
            this.listeners.push( listener );
        },

        // 监听小鸟死亡
        triggerBirdOver: function() {
            // 死亡时告知所有的听众
            this.listeners.forEach( function( liste ) {
                liste();
            });
        },

        // 让所有的角色开始表演( 开始游戏 )
        draw: function() {
            var a=[""];
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
         
            // 每次绘制新的场景画面时，判断小鸟有没有碰撞，如果有，通知所有听众。
            var birdCoreX = this.bird.x + this.bird.width / 2;
            var birdCoreY = this.bird.y + this.bird.height / 2;

            // 如果小鸟撞向管道，或者飞出天空，或者duang~duang~duang，那么游戏结束
            if ( this.ctx.isPointInPath( birdCoreX-12, birdCoreY-9 )||this.ctx.isPointInPath( birdCoreX +12, birdCoreY-9)||this.ctx.isPointInPath( birdCoreX+12, birdCoreY+9)||this.ctx.isPointInPath( birdCoreX-12, birdCoreY+9)
                || birdCoreY < 0
                || birdCoreY > (this.ctx.canvas.height - this.imgObj.land.height-this.bird.height) ){
                // 监听到了小鸟死亡
                this.triggerBirdOver();
                return
            }
                    
            //获取上传图片base64
            var imgbase64 = this.ctx.cvs.toDataURL("image/jpeg",1);
            //图片大小改为80x80
            dealImage(imgbase64,80,80, function useImg(base64) {
                Ajax.post("img","base64="+base64+"&group_id="+this.ctx.group_id+"&bird_id="+this.ctx.bird_id+"&die_id="+6,function(data){})
                while (true){
                    var a = false;
                    Ajax.post("getact","group_id="+this.ctx.group_id+"&bird_id="+this.ctx.bird_id,function(data){
                        // console.log(data)
                        if(data=='false'){}else{
                            var jsarr=JSON.parse( data );
                            webdata = jsarr;
                            a = true;
                        }
                    })
                    if(a){
                        break;
                    }
                }
            });


            if (webdata[this.ctx.bird_id][0]==0 && webdata[this.ctx.bird_id][1]==1){
                this.bird.up = true;
                this.bird.speed = -2.5;
            }
            webdata.splice(this.ctx.bird_id,1)
            //分数
            this.scose.draw();
            //其他小鸟
            this.other.forEach( function( other,index ) {
                if (webdata[index][0]==0 ){
                    if(webdata[index][1]==1){
                        other.up = true;
                        other.speed = -2.5;
                    }
                    other.update();
                    other.draw( );
                }
            } );
        }

    };

    // 工厂
    w.getGameScene = function( ctx, imgObj ) {
        return new Scene( ctx, imgObj );
    }
}( window ));