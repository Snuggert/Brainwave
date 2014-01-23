'use strict';

$(function(){
    var data = new Array();
    $.each(brainwave.graphdata, function( key, value ) {
        data.push({
            label: key,
            color: '#'+Math.floor(Math.random()*16777215).toString(16),
            data: value
        });
    });
    var plot = $.plot(".chart_div", data,
    {
        series: {
            points: {
                show: true,
                fill: true,
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        },
        xaxis: {
            panRange: [brainwave.epoch_week_start, brainwave.epoch_week_end],
            zoomRange: [60 * 60 * 1000, brainwave.epoch_week_end - brainwave.epoch_week_start],
            min: brainwave.epoch_week_start,
            max: brainwave.epoch_week_end,
            mode: "time",
            timeformat: "%d/%m/%Y %H:%M"
        },
        yaxis: {
            min: 0.0,
            zoomRange: [10, 20],
            panRange: [0, 20],
        },
        zoom: {
            interactive: true
        },
        pan: {
            interactive: true
        } 
    });
    $("<div id='tooltip'></div>").css({
            border: "5px solid rgba(0, 0, 0, 0)",
            position: "absolute",
            display: "none",
            "background-color": "#19191A",
            color: "#E8E8E8",
            opacity: 0.8,
            "-webkit-border-radius": "5px",
            "-moz-border-radius": "5px",
            "border-radius": "5px",
    }).appendTo("body");

    $(".chart_div").bind("plothover", function (event, pos, item) {
        if (item) {
            var x = item.datapoint[0];
            var y = item.datapoint[1];

            var date = '<span class="date">' + new Date(x).toUTCString() + '</span>';
            var swatch = '<span class="detail_swatch" style="background-color: ' + item.series.color + '"></span>';
            var content = swatch + item.series.label + ": €" + y + '<br>' + date;

            $("#tooltip").html(content)
                .css({top: item.pageY-10, left: item.pageX+15})
                .fadeIn(200);
        } else {
            $("#tooltip").hide();
        }
    });
    $(".chart_div").unbind("plotclick");
    $(".chart_div").bind("plotclick", function (event, pos, item) {
        if(item) {
            console.log(item)
        }
    });
})