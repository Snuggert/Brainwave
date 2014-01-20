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
            timeformat: "%Y/%m/%d"
        }
    }); 
})