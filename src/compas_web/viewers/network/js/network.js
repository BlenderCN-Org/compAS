"use strict";

/**
 * Representation of a network as an edge graph.
 *
 * @constructor
 */
function Network(config) {

    this._max_int_key = -1;
    this._max_int_fkey = -1;

    /** @member {Object} - Miscellaneous attributes of the network. */
    this.attributes = {
        'name'       : _.get(config, 'name', 'Network'),
        'viewport'   : _.get(config, 'viewport', {}),
        'vertexsize' : _.get(config, 'vertexsize', 5),
        'vertexcolor': _.get(config, 'vertexcolor', {})
    };

    /** @member {Object} - Default attributes of all vertices. */
    this.default_vertex_attributes = {'x': 0.0, 'y': 0.0};

    /** @member {Object} - Default attributes of all edges. */
    this.default_edge_attributes = {'q': 0.0, 'f': 0.0, 'l': 0.0, 'ind': false};

    /** @member {Object} - Default attributes of all faces, if any. */
    this.default_face_attributes = {};

    /** @member {Object} - The vertices of the network. */
    this.vertex = {};

    /** @member {Object} - the edges of the network. */
    this.edge = {};

    /** @member {Object} - The faces of the network. */
    this.face = {};

    /** @member {Object} - The halfedges of the network. */
    this.halfedge = {};
}


/**
 *
 */
Network.prototype.to_data = function() {
    return {
        '_max_in_key'               : this._max_int_key,
        '_max_in_fkey'              : this._max_int_fkey,
        'attributes'                : this.attributes,
        'default_vertex_attributes' : this.default_vertex_attributes,
        'default_edge_attributes'   : this.default_edge_attributes,
        'default_face_attributes'   : this.default_face_attributes,
        'vertex'                    : this.vertex,
        'edge'                      : this.edge,
        'face'                      : this.face,
        'halfedge'                  : this.halfedge
    };
};


/**
 *
 */
Network.prototype.clear = function() {
    this.vertex = {};
    this.edge = {};
    this.face = {};
    this.halfedge = {};
};


/**
 *
 */
Network.prototype.update_from_file = function(file) {

    var type, reader;
    var height = this.attributes['viewport']['height'];

    var self = this;

    if (! file) {
        return;
    }

    type = file.name.split('.').pop();
    reader = new FileReader();

    reader.onerror = function(event) { alert('File reading produced an error.'); };
    reader.onabort = function(event) { alert('File reading was aborted.'); };
    reader.onload  = function(event) {

        switch (type) {
            case 'obj':

                var obj, data;
                var index, key, xyz;
                var u, v;
                
                self.clear();

                obj = new OBJ(event.target.result);

                // replace this by obj.data, obj.text, obj.xxx
                obj.read();
                data = obj.parse();

                for (index in data['vertices']) {
                    xyz = data['vertices'][index];

                    self.add_vertex(index, {'x': xyz[0], 'y': xyz[1]});
                }

                for (index in data['curves']) {

                    u = data['curves'][index][0];
                    v = data['curves'][index][1];

                    self.add_edge(u, v);
                }

                // this is a bit of a hack
                // y = self.y();

                // ymin = d3.min(y);
                // ymax = d3.max(y);

                // for (key in self.vertex) {

                //  self.vertex[key]['y'] = -self.vertex[key]['y'] + (ymin + ymax);
                // }
                // -----------------------

                // this is another hack
                var scale;

                var x = self.x();
                var y = self.y();

                var xmin = d3.min(x);
                var xmax = d3.max(x);
                var ymin = d3.min(y);
                var ymax = d3.max(y);

                var width = self.attributes['viewport']['width'];
                var height = self.attributes['viewport']['height'];
                var padding = self.attributes['viewport']['padding'];

                var xspan = xmax - xmin;
                var yspan = ymax - ymin;

                if (xspan / width > yspan / height) {
                    scale = (width - 2 * padding) / xspan;
                }
                else {
                    scale = (height - 2 * padding) / yspan;
                }

                for (key in self.vertex) {

                    self.vertex[key]['x'] = (self.vertex[key]['x'] - xmin) * scale + padding;
                    self.vertex[key]['y'] = height + ((ymin - self.vertex[key]['y']) * scale - padding);
                }
                // --------------------

                self.draw();

            break;
            default:
            
                alert('Not a supported file type.');
        }

    };

    reader.readAsText(file);
}


/**
 *
 */
Network.prototype.update_from_data = function() {

};


/**
 * Process a given vertex key into something that the network understands.
 * @memberof Network
 * @method
 * @access protected
 * @param {number, string} - The key to process.
 */
Network.prototype._get_vertex_key = function(key) {
    var i;

    if (! key) {
        key = this._max_int_key = this._max_int_key + 1;
    }
    else {
        try {
            i = parseInt(key, 10);
            
            if (i > this._max_int_key) {
                this._max_int_key = i;
            }
        }
        catch (e) {
            //
        }
    }
    return key;
};


Network.prototype._get_face_key = function() {

};


