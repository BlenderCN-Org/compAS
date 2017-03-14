"use strict";


function OBJ(text) {
    this.text = text;

    this.vertices = [];

    this.points = [];
    this.lines = [];
    this.faces = [];

    this.curves = [];
};


OBJ.prototype.read = function() {

    var line, parts, head;
    var lines = this.text.split('\n');

    for (var i = 0; i < lines.length; i++) {
        
        line = lines[i];
        parts = line.split(' ');
        head = parts.shift();

        switch (head) {
            case 'v':

                this._read_vertex_coordinates(head, parts);

            break;
            case 'p':
            case 'l':
            case 'f':

                this._read_polygonal_geometry(head, parts);

            break;
            case 'curv':

                this._read_freeform_geometry(head, parts);

            break;
            default:

                continue;
        }
    }
};


OBJ.prototype.parse = function() {

    var index_key = {};
    var key_index = {};
    var index_index = {};
    var vertex = {};
    var xyz;
    var index;
    var key;

    var vertices = [];
    var points = [];
    var lines = [];
    var faces = [];
    var curves = [];

    // construct the index_key map
    // construct the vertex dict
    for (index in this.vertices) {
        xyz = this.vertices[index];
        key = geometric_key(xyz)
        index_key[index] = key;
        vertex[key] = xyz;
    }

    // construct the vertex coordinates array
    // construct the key_index map
    index = 0;
    for (key in vertex) {
        vertices.push(vertex[key]);
        key_index[key] = index;
        index++;
    }

    // construct the index_index map
    for (index in index_key) {
        key = index_key[index];
        index_index[index] = key_index[key];
    }

    // construct the points array
    for (index in this.points) {
        points.push(index_index[index]);
    }

    // construct the lines array
    for (index in this.lines) {
        lines.push([index_index[this.lines[index][0]], index_index[this.lines[index][1]]]);
    }

    // construct the faces array

    // construct the curves array
    for (index in this.curves) {
        curves.push([index_index[this.curves[index][0]], index_index[this.curves[index][1]]]);
    }

    return {'vertices': vertices,
            'points'  : points,
            'lines'   : lines,
            'faces'   : faces,
            'curves'  : curves};
};


OBJ.prototype._read_vertex_coordinates = function(head, tail) {

    this.vertices.push(tail.map(parseFloat))
};


OBJ.prototype._read_polygonal_geometry = function(head, tail) {

    switch (head) {

        case 'p':

            this.points.push(parseInt(tail[0]) - 1);

        break;
        case 'l':

            if (tail.length == 2) {

                this.lines.push([parseInt(tail[0]) - 1, parseInt(tail[1]) - 1]);
            }

        break;
        case 'f':

            //

        break;
        default:

            //
    }
};


OBJ.prototype._read_freeform_geometry = function(head, tail) {

    var u, v;

    for (var i = 2; i < tail.length - 1; i++) {

        u = parseInt(tail[i + 0]) - 1;
        v = parseInt(tail[i + 1]) - 1;

        this.curves.push([u, v]);
    }
};
