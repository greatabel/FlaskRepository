(function( w ) {
    /*
     * constrcutor { Score } 分数场景
     * param { ctx: Context } 绘图环境
     * */
    function Score( ctx ,zero,one,two,three,four,five,six,seven,eight,nine) {
        this.ctx = ctx;
        this.img= [zero,one,two,three,four,five,six,seven,eight,nine];
        this.ctx.sorce = 0;
    }

    // 给原型扩充方法
    Score.prototype={
        constructor: Score,

        draw:function() {
            this.ctx.save();

            /*
            * 1、分数对应图片列表index
            * 2、分数转成字符串分开为个单数，对应2个图片
            * 3、根据下标绘制对应的分数图片
            * */
            var scorenum = String(this.ctx.sorce).split("");
            var Total = 0
            for(j = 0,len=scorenum.length; j < len; j++) {
                Total += this.img[scorenum[j]].width
            }
        
            var Xoffset = (this.ctx.canvas.width - Total) / 2;
        
            for(j = 0,len=scorenum.length; j < len; j++) {
        
                this.ctx.drawImage( this.img[scorenum[j]],Xoffset, this.ctx.canvas.height * 0.1 );
                Xoffset += this.img[scorenum[j]].width
            }
            this.ctx.restore();
        }
    };
    // 工厂
    w.getScore = function( ctx ,zero,one,two,three,four,five,six,seven,eight,nine) {
        return new Score( ctx,zero,one,two,three,four,five,six,seven,eight,nine );
    }
    
}( window ));