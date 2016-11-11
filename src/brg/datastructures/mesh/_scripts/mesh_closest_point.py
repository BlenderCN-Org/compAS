# finding the closest point on a mesh
# reduces to a 2D problem by comparing the distance in the local plane
# to/of the neighbouring faces of the closest vertex

# 1. construct distance matrix
# 2. find closest vertex
# 3. find neighbouring faces
# 4. compute distances in uv-coordinates
# 5. if 3 equal => vertex is closest
#    if 2 equal => point is on shared edge
#    else       => point is in/on corresponding face
#
# compute distance with:
# d =
