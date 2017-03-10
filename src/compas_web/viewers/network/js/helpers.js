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
                      vertexsize=7,
                      vertexlabel={},
                      vertexcolor={},
                      edgewidth={},
                      edgecolor={},
                      edgelabel={}) {

    var svg;

    var viewport = network.attributes['viewport']['element'];
    var width    = network.attributes['viewport']['width'];
    var height   = network.attributes['viewport']['height'];
    var padding  = network.attributes['viewport']['padding'];
    var name     = network.attributes['name'];

    var edges    = network.edges();
    var vertices = network.vertices();

    var pos = scaled_network_vertex_positions(network, width, height, padding);

    viewport.selectAll('*').remove();

    svg = viewport.append('svg:svg')
        .attr('id', name)
        .attr('class', name)
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', sprintf('0, 0, %i, %i', width, height));

    // add lines for the edges
    svg.append('svg:g')
        .attr('class', 'edges')
        .selectAll('line')
        .data(edges)
        .enter()
        .append('svg:line')
        .attr('class', 'edge')
        .attr('id', function(uv) { return name + '_edge_' + uv[0] + '-' + uv[1]; })
        .attr('x1', function(uv) { return pos[uv[0]]['x']; })
        .attr('y1', function(uv) { return pos[uv[0]]['y']; })
        .attr('x2', function(uv) { return pos[uv[1]]['x']; })
        .attr('y2', function(uv) { return pos[uv[1]]['y']; });

    // add circles for the edges
    svg.append('svg:g')
        .attr('class', 'vertices')
        .selectAll('circle')
        .data(vertices)
        .enter()
        .append('svg:circle')
        .attr('class', 'vertex')
        .attr('id', function(key) { return name + '_vertex_' + key })
        .attr('cx', function(key) { return pos[key]['x'] })
        .attr('cy', function(key) { return pos[key]['y'] })
        .attr('r', vertexsize)
        .on('mousedown', function() {

            var id = d3.event.target.id;
            var key = id.split('_').pop();
            var circle = d3.select(this);

            // add a mousemove listener to the containing svg element
            svg.on('mousemove', function() {

                var to = d3.mouse(this);
                var edges = network.connected_edges(key);
                var index, uv, u, v, edge;

                circle.attr('cx', to[0])
                      .attr('cy', to[1]);

                for (index in edges) {
                    uv = edges[index];

                    u = uv[0];
                    v = uv[1];

                    edge = d3.select(sprintf('#%s_edge_%i-%i', name, u, v));

                    if (u == key) {
                        edge.attr('x1', to[0]);
                        edge.attr('y1', to[1]);
                    }
                    else {
                        edge.attr('x2', to[0]);
                        edge.attr('y2', to[1]);
                    }
                }
            });

            // remove the listeners
            svg.on('mouseup', function() {
                svg.on('mousemove', null)
                   .on('mouseup', null);
            });
        })
}


function scaled_network_vertex_positions(network, width, height, padding=10) {

    var scale;

    var x = network.x();
    var y = network.y();

    var xmin = d3.min(x);
    var xmax = d3.max(x);
    var ymin = d3.min(y);
    var ymax = d3.max(y);

    var xspan = xmax - xmin;
    var yspan = ymax - ymin;

    var pos = {};


    if (xspan / width > yspan / height) {
        scale = (width - 2 * padding) / xspan;
    }
    else {
        scale = (height - 2 * padding) / yspan;
    }

    for (key in network.vertex) {
        pos[key] = {};

        pos[key]['x'] = (network.vertex[key]['x'] - xmin) * scale + padding;
        pos[key]['y'] = height - ((network.vertex[key]['y'] - ymin) * scale + padding);
    }

    return pos;
}


// function display_network_edge_labels(network) {

//     var viewport = network.attributes['viewport']['element'];

//     d3.select('.edgelabels');
    
//     viewport.append('svg:g')
//         .attr('class', 'edgelabels')
//         .selectAll('text')
//         .data(edges)
//         .enter()
//         .append('svg:text')
//         .attr('class', 'elabel')
//         .attr('x', function(uv) {

//             var x1 = vertex[uv[0]]['x'];
//             var x2 = vertex[uv[1]]['x'];

//             return 0.5 * (x1 + x2);

//         })
//         .attr('y', function(uv) {

//             var y1 = vertex[uv[0]]['y'];
//             var y2 = vertex[uv[1]]['y'];

//             return  0.5 * (y1 + y2);

//         })
//         .text(function(uv, index) { return index; });
// }


// function display_network_vertex_labels() {

//     svg.append('svg:g')
//         .attr('class', 'vertexlabels')
//         .selectAll('text')
//         .data(vertices)
//         .enter()
//         .append('svg:text')
//         .attr('class', 'vlabel')
//         .attr('x', function(key) { return pos[key]['x']; })
//         .attr('y', function(key) { return pos[key]['y'] + 3; })
//         .text(function(key, index) { return index; });
// }
