//$(function() {
//    var barOptions = {
//        series: {
//            bars: {
//                show: true,
//                barWidth: 0.6,
//                fill: true,
//                fillColor: {
//                    colors: [{
//                        opacity: 0.8
//                    }, {
//                        opacity: 0.8
//                    }]
//                }
//            }
//        },
//        xaxis: {
//            tickDecimals: 0
//        },
//        colors: ["#1ab394"],
//        grid: {
//            color: "#999999",
//            hoverable: true,
//            clickable: true,
//            tickColor: "#D4D4D4",
//            borderWidth:0
//        },
//        legend: {
//            show: false
//        },
//        tooltip: true,
//        tooltipOpts: {
//            content: "x: %x, y: %y"
//        }
//    };
//    var barData = {
//        label: "bar",
//        data: [
//            [1, 40],
//            [2, 25],
//            [3, 19],
//            [4, 34],
//            [5, 32],
//            [6, 44]
//        ]
//    };
//    $.plot($("#flot-bar-chart"), [barData], barOptions);
//
//});