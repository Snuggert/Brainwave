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
            lines: {
                show: true
            },
            points: {
                show: true
            }
        },
        grid: {
            hoverable: true,
            clickable: true
        },
        xaxis: {
            min: brainwave.epoch_week_start,
            max: brainwave.epoch_week_end,
            mode: "time",
            timeformat: "%d/%m/%Y"
        }
    });
     $(".chart_div").bind("plotclick", function (event, pos, item) {
        if(item) {
            console.log(item)
        }
    });
    $("<div id='tooltip'></div>").css({
            position: "absolute",
            display: "none",
            border: "1px solid #fdd",
            padding: "2px",
            "background-color": "#fee",
            opacity: 0.80
    }).appendTo("body");

    $(".chart_div").bind("plothover", function (event, pos, item) {
        var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
        $("#hoverdata").text(str);

        if (item) {
            var x = item.datapoint[0];
            var y = item.datapoint[1];

            var date = '<span class="date">' + new Date(x).toUTCString() + '</span>';
            var swatch = '<span class="detail_swatch" style="background-color: ' + item.series.color + '"></span>';
            var content = swatch + item.series.label + ": €" + y + '<br>' + date;

            $("#tooltip").html(content)
                .css({top: item.pageY+5, left: item.pageX+5})
                .fadeIn(200);
        } else {
            $("#tooltip").hide();
        }
    });
})