"use strict";

/**
 * Representation of a network as an edge graph.
 *
 * @constructor
 */
function Network(attributes) {

	this._max_int_key = -1;
	this._max_int_fkey = -1;

	/** @member {Object} - Miscellaneous attributes of the network. */
	this.attributes = {
		'name'      : 'Network',
		'viewport'  : _.get(attributes, 'viewport', {}),
		'vertexsize': 7
	};

	/** @member {Object} - Configuation settings of the network. */
	this.settings = {};
	
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
            	var index, xyz;
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

                self.draw();

            break;
            default:
            
            	alert('Not a supported file type.');
        }

    };

    reader.readAsText(file);
}


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


Network.prototype.is_planar = function() {

	var data = this.to_data();

    $.ajax({

    	'data': JSON.stringify(data),

    }).done(function(output, status, xhr) {

    	console.log(output);

    });
};
