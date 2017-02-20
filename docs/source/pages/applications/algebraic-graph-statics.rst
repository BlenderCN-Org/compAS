.. _algebraic-graph-statics:

********************************************************************************
Algebraic Graph Statics
********************************************************************************


.. add scale to drawings
.. interaction?
.. slider?
.. rename obj file
.. for examples in Rhino/Browser, refer to docs of compas_ags
.. all leaves are external loads => draw as such


.. contents::



Basic Graph Statics
===================

.. plot::
    :include-source:

    # single-panel truss
    # formdiagram from obj (lines)
    # forcediagram from formdiagram
    # viewer

    import brg_ags

    from brg_ags.diagrams import FormDiagram
    from brg_ags.diagrams import ForceDiagram

    from brg_ags.viewers.viewer import Viewer

    import brg_ags.algorithms as ags

    form = FormDiagram.from_obj(brg_ags.get_data('/cases/gs_form_force.obj'))

    # replace by set_fixed
    form.identify_fixed()

    force = ForceDiagram.from_formdiagram(form)

    index_uv = {index: (u, v) for index, u, v in form.edges_enum()}

    u, v = index_uv[0]

    form.edge[u][v]['is_ind'] = True
    form.edge[u][v]['q'] = -3.

    ags.update_forcedensity(form)
    ags.update_forcediagram(force, form)

    viewer = Viewer(form, force)

    viewer.setup()

    viewer.draw_form(forcescale=2)
    viewer.draw_force()

    viewer.show()


Advanced Graph Statics
======================

.. plot::
    :include-source:

    # single-panel truss
    # modification of form & update of force

    import brg_ags

    from brg_ags.diagrams import FormDiagram
    from brg_ags.diagrams import ForceDiagram

    from brg_ags.viewers.viewer import Viewer

    import brg_ags.algorithms as ags

    form = FormDiagram.from_obj(brg_ags.get_data('cases/gs_form_force.obj'))

    form.identify_fixed()

    force = ForceDiagram.from_formdiagram(form)

    form[5]['is_fixed'] = True
    form[4]['is_fixed'] = True

    force[2]['is_fixed'] = True

    index_uv = form.index_uv()

    u, v = index_uv[0]

    form.edge[u][v]['q'] = -5.
    form.edge[u][v]['is_ind'] = True

    ags.update_forcedensity(form)
    ags.update_forcediagram(force, form)

    # store lines representing the original diagram

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

    force.vertex[1]['x'] -= 5.0

    ags.update_formdiagram(form, force, kmax=100)

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