Network.prototype.add_vertex = function(key, attr_obj) {
    var attr = {};
    var key = this._get_vertex_key(key);

    _.assign(attr, this.default_vertex_attributes, attr_obj);

    if (! this.vertex.hasOwnProperty(key)) {
        this.vertex[key] = {};
        this.edge[key] = {};
        this.halfedge[key] = {};    
    }

    _.assign(this.vertex[key], attr);

    return key;
};


Network.prototype.add_edge = function(u, v, attr_obj) {
    var attr = {};
    var u = u;
    var v = v;

    _.assign(attr, this.default_edge_attributes, attr_obj);

    if (! this.vertex.hasOwnProperty(u)) {
        u = this.add_vertex(u);
    }

    if (! this.vertex.hasOwnProperty(v)) {
        v = this.add_vertex(v);
    }

    if (! this.edge[u].hasOwnProperty(v)) {
        this.edge[u][v] = {};
    }

    _.assign(this.edge[u][v], attr);

    this.halfedge[u][v] = null;
    this.halfedge[v][u] = null;

    return [u, v];
};


Network.prototype.add_face = function() {};


Network.prototype.vertices = function(data=false) {
    var vertices = [];

    for (var key in this.vertex) {
        if (data) {
            vertices.push([key, this.vertex[key]]);
        }
        else {
            vertices.push(key);
        }
    }

    return vertices;
};


Network.prototype.edges = function(data=false) {
    var edges = [];

    for (var u in this.edge) {
        for (var v in this.edge[u]) {
            if (data) {
                edges.push([u, v, this.edge[u][v]]);
            }
            else {
                edges.push([u, v]);
            }
        }
    }

    return edges;
};


Network.prototype.faces = function() {};


Network.prototype.neighbours = function(key) {
    var nbrs = [];

    for (var nbr in this.halfedge[key]) {
        nbrs.push(nbr);
    }

    return nbrs;
};


Network.prototype.is_leaf = function(key) {

    return this.neighbours(key).length == 1;
};


Network.prototype.connected_edges = function(key) {
    var edges = [];
    var nbrs = this.neighbours(key);
    var nbr;
    var index;

    for (index in nbrs) {
        nbr = nbrs[index];

        if (key in this.edge && nbr in this.edge[key]) {
            edges.push([key, nbr]);
        }
        else {
            edges.push([nbr, key]);
        }
    }

    return edges;
};


Network.prototype.vertex_coordinates = function(key) {
    var xy = [];

    xy.push(this.vertex[key]['x']);
    xy.push(this.vertex[key]['y']);

    return xy;
};


Network.prototype.edge_length = function(u, v) {
    var a, b, l;

    a = this.vertex_coordinates(u);
    b = this.vertex_coordinates(v);

    return Math.sqrt(Math.pow(b[0] - a[0], 2) + Math.pow(b[1] - a[1], 2), Math.pow(b[2] - a[2], 2))
}


Network.prototype.x = function() {
    var x = [];

    for (var key in this.vertex) {
        x.push(this.vertex[key]['x']);
    }

    return x;
};


Network.prototype.y = function() {
    var y = [];
    var key;

    for (key in this.vertex) {
        y.push(this.vertex[key]['y']);
    }

    return y;
};


Network.prototype.xy = function() {
    var xy = [];
    var key;

    for (key in this.vertex) {
        xy.push([this.vertex[key]['x'], this.vertex[key]['y']]);
    }

    return xy;
};


Network.prototype.draw = function() {
    draw_network(this);
};


Network.prototype.display_vertex_keys = function(display) {
    display_network_vertex_keys(this, display);
};


Network.prototype.display_edge_indices = function(display) {
    display_network_edge_indices(this, display);
};


/**
 * Wrapper for call to WebService function.
 *
 */
Network.prototype.is_planar = function() {

    var idict = {
        'function': 'is_planar',
        'args'    : [this.to_data()],
        'kwargs'  : {}
    };

    $.ajax({
    
        data: JSON.stringify(idict)

    }).done(function(odict) {

        console.log(odict);

        if ('error' in odict && 'data' in odict) {

            if (odict['error']) {
                alert(odict['error']);
            }
            else {
                alert(odict['data']);
            }
        }

    });
};


/**
 *
 */
Network.prototype.shortest_path = function() {

    alert('Sorry, not implemented yet...');
};


/**
 *
 */
Network.prototype.dijkstra_path = function() {

    alert('Sorry, not implemented yet...');
};


/**
 *
 */
Network.prototype.vertex_coloring = function() {

    var idict = {
        'function': 'vertex_coloring',
        'args'    : [this.to_data()],
        'kwargs'  : {}
    };
    var self = this;

    $.ajax({
    
        data: JSON.stringify(idict)

    }).done(function(odict) {

        var key;
        var color;
        var colors = [
            tinycolor('red'),
            tinycolor('green'),
            tinycolor('blue'),
            tinycolor('yellow'),
            tinycolor('cyan'),
        ];

        console.log(odict);

        if ('error' in odict && 'data' in odict) {

            if (odict['error']) {
                alert(odict['error']);
            }
            else {

                for (key in odict['data']) {
                    color = odict['data'][key];

                    set_network_vertex_color(self, key, colors[color]);
                }
            }
        }

    });
};


/**
 *
 */
Network.prototype.smooth = function() {

    alert('Sorry, not implemented yet...');
};


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
