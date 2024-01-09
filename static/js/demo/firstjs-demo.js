$(function () {

    // var radarData = {
    //     labels: ["Частота", "Ядра", "Техпроцесс", "TDP"],
    //     datasets: [
    //         {
    //             label: "Байкал",
    //             backgroundColor: "rgba(220,220,220,0.2)",
    //             borderColor: "rgba(220,220,220,1)",
    //             data: [15, 8, 20, 30]
    //         },
    //         {
    //             label: "Эльбрус",
    //             backgroundColor: "rgba(26,179,148,0.2)",
    //             borderColor: "rgba(26,179,148,1)",
    //             data: [30, 8, 28, 80]
    //         }
    //     ]
    // };

    // var radarOptions = {
    //     responsive: true
    // };

    // var ctx1 = document.getElementById("radarChart1").getContext("2d");
    // new Chart(ctx1, {type: 'radar', data: radarData, options:radarOptions});

    var barData = {
        labels: ["CoreMark[Coremarks]", "Dhrystone[VAX Dryhstones]", "Dhrystone[Dhrystones per Second]", "Whetstone[MWIPS]", "STREAM[Copy, MBs]", "HPLinpack 2.3[HPL, GFLOPs]", "HPLinpack 2.3[PEAK, GFLOPs]", "Geekbench 5[Geekbench 5 Score]", "7-Zip benchmark[Compress, MIPS]", "7-Zip benchmark[Decompress, MIPS]", "SPEC CPU 2006[CPU2006int]", "SPEC CPU 2006[CPU2006fp]", "SPEC CPU 2017[CPU2017int]", "SPEC CPU 2017[CPU2017fp]", "Stokfish[Nodes Per Second]", "RAMSpeedSMP 3.5.0[MB/s]", "OpenSSL 1.1.1[sign/s]", "C-Ray 1.1.1[Seconds]"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [6.47292, 6.41661, 1.127397973, 2.25078, 8.1787, 2.946, 3.84, 1.4246, 7.5178, 1.08733, 4.594, 4.859, 8.4, 7.62, 4.3097684, 3.0596, 1.526, 3.29]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [7.56132, 5.69265, 1.167785421, 2.02767, 7.9816, 3.00, 4.00, 1.4000, 7.4000, 1.09563, 4.50, 4.765, 9.0, 7.5, 4.3378421, 3.4717, 1.556, 3.16]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx1 = document.getElementById("barChart1").getContext("2d");
    new Chart(ctx1, {type: 'bar', data: barData, options:barOptions});

    var barData = {
        labels: ["CoreMark[Coremarks]", "Dhrystone[VAX Dryhstones]", "Dhrystone[Dhrystones per Second]", "Whetstone[MWIPS]", "STREAM[Copy, MBs]", "HPLinpack 2.3[HPL, GFLOPs]", "HPLinpack 2.3[PEAK, GFLOPs]", "Geekbench 5[Geekbench 5 Score]", "7-Zip benchmark[Compress, MIPS]", "7-Zip benchmark[Decompress, MIPS]", "SPEC CPU 2006[CPU2006int]", "SPEC CPU 2006[CPU2006fp]", "SPEC CPU 2017[CPU2017int]", "SPEC CPU 2017[CPU2017fp]", "PHPBench[Score]", "PyBench[Milliseconds]"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [1.3540, 1.3410, 2.3561181, 4.702, 1.6568, 6.9, 4.00, 8, 4.05, 2.820, 2.443, 1.92, 2.15, 2.5, 4.3378421, 2.34867, 3.156]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [7.56132, 5.69265, 1.167785421, 2.02767, 7.9816, 3.00, 4.00, 1.4000, 7.4000, 1.09563, 4.50, 4.765, 9.0, 7.5, 4.3378421, 3.4717, 1.556, 3.16, 2.34867, 3.156]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx2 = document.getElementById("barChart2").getContext("2d");
    new Chart(ctx2, {type: 'bar', data: barData, options:barOptions});

    var barData = {
        labels: ["500.perlbench_r", "502.gcc_r", "505.mcf_r", "525.x264_r", "557.xz_r"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [93.6, 65.4, 38.6, 199.9, 50.3]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [98, 87.2, 40, 205.6, 86]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx3 = document.getElementById("barChart3").getContext("2d");
    new Chart(ctx3, {type: 'bar', data: barData, options:barOptions});

    var barData = {
        labels: ["500.perlbench_r", "502.gcc_r", "505.mcf_r", "525.x264_r", "557.xz_r"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [93.6, 65.4, 38.6, 199.9, 50.3]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [98, 87.2, 40, 205.6, 86]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx4 = document.getElementById("barChart4").getContext("2d");
    new Chart(ctx4, {type: 'bar', data: barData, options:barOptions});

    var barData = {
        labels: ["500.perlbench_r", "502.gcc_r", "505.mcf_r", "525.x264_r", "557.xz_r"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [93.6, 65.4, 38.6, 199.9, 50.3]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [98, 87.2, 40, 205.6, 86]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx5 = document.getElementById("barChart5").getContext("2d");
    new Chart(ctx5, {type: 'bar', data: barData, options:barOptions});

    var barData = {
        labels: ["500.perlbench_r", "502.gcc_r", "505.mcf_r", "525.x264_r", "557.xz_r"],
        datasets: [
            {
                label: "Байкал-М",
                backgroundColor: 'rgba(26, 179, 148, 1)',
                pointBorderColor: "#fff",
                data: [93.6, 65.4, 38.6, 199.9, 50.3]
            },
            {
                label: "Эльбрус",
                backgroundColor: 'rgba(35, 198, 200, 1)',
                borderColor: "rgba(35, 198, 200, 1.2)",
                pointBackgroundColor: "rgba(26,179,148,1)",
                pointBorderColor: "#fff",
                data: [98, 87.2, 40, 205.6, 86]
            }
        ]
    };

    var barOptions = {
        responsive: true
    };

    var ctx6 = document.getElementById("barChart6").getContext("2d");
    new Chart(ctx6, {type: 'bar', data: barData, options:barOptions});

});