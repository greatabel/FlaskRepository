function c_delay (data) {
    var myChart = echarts.init(document.getElementById('main1'), 'vintage');

    
    option = {
        title : {
            text: '2018.08.23~2018.09.07各公司航班延误总数',
        },
        tooltip : {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
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
                data : [
                    '中国国航', 
                    '南方航空',
                    '夏威夷航空', 
                    '东方航空', 
                    '海南航空', 
                    '美国航空', 
                    '四川航空', 
                    '达美航空', 
                    '深圳航空', 
                    '厦门航空'
                ]
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
                name:'Number of Delay',
                type:'bar',
                stack: 'sum',
                barCategoryGap: '50%',
                itemStyle: {
                    normal: {
                        color: '#f0e',
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



// ===========================================================================

function d_delay (data) {
    var myChart = echarts.init(document.getElementById('main2'), 'vintage');

    option = {
        baseOption: {
            timeline: {
                // y: 0,
                axisType: 'category',
                // realtime: false,
                // loop: false,
                autoPlay: true,
                // currentIndex: 2,
                playInterval: 1000,
                // controlStyle: {
                //     position: 'left'
                // },
                data: [
                    "08.23",
                    "08.24",
                    "08.25",
                    "08.26",
                    "08.27",
                    "08.28",
                    "08.29",
                    "08.30",
                    "08.31",
                    "09.01",
                    "09.02",
                    "09.03",
                    "08.34",
                    "09.05",
                    "09.06",
                    "09.07"
                ]
            },
            tooltip: {},
            calculable : true,
            grid: {
                top: 80,
                bottom: 100
            },
            xAxis: [
                {   
                    'type':'category',
                    'axisLabel':{
                        'interval':0
                    },
                    //'date' : company,
                    'data':[
                        '中国国航', 
                        '南方航空',
                        '夏威夷航空公司', 
                        '东方航空', 
                        '海南航空', 
                        '美国航空', 
                        '四川航空', 
                        '达美航空公司', 
                        '深圳航空', 
                        '厦门航空'
                    ],
                    splitLine: {show: false}
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '延误班数',
                    max: 7
                }
            ],
            series: [
                {name: '延误', type: 'bar'}
            ]
        },
        options: [
            {   
                title: {text: '2020年8月23日'},
                
                series: [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200823']
                }]
            },
            {
                title : {text: '2020年8月24日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200824']
                }] 
            },
            {
                title : {text: '2020年8月25日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200825']
                }] 
            },
            {
                title : {text: '2020年8月26日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200826']
                }] 
            },
            {
                title : {text: '2020年8月27日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200827']
                }] 
            },
            {
                title : {text: '2020年8月28日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200828']
                }] 
            },
            {
                title : {text: '2020年8月29日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200829']
                }] 
            },
            {
                title : {text: '2020年8月30日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200830']
                }] 
            },
            {
                title : {text: '2020年8月31日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200831']
                }] 
            },
            {
                title : {text: '2020年9月01日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200901']
                }] 
            },
            {
                title : {text: '2020年9月02日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200902']
                }] 
            },
            {
                title : {text: '2020年9月03日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200903']
                }] 
            },
            {
                title : {text: '2020年9月04日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200904']
                }] 
            },
            {
                title : {text: '2020年9月05日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200905']
                }] 
            },
            {
                title : {text: '2020年9月06日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200906']
                }] 
            },
            {
                title : {text: '2020年9月07日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20200907']
                }] 
            }
        ]
    };
    myChart.setOption(option)
}

// ===========================================================================

