
function showTimezone (data) {
    var myChart = echarts.init(document.getElementById('main2'));
    
    
    option = {
        title : {
            text: '各时区机场数量',
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (params){
                return "Timezone : " + params[0].name + '<br/>'
                    + params[0].seriesName + ' : ' + params[0].value + '<br/>'
            }
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : ['-12','-11','-10','-9','-8','-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8','9','10','11','12','13']
            }
        ],
        yAxis : [
            {
                type : 'value',
                boundaryGap: [0, 0.1]
            }
        ],
        series : [
            {
                name:'Number of Airports',
                type:'bar',
                stack: 'sum',
                barCategoryGap: '0%',
                itemStyle: {
                    normal: {
                        color: 'pink',
                        label : {
                            show: true, position: 'top'
                        }
                    }
                },
                data:data,
            },
            {
                name:'Number',
                type:'line',
                symbol: 'none',
                smooth: 0,
                color:['#66AEDE'],
                data:data,
            }
        ]
    };
    myChart.setOption(option)
}




function Longitude_Aatitude_Altitude (data, Acolor) {
    var myChart = echarts.init(document.getElementById('main1'));
    
 
    myChart.setOption({
        
        visualMap: {

            show: false,
            calculable: true,
            realtime: false,
            max: 3000,
            inRange: {
                color:['#a50026', '#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695']
            },
            outOfRange: {
                color: ["#ddd"]
            //     colorAlpha: 0
            },

            // type: 'piecewise', 
            // splitNumber:13, 
            // max: 2000,
            // inRange: {
            //     color: Acolor
            // },
            // outOfRange:{
            //     color: ["#ddd"]
            // }
        },
        tooltip: {
        },
        xAxis3D: {
            name: "经度",
            type: 'value',
        },
        yAxis3D: {
            name: "纬度",
            type: 'value',
        },
        zAxis3D: {
            name: "海拔",
            type: 'value',
        },
        grid3D: {
            axisLine: {
                lineStyle: {
                    color: '#000'
                }
            },
            axisPointer: {
                lineStyle: {
                    color: '#f00'
                },
                show: false
            },
            viewControl: {
//              autoRotate: true,//旋转展示
                projection: 'orthographic',
                beta: 10
            },
            boxWidth: 300,
            boxHeight: 200,
            boxDepth: 200,
            top: -100
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },

        series: [
        {
            name:'scatter',
            type: 'scatter3D',
            dimensions: ['Longtitude', 'Latitude', 'Altitude'//显示框信息
            ],
            data: data,
            symbolSize: 3.2,
            symbol: 'triangle',
            itemStyle: {
                borderWidth: 1,
                borderColor: 'rgba(255,255,255,0.8)'
            },
            emphasis: {
                itemStyle: {
                    color: '#ccc'
                }
            },
            itemStyle: {
                color: '#b0f'
            }
        }
    ],
        backgroundColor: "#fff"
    });
}


// ============================================================


function Airline_Country_Active(data){
    var myChart = echarts.init(document.getElementById('main3'));
    

    myChart.setOption({
        backgroundColor: "#ffffff",
        color: ["#FF9F7F", "#37A2DA"],
        legend: {
            data: ['non-Active', 'Active']
        },
        grid: {
            containLabel: true
        },
        xAxis: [{
            type: 'value'
        }],
        yAxis: [{
            type: 'category',
            axisTick: {
                show: false
            },
            data: data[0]
        }],
        series: [{
            name: 'Active',
            type: 'bar',
            stack: 'total',
            label: {
                normal: {
                    show: true,
                    position: 'right'
                }
            },
            data: data[1]
        }, {
            name: 'non-Active',
            type: 'bar',
            stack: 'total',
            label: {
                normal: {
                    show: true,
                    position: 'left'
                }
            },
            data: data[2]
        }]
    })
}