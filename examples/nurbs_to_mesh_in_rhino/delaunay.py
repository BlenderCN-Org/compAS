
from brg.datastructures.mesh.mesh import Mesh

from brg.geometry.functions import centroid
from brg.geometry.functions import bounding_box
from brg.geometry.functions import distance
from brg.geometry.arithmetic import add_vectors
from brg.geometry.queries import is_point_in_polygon
from brg.geometry.queries import is_point_in_circle
import rhinoscriptsyntax as rs  


class DelaunayMesh(Mesh):
    def insert_vertex(self, fkey, xyz=None):
        """Insert a vertex in the specified face.
    
        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.
    
        Returns:
            str: The keys of the newly created faces.
    
        Raises:
            VelueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(x=x, y=y, z=z)
        for u, v in self.face[fkey].iteritems():
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        return fkeys,w
    
    
    
    
def swap_edge(mesh, u, v):
    """Replace an edge of the mesh by an edge connecting the opposite
    vertices of the adjacent faces.

    Parameters:
        u (str): The key of one of the vertices of the edge.
        v (str): The key of the other vertex of the edge.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbours.
        TriMeshError: If one of the half-edges does not exist.
    """
    # check legality of the swap
    # swapping on the boundary is not allowed
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]
    if fkey_uv is None or fkey_vu is None:
        return "yo 1"
    # swapping to a half-edge that already exists is not allowed
    o_uv = mesh.face[fkey_uv][v]
    o_vu = mesh.face[fkey_vu][u]
    if o_uv in mesh.halfedge[o_vu] and o_vu in mesh.halfedge[o_uv]:
        return "yo 2"
    # swapping between non-triangles is not allowed
    # this check is only necessary to make the algorithm applicable to
    # non-triangle meshes!
    # perhaps this is not necessary
    if len(mesh.face[fkey_uv]) != 3 or len(mesh.face[fkey_vu]) != 3:
        return "yo 3"
    # swap
    # delete the current half-edge
    del mesh.halfedge[u][v]
    del mesh.halfedge[v][u]
    # delete the adjacent faces
    del mesh.face[fkey_uv]
    del mesh.face[fkey_vu]
    # add the faces created by the swap
    fkey1 =  mesh.add_face([o_uv, o_vu, v])
    fkey2 =  mesh.add_face([o_vu, o_uv, u])
    return fkey1,fkey2



def draw_light(mesh,temp = True):
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    xyz = mesh.xyz
    faces = []
    for fkey in mesh.faces_iter():
        face = mesh.face_vertices(fkey,True)
        face.append(face[-1])
        faces.append([key_index[k] for k in face])
    guid = rs.AddMesh(xyz, faces) 
    if temp:
        rs.EnableRedraw(True)
        rs.EnableRedraw(False)
        rs.DeleteObject(guid)     

def super_triangle(coords):
    
    centpt = centroid(coords)
    bbpts = bounding_box(coords)
    dis = distance(bbpts[0], bbpts[2])
    dis = dis *300
    v1 = (0*dis,2*dis,0)
    v2 = (1.73205*dis,-1.0000000000001*dis,0)#due to numerical issues
    v3 = (-1.73205*dis,-1*dis,0)
    
    pt1 = add_vectors(centpt, v1)
    pt2 = add_vectors(centpt, v2)
    pt3 = add_vectors(centpt, v3)
    
    return (pt1,pt2,pt3)

def delaunay(points3d,outboundkeys=None,inboundkeyslist=None,constraintkeypairs=None):
    

    #delete all faces
    mesh = DelaunayMesh()
    points =[(point[0],point[1],0.0) for point in points3d]
#     for i,point in enumerate(points):
#         mesh.add_vertex(str(i),{'x' : point[0], 'y' : point[1], 'z' : point[2]})
     
    #create super triangle
    pt1,pt2,pt3 = super_triangle(points) 
    #add super triangle vertices to mesh (remember supertrikeys)
           
    mesh.add_vertex('0',{'x' : pt1[0], 'y' : pt1[1], 'z' : pt1[2]})
    mesh.add_vertex('1',{'x' : pt2[0], 'y' : pt2[1], 'z' : pt2[2]})
    mesh.add_vertex('2',{'x' : pt3[0], 'y' : pt3[1], 'z' : pt3[2]})
    mesh.add_face(['0','1','2'])   
    #print "super "+ str(superkeys)
    
    keys = mesh.vertices()
    
    #keyslen = float(len(keys))
    #iterate over keys (exclude supertrikeys)
    for i,pt in enumerate(points):
        #if key not in superkeys:
        #insert point
        
#         dictpt = mesh.vertex[key]
#         pt = (dictpt['x'],dictpt['y'])
        fkeys = mesh.faces()
        #if i%25==0: print str(int(i/keyslen*100))+" %"
        #check in which triangle this point falls
        for fkey in fkeys:
            #abc = mesh.face_coordinates(fkey) #This is slower
            #This is faster:
            keya,keyb,keyc = mesh.face_vertices(fkey)
            dicta = mesh.vertex[keya]
            a = [dicta['x'],dicta['y']]
            dictb = mesh.vertex[keyb]
            b = [dictb['x'],dictb['y']]
            dictc = mesh.vertex[keyc]
            c = [dictc['x'],dictc['y']]
            pt_2d = (pt[0],pt[1]) 
            if is_point_in_polygon([a,b,c],pt_2d):
                #generate 3 new triangles (faces) and delete surrounding triangle
                #newtris = mesh.insert_vertex_coordinates(fkey,key,pt)
                newtris,key = mesh.insert_vertex(fkey, xyz=pt)
                break

            

        while newtris:
            
            #print "newtris: "+ str(newtris)
            fkey = newtris.pop()
            #print "popped: "+ str(fkey)
            
            #get opposite_face
            keys = mesh.face_vertices(fkey,ordered=True)#-----------------------------------try later without ordered
            s = list(set(keys) - set([key]))
            u,v = s[0],s[1]
            fkey1 = mesh.halfedge[u][v]
            if fkey1 != fkey:
                fkey_op,u,v = fkey1,u,v
            else:
                fkey_op,u,v = mesh.halfedge[v][u],u,v
            
            
            
            #fkey_op,u,v = mesh.opposite_face(key,fkey)
            #print "u v: "+ u +" - " + v
            #print "opposite: "+ str(fkey_op)
            if fkey_op:  
                #if uv is a constaint edge -> don't swap edge
                flag = True
                if constraintkeypairs:
                    for pairs in constraintkeypairs:
                        if len(set([u,v]+pairs))==2:
                            flag = False
                            break
                if flag:
                    #fpts = mesh.face_coordinates(fkey_op)#This is slower
                    #This is faster:
                    keya,keyb,keyc = mesh.face_vertices(fkey_op)
                    dicta = mesh.vertex[keya]
                    a = [dicta['x']+0.000000001,dicta['y']-0.000000001]#avoid numerical issues for points on a line
                    dictb = mesh.vertex[keyb]
                    b = [dictb['x'],dictb['y']]
                    dictc = mesh.vertex[keyc]
                    c = [dictc['x'],dictc['y']]  
                                  
                    if is_point_in_circle(a,b,c,pt):              
                        #mesh.swap_edge(u, v)
                        fkey,fkey_op = swap_edge(mesh, u, v)
                        #print "swaped: "+ u +" - " + v
                        newtris.append(fkey)
                        newtris.append(fkey_op)  
                    
                        
    # Clean-up:
    # Delete faces adjacent to supertriangle                     
    for key in  ['0','1','2']:
        #mesh.delete_vertex(key) for future implementation
        mesh.remove_vertex(key)   
    draw_light(mesh,temp = False)
    
    
    # Delete faces outside of boundary
    if outboundkeys:
        poly=[]
        poly.append(mesh.vertex_coordinates(outboundkeys[-1]))#make it a closed poly
        for key in outboundkeys:
            poly.append(mesh.vertex_coordinates(key))
        for fkey in mesh.faces():
            cent = mesh.face_centroid(fkey)
            if not is_point_in_polygon(poly,cent):
                mesh.delete_face(fkey)

    # Delete faces inside of inside boundaries
    if inboundkeyslist:
        for inboundkeys in inboundkeyslist:
            poly=[]
            poly.append(mesh.vertex_coordinates(inboundkeys[-1]))#make it a closed poly
            for key in inboundkeys:
                poly.append(mesh.vertex_coordinates(key))                       
            for fkey in mesh.faces():
                cent = mesh.face_centroid(fkey)
                if is_point_in_polygon(poly,cent):
                    mesh.delete_face(fkey)               
 
    # Remesh area left and right to constraint edges
    if constraintkeypairs:
        #pairslen = float(len(constraintkeypairs))
        for i,constraintkeypair in enumerate(constraintkeypairs):
            
            pair0 = constraintkeypair[0]
            pair1 = constraintkeypair[1]
            vdict = mesh.vertex[pair0]
            pt0 = [vdict['x'],vdict['y']]  
            vdict = mesh.vertex[pair1]
            pt1 = [vdict['x'],vdict['y']]    

            
            #if i%25==0: print str(int(i/pairslen*100))+" %"
            xfkeys = []#all triangles which have intersecting edges with the constraint edge
            regionkeys = []#all vertices of the region
            for fkey in mesh.faces():
                keys = mesh.face_vertices(fkey)
                for i,key in enumerate(keys):
                    u = keys[i-1]
                    v = keys[i]
                    #don't accept intersection if the edges share a vertex
                    if u == pair0 or u == pair1:
                        continue
                    if v == pair0 or v == pair1:
                        continue
                                
                    vdict = mesh.vertex[u]
                    pt2 = [vdict['x'],vdict['y']]        
                    vdict = mesh.vertex[v]
                    pt3 = [vdict['x'],vdict['y']]                                      
            
                    #check if edges intersect
                    if are_edges_crossing([(0,1),(2,3)],[pt0,pt1,pt2,pt3]):
                        regionkeys = regionkeys + keys#all vertices of the region
                        xfkeys.append(fkey)#all triangles which have intersecting edges
                        break#if one edges of the triangle intersects -> break
                    
            #find boundary vertices for all intersecting triangles
            
            boundkeys = mesh.boundary_vertices_partly(xfkeys,constraintkeypair[0])
            # split boundary based on the start and end vertex of the
            if boundkeys:#check if boundkeys exists (does not exist if the constraint edge is already in the mesh
                ind = boundkeys.index(constraintkeypair[1])
                #boundary region 1
                boundkeys1=boundkeys[:ind+1]+[boundkeys[0]]#make it a closed poly
                #boundary region 2
                boundkeys2=boundkeys[ind:]+[boundkeys[0]]+[boundkeys[ind]]#make it a closed poly
                
                #check for any inner vertices in region
                # Why is this important: Figure 7 -> An Improved Incremental Algorithm for. Constructing Restricted Delaunay Triangulations
                innerkeys = list(set(regionkeys)-set(boundkeys))
    
                #generate vertices for both regions (boundary vertices and inner vertices
                #Note that they are ordered -> boundary vertices in oder + inner vertices if any
                if innerkeys:
                    poly = [mesh.vertex_coordinates(key) for key in boundkeys1]
                    vertices1 = boundkeys1[1:] + [key for key in innerkeys if is_point_in_polygon(poly,mesh.vertex_coordinates(key))]
                    
                    poly = [mesh.vertex_coordinates(key) for key in boundkeys2]
                    vertices2 = boundkeys2[1:] + [key for key in innerkeys if is_point_in_polygon(poly,mesh.vertex_coordinates(key))]   
                else:
                    vertices1 = boundkeys1[1:] 
                    vertices2 = boundkeys2[1:]
                
                #delete old faces (just keys)
                for xfkey in xfkeys:
                    del mesh.face[xfkey] 
                     
                #remeshing of region 1     
                if boundkeys1:
                    indices = [];pts = []
                    for key in vertices1:
                        pts.append(points[int(key)])
                        indices.append(key)
                    # delaunay of region 1    
                    # second argument is a list with boundary indices starting with '0' -> ['0','1','2',...,'0']
                    faces = delaunay(pts,[str(ind) for ind in range(0,len(boundkeys1)-1)]+['0'])
                    #add new faces to mesh
                    for face in faces:
                        newface = [indices[int(face[0])],indices[int(face[1])],indices[int(face[2])]]
                        mesh.add_face(newface)
                        
                #remeshing of region 1    
                if boundkeys2: 
                    indices = [];pts = []
                    for key in vertices2:
                        pts.append(points[int(key)])
                        indices.append(key)
                    # delaunay of region 2    
                    # second argument is a list with boundary indices starting with '0' -> ['0','1','2',...,'0']
                    faces = delaunay(pts,[str(ind) for ind in range(0,len(boundkeys2)-1)]+['0'])
                    #add new faces to mesh
                    for face in faces:
                        newface = [indices[int(face[0])],indices[int(face[1])],indices[int(face[2])]]
                        mesh.add_face(newface)
             
    #return face vertices (ordered!)            
    return [mesh.face_vertices(fkey,True) for fkey in mesh.faces()]

