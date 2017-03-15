"use strict";

/**
 *
 *
 */
function create_svg(network) {

    var svg;

    var scale;

    var ratio_x;
    var ratio_y;

    var viewport = network.attributes['viewport']['element'];
    var width    = network.attributes['viewport']['width'];
    var height   = network.attributes['viewport']['height'];
    var name     = network.attributes['name'];

    var x = network.x();
    var y = network.y();

    var xmin = d3.min(x);
    var xmax = d3.max(x);
    var ymin = d3.min(y);
    var ymax = d3.max(y);

    var xspan = xmax - xmin;
    var yspan = ymax - ymin;

    viewport.selectAll('*').remove();

    svg = viewport.append('svg:svg')
        .attr('id', name)
        .attr('class', name)
        .attr('width', width)
        .attr('height', height)
        // .attr('viewBox', sprintf('%.3f, %.3f, %.3f, %.3f', xmin - 0.1 * xspan, ymin - 0.1 * yspan, xspan + 0.2 * xspan, yspan + 0.2 * yspan))
        .attr('viewBox', sprintf('%.3f, %.3f, %.3f, %.3f', 0, 0, width, height))
        .attr('preserveAspectRatio', 'xMidYMid meet');

    return svg;
}

/**
 * Draw a network in a viewport.
 * A viewport is a html element that serves as a container for the svg data.
 * Note that the svg element does not exist in the viewport, and if it does, it should be deleted.
 *
 * @param network {Network} - A javascript network object.
 * @param viewport {DOM element} - A(n empty) DOM element.
 * 
 */
function draw_network(network,
                      vertexlabel={},
                      vertexcolor={},
                      edgewidth={},
                      edgecolor={},
                      edgelabel={}) {

    var svg = create_svg(network);

    var name       = network.attributes['name'];
    var vertexsize = network.attributes['vertexsize'];

    var edges    = network.edges();
    var vertices = network.vertices();

    // add lines for the edges
    svg.append('svg:g')
        .attr('class', 'edges')
        .selectAll('line')
        .data(edges)
        .enter()
        .append('svg:line')
        .attr('class', 'edge')
        .attr('id', function(uv) { return name + '_edge_' + uv[0] + '-' + uv[1]; })
        .attr('x1', function(uv) { return network.vertex[uv[0]]['x']; })
        .attr('y1', function(uv) { return network.vertex[uv[0]]['y']; })
        .attr('x2', function(uv) { return network.vertex[uv[1]]['x']; })
        .attr('y2', function(uv) { return network.vertex[uv[1]]['y']; })
        .attr('stroke', '#222222')
        .attr('vector-effect', 'non-scaling-stroke');

    // add circles for the edges
    svg.append('svg:g')
        .attr('class', 'vertices')
        .selectAll('circle')
        .data(vertices)
        .enter()
        .append('svg:circle')
        .attr('class', 'vertex')
        .attr('id', function(key) { return name + '_vertex_' + key })
        .attr('cx', function(key) { return network.vertex[key]['x'] })
        .attr('cy', function(key) { return network.vertex[key]['y'] })
        .attr('r', vertexsize)
        .attr('stroke', function(key) { return (network.is_leaf(key) ? '#222222' : '#222222'); })
        .attr('vector-effect', 'non-scaling-stroke')
        .attr('fill', function(key) { return (network.is_leaf(key) ? '#aaaaaa' : '#ffffff'); })
        .on('mousedown', function() {

            var id = d3.event.target.id;
            var key = id.split('_').pop();
            var circle = d3.select(this);

            // add a mousemove listener to the containing svg element
            svg.on('mousemove', function() {

                var x, y;
                var to = d3.mouse(this);
                var edges = network.connected_edges(key);
                var index, uv, u, v, edge;

                x = to[0];
                y = to[1];

                circle.attr('cx', x)
                      .attr('cy', y);

                for (index in edges) {
                    uv = edges[index];

                    u = uv[0];
                    v = uv[1];

                    edge = d3.select(sprintf('#%s_edge_%i-%i', name, u, v));

                    if (u == key) {
                        edge.attr('x1', x);
                        edge.attr('y1', y);
                    }
                    else {
                        edge.attr('x2', x);
                        edge.attr('y2', y);
                    }
                }
            });

            // remove the listeners
            svg.on('mouseup', function() {

                // remove the listeners
                svg.on('mousemove', null)
                   .on('mouseup', null);

                // update the datastructure
                var x, y;
                var to = d3.mouse(this);

                x = to[0];
                y = to[1];

                network.vertex[key]['x'] = x;
                network.vertex[key]['y'] = y;
            });
        });
}