function a_delay (data) {
    var myChart = echarts.init(document.getElementById('main3'), 'vintage');

    
    option = {
        title : {
            text: '2018.08.23~2018.09.07各时间段航班延误总数',
        },
        calculable : true,
        tooltip : {},
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
                axisLabel :{
                    'interval':0,
                    'rotate' : 45
                },
                data : [
                    '00:00',
                    '01:00', 
                    '02:00',
                    '03:00',
                    '04:00',
                    '05:00',
                    '06:00',
                    '07:00',
                    '08:00',
                    '09:00',
                    '10:00',
                    '11:00',
                    '12:00',
                    '13:00',
                    '14:00',
                    '15:00',
                    '16:00',
                    '17:00',
                    '18:00',
                    '19:00',
                    '20:00',
                    '21:00',
                    '22:00',
                    '23:00'
                ]
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
                name:'Number of Delay',
                type:'line',
                color:['#66AEDE'],
                data:data,
                itemStyle: {
                    normal: {
                        label : {
                            show: true, position: 'top'
                        }
                    }
                },
            }
        ]
    };
    myChart.setOption(option)
}




// ===========================================================================


function e_delay (data) {
    var myChart = echarts.init(document.getElementById('main4'), 'vintage');

    option = {
        baseOption: {
            timeline: {
                // y: 0,
                axisType: 'category',
                // realtime: false,
                // loop: false,
                autoPlay: true,
                // currentIndex: 2,
                playInterval: 2200,
                // controlStyle: {
                //     position: 'left'
                // },
                data: [
                    "08.23",
                    "08.24",
                    "08.25",
                    "08.26",
                    "08.27",
                    "08.28",
                    "08.29",
                    "08.30",
                    "08.31",
                    "09.01",
                    "09.02",
                    "09.03",
                    "08.34",
                    "09.05",
                    "09.06",
                    "09.07"
                ]
            },
            tooltip: {},
            calculable : true,
            grid: {
                top: 80,
                bottom: 100
            },
            xAxis: [
                {
                    'type':'category',
                    'axisLabel':{
                        'interval':0,
                        'rotate' : 45
                    },
                    //'date' : company,
                    'data':[
                        '00:00',
                        '01:00', 
                        '02:00',
                        '03:00',
                        '04:00',
                        '05:00',
                        '06:00',
                        '07:00',
                        '08:00',
                        '09:00',
                        '10:00',
                        '11:00',
                        '12:00',
                        '13:00',
                        '14:00',
                        '15:00',
                        '16:00',
                        '17:00',
                        '18:00',
                        '19:00',
                        '20:00',
                        '21:00',
                        '22:00',
                        '23:00'
                    ],
                    splitLine: {show: false}
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '延误班数',
                    max: 8
                }
            ],
            series: [{
                name: '延误', 
                type: 'line'
            }]
        },
        options: [
            {   
                title: {text: '2018年8月23日'},
                
                series: [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180823']
                }]
            },
            {
                title : {text: '2018年8月24日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180824']
                }] 
            },
            {
                title : {text: '2018年8月25日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180825']
                }] 
            },
            {
                title : {text: '2018年8月26日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180826']
                }] 
            },
            {
                title : {text: '2018年8月27日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180827']
                }] 
            },
            {
                title : {text: '2018年8月28日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180828']
                }] 
            },
            {
                title : {text: '2018年8月29日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180829']
                }] 
            },
            {
                title : {text: '2018年8月30日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180830']
                }] 
            },
            {
                title : {text: '2018年8月31日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180831']
                }] 
            },
            {
                title : {text: '2018年9月01日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180901']
                }] 
            },
            {
                title : {text: '2018年9月02日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180902']
                }] 
            },
            {
                title : {text: '2018年9月03日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180903']
                }] 
            },
            {
                title : {text: '2018年9月04日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180904']
                }] 
            },
            {
                title : {text: '2018年9月05日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180905']
                }] 
            },
            {
                title : {text: '2018年9月06日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180906']
                }] 
            },
            {
                title : {text: '2018年9月07日'},
                series : [{
                    itemStyle: {
                        normal: {
                            label : {
                                show: true, position: 'top'
                            }
                        }
                    },
                    data: data['20180907']
                }] 
            }
        ]
    };
    myChart.setOption(option)
}

