def mesh_from_diana(cls, filepath, dva=None, dfa=None, dea=None, **kwargs):
    with open(filepath, 'rb') as fh:
        in_coords = False
        in_elements = False
        coords = []
        elements = []
        for line in fh:
            line = line.strip()
            if line == "'COORDINATES'":
                in_coords = True
                in_elements = False
                continue
            if line == "'ELEMENTS'":
                in_elements = True
                in_coords = False
                continue
            if line == "'GROUPS'":
                break
            if line == "'LOADS'":
                break
            if in_coords:
                parts = line.split()
                if len(parts) != 4:
                    continue
                # key = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                coords.append((x, y, z))
            if in_elements:
                parts = line.split()
                if len(parts) < 8:
                    continue
                # key = parts[0]
                # etype = parts[1]
                vertices = [int(k) - 1 for k in parts[2:]]
                elements.append(vertices)
    return cls.from_vertices_and_faces(coords, elements, dva=dva, dfa=dfa, dea=dea, **kwargs)


def mesh_to_diana(mesh):
    # for u, v in mesh.edges():
    #     split_edge(mesh, u, v, t=0.5, allow_boundary=True)

    key_index = dict((key, index + 1) for index, key in mesh.vertices_enum())

    with open('../../data/thelord/versions/10x8/moreinfo.dat', 'wb+') as fh:
        fh.write("'COORDI' DI=3\n")
        for key, attr in mesh.vertices_iter(True):
            fh.write("{0:<5}".format(key_index[key]))
            fh.write("{0:>20.9e}  {1:>20.9e}  {2:>20.9e}\n".format(attr['x'], attr['y'], attr['z']))

        fh.write("'MATERI'\n")
        # name
        fh.write("{0:<5}".format(1))
        fh.write("{0:<7}".format('NAME'))
        fh.write("{0}\n".format('MASONRY'))
        # young
        fh.write("{0:<5}".format(''))
        fh.write("{0:<7}".format('YOUNG'))
        fh.write("{0:.9e}\n".format(3e+9))
        # poison
        fh.write("{0:<5}".format(''))
        fh.write("{0:<7}".format('POISON'))
        fh.write("{0:.9e}\n".format(2e-1))
        # densit
        fh.write("{0:<5}".format(''))
        fh.write("{0:<7}".format('DENSIT'))
        fh.write("{0:.9e}\n".format(1.9e+3))

        fh.write("'GEOMET'\n")
        # name
        fh.write("{0:<5}".format(1))
        fh.write("{0:<7}".format('NAME'))
        fh.write("{0}\n".format('SHELLS'))
        # thick
        fh.write("{0:<5}".format(''))
        fh.write("{0:<7}".format('THICK'))
        fh.write("{0:.9e}\n".format(0.1))

        fh.write("'DATA'\n")
        # name
        fh.write("{0:<5}".format(1))
        fh.write("{0:<7}".format('NAME'))
        fh.write("{0}\n".format('VAULT'))
        # ninteg
        fh.write("{0:<5}".format(''))
        fh.write("{0:<7}".format('NINTEG'))
        fh.write("{0} {1}\n".format(6, 5))

        fh.write("'ELEMEN'\n")
        fh.write("CONNEC\n")
        count = 1
        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey, ordered=True)
            v1 = key_index[vertices[0]]
            v2 = key_index[vertices[1]]
            v3 = key_index[vertices[2]]
            v4 = key_index[vertices[3]]
            v5 = key_index[vertices[4]]
            v6 = key_index[vertices[5]]
            fh.write("{0:<5}".format(count))
            fh.write("{0:<7}".format('CT30S'))
            fh.write("{0}  {1}  {2}  {3}  {4}  {5}\n".format(v1, v2, v3, v4, v5, v6))
            count += 1
        fh.write("MATERI 1\n")
        fh.write("GEOMET 1\n")
        fh.write("DATA 1\n")

        fh.write("'GROUPS'\n")
        fh.write("'SUPPOR'\n")
        fh.write("'LOADS'\n")

        fh.write("'DIRECTIONS'\n")

        fh.write("'END'\n")
