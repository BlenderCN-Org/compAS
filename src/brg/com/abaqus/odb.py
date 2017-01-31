"""brg_fea.odb : Abaqus .odb file."""

from abaqus import *
from abaqusConstants import *
from job import *

from brg_fea.structure import structure

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def odb_results(odb):
    """ Extracts results from the .odb file for all steps.

    Note:
        Element values are converted into nodal values.

    Parameters:
        odb (str): Path of the .odb file to open.

    Returns:
        dic: .odb data for nodes and elements.
    """
    od = openOdb(path=odb)
    data = {}
    fo_nodes = ['RF', 'RM', 'U', 'UR']
    fo_elements = ['SF', 'SM', 'SK', 'SE', 'S']
    for step in od.steps.keys():
        frames = od.steps[step].frames
        ds = {'nodes': {}, 'elements': {}, 'increments': [],
              'descriptions': []}
        # for frame in frames:
        for frame in [frames[-1]]:
            fo = frame.fieldOutputs
            fkeys = fo.keys()
            ds['increments'].append(frame.frameValue)
            no = str(frame.incrementNumber)
            df = {}
            ds['descriptions'].append(frame.description)
            for i in fo_nodes:
                if i in fkeys:
                    labels = fo[i].componentLabels
                    values = fo[i].values
                    dfo = {}
                    for j in values:
                        dt = j.data
                        node = str(j.nodeLabel - 1)
                        dv = {}
                        dv['magnitude'] = j.magnitude
                        for c, label in enumerate(labels):
                            try:
                                dv[label] = float(dt[c])
                            except:
                                pass
                        dfo[node] = dv
                    df[i] = dfo
            ds['nodes'][no] = df
            df = {}
            for i in fo_elements:
                if i in fkeys:
                    labels = fo[i].componentLabels
                    values = fo[i].values
                    dfo = {}
                    for j in values:
                        ip = j.integrationPoint
                        if j.sectionPoint:
                            sp = j.sectionPoint.number
                        else:
                            sp = 0
                        id = 'ip{0}_sp{1}'.format(ip, sp)
                        dt = j.data
                        element = str(j.elementLabel - 1)
                        dv = {}
                        for c, label in enumerate(labels):
                            try:
                                dv[label] = float(dt[c])
                            except:
                                pass
                        dv['magnitude'] = j.magnitude
                        dv['mises'] = j.mises
                        dv['maxPrincipal'] = j.maxPrincipal
                        dv['minPrincipal'] = j.minPrincipal
                        try:
                            dfo[element]
                        except:
                            dfo[element] = {}
                        dfo[element]['axes'] = j.localCoordSystem
                        dfo[element][id] = dv
                    df[i] = dfo
            ds['elements'][no] = df
        data[step] = ds
    return data


# Run and extract data
name = sys.argv[-1]
path = sys.argv[-2]
temp = sys.argv[-3]
fnm = '{0}{1}.inp'.format(path, name)
print('Submitting job {0}'.format(fnm))
job = mdb.JobFromInputFile(inputFileName=fnm, name=name)
job.submit()
job.waitForCompletion()
results = odb_results(odb='{0}{1}.odb'.format(temp, name))
try:
    mdl = structure.load('{0}{1}.obj'.format(path, name))
    mdl.results = results
    mdl.save('{0}{1}.obj'.format(path, name))
except:
    pass
with open('{0}{1}.json'.format(path, name), 'w') as f:
    json.dump(results, f)
