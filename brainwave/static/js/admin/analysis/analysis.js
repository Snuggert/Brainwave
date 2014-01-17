'use strict';

$(function(){
    var graph = new Rickshaw.Graph( {
            element: document.querySelector(".chart_div"),
            renderer: 'line',
            width: 580,
            height: 400,
            series: [{
                    color: 'steelblue',
                    data: brainwave.graphdata
            }]
    } );
    var axes = new Rickshaw.Graph.Axis.Time( { graph: graph } );
    graph.render();
    var hoverDetail = new Rickshaw.Graph.HoverDetail({
        graph: graph,
        formatter: function(series, x, y) {
            var date = '<span class="date">' + new Date(x * 1000).toUTCString() + '</span>';
            var swatch = '<span class="detail_swatch" style="background-color: ' + series.color + '"></span>';
            var content = swatch + series.name + ": " + y + '<br>' + date;
            return content;
        }
    }); 
})