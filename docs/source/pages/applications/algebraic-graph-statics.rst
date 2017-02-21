.. _algebraic-graph-statics:

********************************************************************************
Graph(ic) Statics
********************************************************************************

This page contains a few simple examples of Algebraic Graph Statics (AGS).
For more advanced and interactive examples, and examples in Rhino, Grasshopper
and the browser, please refer to the documentation of the AGS package.

http://block.arch.ethz.ch/docs/compas_ags


.. add scale to drawings
.. interaction?
.. slider?
.. rename obj file
.. for examples in Rhino/Browser, refer to docs of compas_ags
.. all leaves are external loads => draw as such


.. contents::


Single-panel truss
==================

In this example, we create the form diagram of a simple truss from the
geometric information stored in an OBJ file.

We set the edge representing an applied load as independent, give it a force
(or force density) and compute the force densities in the dependent edges.

Finally, we simply draw the force diagram as a representation of the computed
force distribution.


.. plot::
    :include-source:

    import brg_ags

    from brg_ags.diagrams import FormDiagram
    from brg_ags.diagrams import ForceDiagram

    from brg_ags.viewers.viewer import Viewer

    import brg_ags.algorithms as gs

    # make form diagram from obj
    # make force diagram from form

    form = FormDiagram.from_obj(brg_ags.get_data('/cases/gs_form_force.obj'))
    force = ForceDiagram.from_formdiagram(form)

    # set the magnitude of the applied load

    form.set_edge_force_by_index(0, -10.0)

    # update form and force diagram

    gs.update_forcedensity(form)
    gs.update_forcediagram(force, form)

    # display results

    viewer = Viewer(form, force, delay_setup=False)

    viewer.draw_form()
    viewer.draw_force()

    viewer.show()


Force-driven design
===================

Here we do the same as in the previous example, but then modify the force
diagram and compute the corresponding changes in the form diagram.

We store the original configuration to be plotted together with the modified one.


.. plot::
    :include-source:

    import brg_ags

    from brg_ags.diagrams import FormDiagram
    from brg_ags.diagrams import ForceDiagram

    from brg_ags.viewers.viewer import Viewer

    import brg_ags.algorithms as gs

    # make form diagram from obj
    # make force diagram from form

    form = FormDiagram.from_obj(brg_ags.get_data('cases/gs_form_force.obj'))
    force = ForceDiagram.from_formdiagram(form)

    # set the fixed points

    form.set_fixed([4, 5])
    force.set_fixed([2])

    # set the magnitude of the applied load

    form.set_edge_force_by_index(0, -10.0)

    # update the diagrams

    gs.update_forcedensity(form)
    gs.update_forcediagram(force, form)

    # store lines representing the current state of equilibrium

    form_lines = []
    for u, v in form.edges_iter():
        form_lines.append({
            'start': form.vertex_coordinates(u, 'xy'),
            'end'  : form.vertex_coordinates(v, 'xy'),
            'width': 2.0,
            'color': '#999999'
        })

    force_lines = []
    for u, v in force.edges_iter():
        force_lines.append({
            'start': force.vertex_coordinates(u, 'xy'),
            'end'  : force.vertex_coordinates(v, 'xy'),
            'width': 2.0,
            'color': '#999999'
        })

    # modify the geometry of the force diagram

    force.vertex[1]['x'] -= 5.0

    # update the formdiagram

    gs.update_formdiagram(form, force, kmax=100)

    # display the orginal configuration
    # and the configuration after modifying the force diagram

    viewer = Viewer(form, force, delay_setup=False)

    viewer.draw_form(lines=form_lines, forces_on=False)
    viewer.draw_force(lines=force_lines)

    viewer.show()


Loadpath Optimisation
=====================

.. plot::
    :include-source:

    import yaml

    import brg_ags

    from brg_ags.diagrams.formdiagram import FormDiagram
    from brg_ags.diagrams.forcediagram import ForceDiagram

    from brg_ags.viewers.viewer import Viewer

    import brg_ags.algorithms as gs


    with open(brg_ags.get_data('form_lpopt.yaml'), 'rb') as fp:
        data = yaml.load(fp)


    form = FormDiagram.from_data(data['form'])
    form.identify_fixed()

    force = ForceDiagram.from_formdiagram(form)

    gs.update_forcediagram(force, form)

    force.vertex[1]['is_param'] = True
    force.vertex[2]['is_param'] = True
    force.vertex[3]['is_param'] = True
    force.vertex[4]['is_param'] = True
    force.vertex[5]['is_param'] = True
    force.vertex[6]['is_param'] = True

    form.vertex[0]['is_fixed'] = True
    form.vertex[1]['is_fixed'] = True
    form.vertex[2]['is_fixed'] = True
    form.vertex[3]['is_fixed'] = True
    form.vertex[4]['is_fixed'] = True
    form.vertex[5]['is_fixed'] = True
    form.vertex[6]['is_fixed'] = True

    form_lines = []
    for u, v in form.edges_iter():
        form_lines.append({
            'start': form.vertex_coordinates(u, 'xy'),
            'end'  : form.vertex_coordinates(v, 'xy'),
            'width': 2.0,
            'color': '#999999'
        })

    force_lines = []
    for u, v in force.edges_iter():
        force_lines.append({
            'start': force.vertex_coordinates(u, 'xy'),
            'end'  : force.vertex_coordinates(v, 'xy'),
            'width': 2.0,
            'color': '#999999'
        })

    gs.optimise_loadpath(form, force)

    viewer = Viewer(form, force, delay_setup=False)

    viewer.draw_form(forcescale=5, lines=form_lines)
    viewer.draw_force(vertexlabel={key: key for key in force}, lines=force_lines)

    viewer.show()
