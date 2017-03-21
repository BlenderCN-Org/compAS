/**
 *
 */
Network.prototype.forcelayout = function() {

    var svg;
    var simulation;

    var index, key, u, v, node, link;

    var name     = this.attributes['name'];
    var viewport = this.attributes['viewport']['element'];
    var width    = this.attributes['viewport']['width'];
    var height   = this.attributes['viewport']['height'];

    var nodes = [];
    var links = [];

    var key_index = {};

    var vertices = network.vertices();

    var svg = viewport.select('#' + name);
    var circles = svg.selectAll('.vertex');
    var lines = svg.selectAll('.edge');

    var self = this;

    index = 0;

    for (key in this.vertex) {
        node = {
            'x'    : this.vertex[key]['x'],
            'y'    : this.vertex[key]['y'],
            'index': index,
            'key'  : key,
        };

        if (key == 2) {
            node['fx'] = this.vertex[key]['x'];
            node['fy'] = this.vertex[key]['y'];
        }

        nodes.push(node);

        key_index[key] = index;

        index = index + 1;
    }

    for (u in this.edge) {
        for (v in this.edge[u]) {
            links.push({
                'source': key_index[u],
                'target': key_index[v],
                'u'     : u,
                'v'     : v
            });
        }
    }

    simulation = d3.forceSimulation(nodes)
        .force("charge", d3.forceManyBody().strength(function(d, i) {
            // if (d.key == 9 || d.key == 6) {
            //     return -1000;
            // }
            // return -1000;
            if (self.is_leaf(d.key)) {
                return -1000;
            }
            return -100;
        }))
        .force("link", d3.forceLink(links).distance(function(d, i) {

            return 1.1 * self.edge_length(d.u, d.v);

        }).iterations(200));


    simulation.on('tick', function() {

        nodes.forEach(function(node) {

            d3.select('#' + name + '_vertex_' + node['key'])
                .attr('cx', node['x'])
                .attr('cy', node['y']);
        });

        links.forEach(function(link) {
            d3.select('#' + name + '_edge_' + link['u'] + '-' + link['v'])
                .attr('x1', link['source']['x'])
                .attr('y1', link['source']['y'])
                .attr('x2', link['target']['x'])
                .attr('y2', link['target']['y']);
        });
    });
    

    simulation.on('end', function() {

        console.log('simulation end');

        nodes.forEach(function(node) {
            d3.select('#' + name + '_vertex_' + node['key'])
                .attr('cx', node['x'])
                .attr('cy', node['y']);
        });

        links.forEach(function(link) {
            d3.select('#' + name + '_edge_' + link['u'] + '-' + link['v'])
                .attr('x1', link['source']['x'])
                .attr('y1', link['source']['y'])
                .attr('x2', link['target']['x'])
                .attr('y2', link['target']['y']);
        });
    });
};