// function scaled_network_vertex_positions(network, width, height, padding=10) {

//     var pos = {};

//     var scale;

//     var key;

//     var x = network.x();
//     var y = network.y();

//     var xmin = d3.min(x);
//     var xmax = d3.max(x);
//     var ymin = d3.min(y);
//     var ymax = d3.max(y);

//     var xspan = xmax - xmin;
//     var yspan = ymax - ymin;

//     if (xspan / width > yspan / height) {
//         scale = (width - 2 * padding) / xspan;
//     }
//     else {
//         scale = (height - 2 * padding) / yspan;
//     }

//     for (key in network.vertex) {
//         pos[key] = {};

//         pos[key]['x'] = (network.vertex[key]['x'] - xmin) * scale + padding;
//         pos[key]['y'] = height + ((ymin - network.vertex[key]['y']) * scale - padding);
//     }

//     return pos;
// }

// function unscaled_network_vertex_positions(network, pos, width, height, padding=10) {

//     var unscaled = {};

//     var scale;

//     var key;

//     var x = network.x();
//     var y = network.y();

//     var xmin = d3.min(x);
//     var xmax = d3.max(x);
//     var ymin = d3.min(y);
//     var ymax = d3.max(y);

//     var xspan = xmax - xmin;
//     var yspan = ymax - ymin;

//     if (xspan / width > yspan / height) {
//         scale = (width - 2 * padding) / xspan;
//     }
//     else {
//         scale = (height - 2 * padding) / yspan;
//     }

//     for (key in network.vertex) {
//         unscaled[key] = {}; 

//         unscaled[key]['x'] = (pos[key]['x'] - padding) / scale + xmin;
//         unscaled[key]['y'] = (height - pos[key]['y'] - padding) / scale + ymin;
//     }

//     return unscaled;
// }


function display_network_vertex_keys(network, display) {

    var svg;

    var viewport = network.attributes['viewport']['element'];
    var name     = network.attributes['name'];

    var vertices = network.vertices();

    svg = viewport.select('#' + name);

    svg.select('g.vertexlabels').remove();

    if (! display) {
        return;
    }

    svg.append('svg:g')
        .attr('class', 'vertexlabels')
        .selectAll('text')
        .data(vertices)
        .enter()
        .append('svg:text')
        .attr('class', 'vlabel')
        .attr('x', function(key) { return network.vertex[key]['x']; })
        .attr('y', function(key) { return network.vertex[key]['y'] + 4; })
        .attr('vector-effect', 'non-scaling-stroke')
        .attr('fill', function(key) { 

            var color = tinycolor(d3.select('#' + name + '_vertex_' + key).attr('fill'));

            return (color.isLight() ? '#000000' : '#ffffff'); 
        })
        .text(function(key) { return key; });
}


function display_network_edge_indices(network, display) {

    var svg;

    var viewport = network.attributes['viewport']['element'];
    var name     = network.attributes['name'];

    var edges = network.edges();

    svg = viewport.select('#' + name);

    svg.select('g.edgelabels').remove();

    if (! display) {
        return;
    }
    
    svg.append('svg:g')
        .attr('class', 'edgelabels')
        .selectAll('text')
        .data(edges)
        .enter()
        .append('svg:text')
        .attr('class', 'elabel')
        .attr('x', function(uv) {

            var x1 = network.vertex[uv[0]]['x'];
            var x2 = network.vertex[uv[1]]['x'];

            return 0.5 * (x1 + x2);

        })
        .attr('y', function(uv) {

            var y1 = network.vertex[uv[0]]['y'];
            var y2 = network.vertex[uv[1]]['y'];

            return  0.5 * (y1 + y2);

        })
        .text(function(uv, index) { return index; });
}


function scale_network_vertices(network) {

    var svg;

    var viewport   = network.attributes['viewport']['element'];
    var name       = network.attributes['name'];
    var vertexsize = network.attributes['vertexsize'];

    svg = viewport.select('#' + name);

    svg.selectAll('circle.vertex').attr('r', vertexsize);
}


function set_network_vertex_color(network, key, color) {

    d3.select('#' + network.attributes['name'] + '_vertex_' + key)
      .attr('fill', tinycolor(color).toHexString());
}
