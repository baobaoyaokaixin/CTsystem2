/*global $, document*/
$(document).ready(function () {

    'use strict';


    // ------------------------------------------------------- //
    // Charts Gradients
    // ------------------------------------------------------ //
    var ctx1 = $("canvas").get(0).getContext("2d");
    var gradient1 = ctx1.createLinearGradient(150, 0, 150, 300);
    gradient1.addColorStop(0, 'rgba(133, 180, 242, 0.91)');
    gradient1.addColorStop(1, 'rgba(255, 119, 119, 0.94)');

    var gradient2 = ctx1.createLinearGradient(146.000, 0.000, 154.000, 300.000);
    gradient2.addColorStop(0, 'rgba(104, 179, 112, 0.85)');
    gradient2.addColorStop(1, 'rgba(76, 162, 205, 0.85)');


    // ------------------------------------------------------- //
    // Line Chart
    // ------------------------------------------------------ //
    // var LINECHARTEXMPLE = $('#lineChartExample1');
    // var lineChartExample = new Chart(LINECHARTEXMPLE, {
    //     type: 'line',
    //     options: {
    //         legend: {labels: {fontColor: "#777", fontSize: 12}},
    //         scales: {
    //             xAxes: [{
    //                 display: true,
    //                 gridLines: {
    //                     color: '#eee'
    //                 }
    //             }],
    //             yAxes: [{
    //                 display: true,
    //                 gridLines: {
    //                     color: '#eee'
    //                 }
    //             }]
    //         },
    //     },
    //     data: {
    //         labels: ["January", "February", "March", "April", "May", "June", "July"],
    //         datasets: [
    //             {
    //                 label: "Data Set One",
    //                 fill: true,
    //                 lineTension: 0.3,
    //                 backgroundColor: gradient1,
    //                 borderColor: gradient1,
    //                 borderCapStyle: 'butt',
    //                 borderDash: [],
    //                 borderDashOffset: 0.0,
    //                 borderJoinStyle: 'miter',
    //                 borderWidth: 1,
    //                 pointBorderColor: gradient1,
    //                 pointBackgroundColor: "#fff",
    //                 pointBorderWidth: 1,
    //                 pointHoverRadius: 5,
    //                 pointHoverBackgroundColor: gradient1,
    //                 pointHoverBorderColor: "rgba(220,220,220,1)",
    //                 pointHoverBorderWidth: 2,
    //                 pointRadius: 1,
    //                 pointHitRadius: 10,
    //                 data: [30, 50, 40, 61, 42, 35, 40],
    //                 spanGaps: false
    //             },
    //             {
    //                 label: "Data Set Two",
    //                 fill: true,
    //                 lineTension: 0.3,
    //                 backgroundColor: gradient2,
    //                 borderColor: gradient2,
    //                 borderCapStyle: 'butt',
    //                 borderDash: [],
    //                 borderDashOffset: 0.0,
    //                 borderJoinStyle: 'miter',
    //                 borderWidth: 1,
    //                 pointBorderColor: gradient2,
    //                 pointBackgroundColor: "#fff",
    //                 pointBorderWidth: 1,
    //                 pointHoverRadius: 5,
    //                 pointHoverBackgroundColor: gradient2,
    //                 pointHoverBorderColor: "rgba(220,220,220,1)",
    //                 pointHoverBorderWidth: 2,
    //                 pointRadius: 1,
    //                 pointHitRadius: 10,
    //                 data: [50, 40, 50, 40, 45, 40, 30],
    //                 spanGaps: false
    //             }
    //         ]
    //     }
    // });

    var DOUGHNUTCHARTEXMPLE = $('#doughnutChartExample');
    $("#mgrid").change(function () {
        var mgrid = $(this).val();
        $.ajax({

            url: '/getReportline/',

            data: {"mgrid": $(this).val()},
            type: 'GET',
            dataType: 'json',


            success: function (data) {
                console.log(data);
                var totalCount = data['totalCount'];
                var pieChartExample = new Chart(DOUGHNUTCHARTEXMPLE, {
                    type: 'doughnut',
                    options: {

                        cutoutPercentage: 70,
                        tooltips: {

                            callbacks: {

                                label: function (tooltipItem, data) {

                                    var dataset = data.datasets[tooltipItem.datasetIndex];

                                    var total = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {

                                        return previousValue + currentValue;

                                    });

                                    var currentValue = dataset.data[tooltipItem.index];

                                    var precentage = Math.floor(((currentValue / total) * 100) + 0.5);

                                    return precentage + "%";

                                }

                            }

                        }
                    },
                    data: {
                        labels: [
                            "DataCenter", "Routing & Switching", "Collaboration/Voice", "CCDE", "Service Provider", "Security", "Wireless", "Enterprise Infrastructure"
                        ],
                        datasets: [
                            {

                                data: [data['classification']['CCIE-Data Center'], data['classification']['CCIE-Routing & Switching'], data['classification']['CCIE-Collaboration/Voice'], data['classification']['CCDE'], data['classification']['CCIE-Service Provider'], data['classification']['CCIE-Security'], data['classification']['CCIE-Wireless/Enterprise Wireless'], data['classification']['CCIE-Enterprise Infrastructure']],
                                borderWidth: 0,
                                backgroundColor: [
                                    '#3eb579',
                                    '#229954',
                                    "#45B39D",
                                    "#0E6251",
                                    "#54e69d",
                                    "#D1F2EB",
                                    "#71e9ad"
                                ],
                                hoverBackgroundColor: [
                                    '#3eb579',
                                    '#229954',
                                    "#45B39D",
                                    "#0E6251",
                                    "#54e69d",
                                    "#D1F2EB",
                                    "#71e9ad"
                                ]
                            }]
                    }
                });

                pieChartExample = {
                    responsive: true
                };
            },

        });
    })

    //
    // var LINECHART1 = $('#lineChartExample1');
    // var myLineChart = new Chart(LINECHART1, {
    //     type: 'line',
    //     options: {
    //         scales: {
    //             xAxes: [{
    //                 display: true,
    //                 gridLines: {
    //                     display: false
    //                 }
    //             }],
    //             yAxes: [{
    //                 ticks: {
    //                     max: 40,
    //                     min: 0,
    //                     stepSize: 0.5
    //                 },
    //                 display: false,
    //                 gridLines: {
    //                     display: false
    //                 }
    //             }]
    //         },
    //         legend: {
    //             display: false
    //         }
    //     },
    //     data: {
    //         labels: ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20"],
    //         datasets: [
    //             {
    //                 label: "Total Overdue",
    //                 fill: true,
    //                 lineTension: 0,
    //                 backgroundColor: "transparent",
    //                 borderColor: '#6ccef0',
    //                 pointBorderColor: '#59c2e6',
    //                 pointHoverBackgroundColor: '#59c2e6',
    //                 borderCapStyle: 'butt',
    //                 borderDash: [],
    //                 borderDashOffset: 0.0,
    //                 borderJoinStyle: 'miter',
    //                 borderWidth: 3,
    //                 pointBackgroundColor: "#59c2e6",
    //                 pointBorderWidth: 0,
    //                 pointHoverRadius: 4,
    //                 pointHoverBorderColor: "#fff",
    //                 pointHoverBorderWidth: 0,
    //                 pointRadius: 4,
    //                 pointHitRadius: 0,
    //                 data: [20, 28, 30, 22, 24, 10, 7],
    //                 spanGaps: false
    //             }
    //         ]
    //     }
    // });
    //
    // var LINECHART1 = $('#lineChartExample2');
    // var myLineChart = new Chart(LINECHART1, {
    //     type: 'line',
    //     options: {
    //         scales: {
    //             xAxes: [{
    //                 display: true,
    //                 gridLines: {
    //                     display: false,
    //                     color: '#eee'
    //                 }
    //             }],
    //             yAxes: [{
    //                 ticks: {
    //                     max: 40,
    //                     min: 0,
    //                     stepSize: 0.5
    //                 },
    //                 display: false,
    //                 gridLines: {
    //                     display: false
    //                 }
    //             }]
    //         },
    //         legend: {
    //             display: false
    //         }
    //     },
    //     data: {
    //         labels: ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20"],
    //         datasets: [
    //             {
    //                 label: "Total Overdue",
    //                 fill: true,
    //                 lineTension: 0,
    //                 backgroundColor: "transparent",
    //                 borderColor: '#ff7676',
    //                 pointBorderColor: '#ff7676',
    //                 pointHoverBackgroundColor: '#ff7676',
    //                 borderCapStyle: 'butt',
    //                 borderDash: [],
    //                 borderDashOffset: 0.0,
    //                 borderJoinStyle: 'miter',
    //                 borderWidth: 3,
    //                 pointBackgroundColor: "#ff7676",
    //                 pointBorderWidth: 0,
    //                 pointHoverRadius: 4,
    //                 pointHoverBorderColor: "#fff",
    //                 pointHoverBorderWidth: 0,
    //                 pointRadius: 4,
    //                 pointHitRadius: 0,
    //                 data: [20, 8, 30, 22, 24, 17, 20],
    //                 spanGaps: false
    //             }
    //         ]
    //     }
    // });

    var BARCHARTEXMPLE = $('#barChartExample');
    $("#mgrid").change(function () {
        var mgrid = $(this).val();
        console.log(BARCHARTEXMPLE);
        $.ajax({

            url: '/getReportline/',

            data: {"mgrid": $(this).val()},
            type: 'GET',
            dataType: 'json',


            success: function (data) {
                var totalCount = data['totalCount'];
                var barChartExample = new Chart(BARCHARTEXMPLE, {
                    type: 'bar',
                    options: {
                        hover: {
                animationDuration: 0
            },

            animation: {
                onComplete: function () {
                    var chartInstance = this.chart,
                        ctx = chartInstance.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                    ctx.fillStyle = "black";
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';

                    this.data.datasets.forEach(function (dataset, i) {
                        var meta = chartInstance.controller.getDatasetMeta(i);
                        meta.data.forEach(function (bar, index) {
                            var data = dataset.data[index];
                            ctx.fillText(data, bar._model.x, bar._model.y - 5);
                        });
                    });
                }
            },
                        scales: {
                            xAxes: [{
                                display: true,
                                gridLines: {
                                    color: '#eee'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                gridLines: {
                                    color: '#eee'
                                }
                            }]
                        },
                    },
                    data: {
                        labels: ["DC", "RS", "C/V", "CCDE", "ServPro", "Security", "Wireless", "EnIn"],
                        datasets: [
                            {
                                label: "CCIE Directions",
                                backgroundColor: [
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1
                                ],
                                hoverBackgroundColor: [
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1
                                ],
                                borderColor: [
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1,
                                    gradient1
                                ],
                                borderWidth: 1,
                                data: [data['classification']['CCIE-Data Center'], data['classification']['CCIE-Routing & Switching'], data['classification']['CCIE-Collaboration/Voice'], data['classification']['CCDE'], data['classification']['CCIE-Service Provider'], data['classification']['CCIE-Security'], data['classification']['CCIE-Wireless/Enterprise Wireless'], data['classification']['CCIE-Enterprise Infrastructure']],
                            },

                        ]
                    }
                });


            },

        });
    })



    var PIECHARTEXMPLE = $('#pieChartExample');
    $("#mgrid").change(function () {
        var mgrid = $(this).val();
        $.ajax({

            url: '/getReportline/',

            data: {"mgrid": $(this).val()},
            type: 'GET',
            dataType: 'json',


            success: function (data) {
                var LINECHART1 = $('#lineChartExample1');
    var myLineChart1 = new Chart(LINECHART1, {
        type: 'line',
        options: {
             hover: {
                animationDuration: 0
            },

            animation: {
                onComplete: function () {
                    var chartInstance = this.chart,

                        ctx = chartInstance.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                    ctx.fillStyle = "black";
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';

                    this.data.datasets.forEach(function (dataset, i) {
                        var meta = chartInstance.controller.getDatasetMeta(i);
                        meta.data.forEach(function (bar, index) {
                            var data = dataset.data[index];
                            ctx.fillText(data, bar._model.x, bar._model.y - 5);
                        });
                    });
                }
            },
            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: true
                    }
                }],
                yAxes: [{
                    ticks: {
                        max: 400,
                        min: 0,
                        stepSize: 25
                    },
                    display: true,
                    gridLines: {
                        display: true
                    }
                }]
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20"],
            datasets: [
                {
                    label: "Total Overdue",
                    fill: true,
                    lineTension: 0,
                    backgroundColor: "transparent",
                    borderColor: '#6ccef0',
                    pointBorderColor: '#59c2e6',
                    pointHoverBackgroundColor: '#59c2e6',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    borderWidth: 3,
                    pointBackgroundColor: "#59c2e6",
                    pointBorderWidth: 0,
                    pointHoverRadius: 4,
                    pointHoverBorderColor: "#fff",
                    pointHoverBorderWidth: 0,
                    pointRadius: 4,
                    pointHitRadius: 0,
                    data: [data['dateB']['2014'], data['dateB']['2015'], data['dateB']['2016'], data['dateB']['2014'], data['dateB']['2014'], data['dateB']['2014'], data['dateB']['2014']],
                    spanGaps: false
                }
            ]
        }
    });

    var LINECHART2 = $('#lineChartExample2');
    var myLineChart2 = new Chart(LINECHART2, {
        type: 'line',
        options: {
             hover: {
                animationDuration: 0
            },
            animation: {
                onComplete: function () {
                    var chartInstance = this.chart,

                        ctx = chartInstance.ctx;
                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                    ctx.fillStyle = "black";
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';

                    this.data.datasets.forEach(function (dataset, i) {
                        var meta = chartInstance.controller.getDatasetMeta(i);
                        meta.data.forEach(function (bar, index) {
                            var data = dataset.data[index];
                            ctx.fillText(data, bar._model.x, bar._model.y - 5);
                        });
                    });
                }
            },

            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: true,
                        color: '#eee'
                    }
                }],
                yAxes: [{
                    ticks: {
                        max: 400,
                        min: 0,
                        stepSize: 25
                    },
                    display: true,
                    gridLines: {
                        display: true
                    }
                }]
            },
            legend: {
                display: true
            }
        },
        data: {
            labels: ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20"],
            datasets: [
                {
                    label: "Total Overdue",
                    fill: true,
                    lineTension: 0,
                    backgroundColor: "transparent",
                    borderColor: '#ff7676',
                    pointBorderColor: '#ff7676',
                    pointHoverBackgroundColor: '#ff7676',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    borderWidth: 3,
                    pointBackgroundColor: "#ff7676",
                    pointBorderWidth: 0,
                    pointHoverRadius: 4,
                    pointHoverBorderColor: "#fff",
                    pointHoverBorderWidth: 0,
                    pointRadius: 4,
                    pointHitRadius: 0,
                    data: [data['dateR']['2014'], data['dateR']['2015'], data['dateR']['2016'], data['dateR']['2014'], data['dateR']['2014'], data['dateR']['2014'], data['dateR']['2014']],
                    spanGaps: false
                }
            ]
        }
    });
    myLineChart2 = {
                    responsive: true
                };
      myLineChart1 = {
                    responsive: true
                };




                var pieChartExample = new Chart(PIECHARTEXMPLE, {
                    type: 'pie',
                    option:{

                             events: false,
  animation: {
    duration: 500,
    easing: "easeOutQuart",
    onComplete: function () {
      var ctx = this.chart.ctx;
      ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontFamily, 'normal', Chart.defaults.global.defaultFontFamily);
      ctx.textAlign = 'center';
      ctx.textBaseline = 'bottom';
      ctx.fillStyle = 'black';
      this.data.datasets.forEach(function (dataset) {

        for (var i = 0; i < dataset.data.length; i++) {
            var model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model,
              total = dataset._meta[Object.keys(dataset._meta)[0]].total,
              mid_radius = model.innerRadius + (model.outerRadius - model.innerRadius)/2,
              start_angle = model.startAngle,
              end_angle = model.endAngle,
              mid_angle = start_angle + (end_angle - start_angle)/2;

          var x = mid_radius * Math.cos(mid_angle);
          var y = mid_radius * Math.sin(mid_angle);
          var percent = String(Math.round(dataset.data[i]/total*100)) + "%";
          if(dataset.data[i] != 0 && dataset._meta[0].data[i].hidden != true) {
            ctx.fillText(dataset.data[i], model.x + x, model.y + y);
            ctx.fillText(percent, model.x + x, model.y + y + 15);
          }
        }
      });
    }
  }
                    },
                    data: {
                        labels: [
                            "Single",
                            "Double",
                            "Triple",
                            "Quadruple",
                            "Quintuple",
                            "Sextuple",

                        ],
                        datasets: [
                            {
                                data: [data['countB']['Single'], data['countB']['Double'], data['countB']['Triple'], data['countB']['Quadruple'], data['countB']['Quintuple'], data['countB']['Sextuple']],
                                borderWidth: 0,
                                backgroundColor: [
                                    '#44b2d7',
                                    "#59c2e6",
                                    "#71d1f2",
                                    "#96e5ff",
                                    "#21618C",
                                    "#2471A3",
                                    "#A9CCE3"
                                ],
                                hoverBackgroundColor: [
                                    '#44b2d7',
                                    "#59c2e6",
                                    "#71d1f2",
                                    "#96e5ff",
                                    "#21618C",
                                    "#2471A3",
                                    "#A9CCE3"
                                ]
                            }]
                    }
                });

                pieChartExample = {
                    responsive: true
                };


            },

        });
    })


    var PIECHARTEXMPLE1 = $('#pieChartExample1');
   $("#mgrid").change(function () {
        var mgrid = $(this).val();
        $.ajax({

            url: '/getReportline/',

            data: {"mgrid": $(this).val()},
            type: 'GET',
            dataType: 'json',


            success: function (data) {



               var pieChartExample1 = new Chart(PIECHARTEXMPLE1, {
        type: 'pie',
        data: {
            labels: [
                "Single",
                "Double",
                "Triple",
                "Quadruple",
                "Quintuple",
                "Sextuple",

            ],
            datasets: [
                {
                    data: [data['countR']['Single'], data['countR']['Double'], data['countR']['Triple'], data['countR']['Quadruple'], data['countR']['Quintuple'], data['countR']['Sextuple']],
                    borderWidth: 0,
                    backgroundColor: [
                        "#F1948A",
                        "#E74C3C",
                        "#CB4335",
                        "#A93226",
                        "#E6B0AA",
                        "#943126",
                        "#922B21"
                    ],
                    hoverBackgroundColor: [
                        "#F1948A",
                        "#E74C3C",
                        "#CB4335",
                        "#A93226",
                        "#E6B0AA",
                        "#943126",
                        "#922B21"

                    ]
                }]
        }
    });

    var pieChartExample1 = {
        responsive: true
    };


            },

        });
    })




    // ------------------------------------------------------- //
    // Bar Chart 1
    // ------------------------------------------------------ //
    var BARCHART1 = $('#barChart1');
    var barChartHome = new Chart(BARCHART1, {
        type: 'bar',
        options:
            {
                scales:
                    {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }],
                    },
                legend: {
                    display: false
                }
            },
        data: {
            labels: ["A", "B", "C", "D", "E", "F", "G", "H"],
            datasets: [
                {
                    label: "Data Set 1",
                    backgroundColor: [
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7'
                    ],
                    borderColor: [
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7',
                        '#44b2d7'
                    ],
                    borderWidth: 0,
                    data: [35, 55, 65, 85, 30, 22, 18, 35]
                },
                {
                    label: "Data Set 1",
                    backgroundColor: [
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6'
                    ],
                    borderColor: [
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6',
                        '#59c2e6'
                    ],
                    borderWidth: 0,
                    data: [49, 68, 85, 40, 27, 35, 20, 25]
                }
            ]
        }
    });


    // ------------------------------------------------------- //
    // Bar Chart 2
    // ------------------------------------------------------ //
    var BARCHART2 = $('#barChart2');
    var barChartHome = new Chart(BARCHART2, {
        type: 'bar',
        options:
            {
                scales:
                    {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }],
                    },
                legend: {
                    display: false
                }
            },
        data: {
            labels: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
            datasets: [
                {
                    label: "Data Set 1",
                    backgroundColor: [
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d'
                    ],
                    borderColor: [
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d',
                        '#54e69d'
                    ],
                    borderWidth: 1,
                    data: [40, 33, 22, 28, 40, 25, 30, 40, 28, 27, 22, 15, 20, 24, 30]
                }
            ]
        }
    });


    // ------------------------------------------------------- //
    // Polar Chart
    // ------------------------------------------------------ //
    var POLARCHARTEXMPLE = $('#polarChartExample');
    var polarChartExample = new Chart(POLARCHARTEXMPLE, {
        type: 'polarArea',
        options: {
            elements: {
                arc: {
                    borderWidth: 0,
                    borderColor: '#aaa'
                }
            }
        },
        data: {
            datasets: [{
                data: [
                    11,
                    16,
                    12,
                    11,
                    7
                ],
                backgroundColor: [
                    "#e05f5f",
                    "#e96a6a",
                    "#ff7676",
                    "#ff8b8b",
                    "#fc9d9d"
                ],
                label: 'My dataset' // for legend
            }],
            labels: [
                "A",
                "B",
                "C",
                "D",
                "E"
            ]
        }
    });

    var polarChartExample = {
        responsive: true
    };


    // ------------------------------------------------------- //
    // Radar Chart
    // ------------------------------------------------------ //
    var RADARCHARTEXMPLE = $('#radarChartExample');
    var radarChartExample = new Chart(RADARCHARTEXMPLE, {
        type: 'radar',
        data: {
            labels: ["A", "B", "C", "D", "E", "C"],
            datasets: [
                {
                    label: "First dataset",
                    backgroundColor: "rgba(84, 230, 157, 0.4)",
                    borderWidth: 2,
                    borderColor: "rgba(75, 204, 140, 1)",
                    pointBackgroundColor: "rgba(75, 204, 140, 1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(75, 204, 140, 1)",
                    data: [65, 59, 90, 81, 56, 55]
                },
                {
                    label: "Second dataset",
                    backgroundColor: "rgba(255, 119, 119, 0.4)",
                    borderWidth: 2,
                    borderColor: "rgba(255, 119, 119, 1)",
                    pointBackgroundColor: "rgba(255, 119, 119, 1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(255, 119, 119, 1)",
                    data: [50, 60, 80, 45, 96, 70]
                }
            ]
        }
    });
    var radarChartExample = {
        responsive: true
    };


});
