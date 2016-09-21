# brg.datastructures: todo

- mesh: geodesic distance
- mesh: heat diffusion
- mesh: ...
- area weighted smoothing
- mesh isolines/contours
- mesh downhill
- mesh curvature

- what to do with mesh-specific errors?
- should there be a procedural interface?

- active vs passive (?!) verbs to indicate operation on same mesh or return of new mesh

- operations => local vs. algorithms => global

- is it okay to have different possible return types?
  e.g.: str, None

- many of the ``None`` returns have to be replaced by ``MeshError`` raises.
