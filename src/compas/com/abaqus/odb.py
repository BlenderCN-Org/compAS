"""Abaqus .odb data extraction file."""

from abaqus import *
from abaqusConstants import *
from job import *

from time import time

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


node_fields = ['RF', 'RM', 'U', 'UR', 'CF', 'CM']
element_fields = ['SF', 'SM', 'SK', 'SE', 'S', 'E']


def odb_results(temp, name, output):
    """ Extracts results from the .odb file for all steps.

    Parameters:
        temp (str): Temp folder for storing the written data and analysis files.
        name (str): Name of the Structure.
        output (str): Output type 'json' or 'txt'.

    Returns:
        None
    """
    odb = '{0}{1}.odb'.format(temp, name)
    od = openOdb(path=odb)
    # print od.steps['S2_LOADS'].frames[-1].fieldOutputs['SF'].values[4]
    for step in od.steps.keys():
        frames = od.steps[step].frames
        for frame in [frames[-1]]:
            tic = time()
            fo = frame.fieldOutputs
            fields = fo.keys()

            # Node data
            cadd = ['magnitude']
            for field in node_fields:
                if field in fields:
                    components = list(fo[field].componentLabels)
                    call = components + cadd
                    dt = {component: {} for component in call}
                    for value in fo[field].values:
                        data = value.data
                        node = str(value.nodeLabel - 1)
                        for c, component in enumerate(components):
                            dt[component][node] = float(data[c])
                        dt['magnitude'][node] = float(value.magnitude)
                    for component in call:
                        fnm = '{0}{1}_{2}_{3}_{4}'.format(temp, name, step, field, component)
                        if output == 'json':
                            with open(fnm + '.json', 'w') as f:
                                json.dump(dt[component], f)
                        elif output == 'txt':
                            with open(fnm + '.txt', 'w') as f:
                                f.write('node value\n')
                                for nkey in sorted(dt[component], key=int):
                                    val = dt[component][nkey]
                                    f.write('{0} {1}\n'.format(nkey, val))

            # Element data
            cadd = ['mises', 'maxPrincipal', 'axes', 'minPrincipal']
            for field in element_fields:
                if field in fields:
                    components = list(fo[field].componentLabels)
                    call = components + cadd
                    dt = {component: {} for component in call}
                    for value in fo[field].values:
                        data = value.data
                        element = str(value.elementLabel - 1)
                        ip = value.integrationPoint
                        sp = value.sectionPoint.number if value.sectionPoint else 0
                        id = 'ip{0}_sp{1}'.format(ip, sp)
                        for c, component in enumerate(components):
                            try:
                                dt[component][element][id] = float(data[c])
                            except:
                                for j in call:
                                    dt[j][element] = {}
                                try:  # Can remove this try?
                                    dt[component][element][id] = float(data[c])
                                except:
                                    pass
                        if value.localCoordSystem:
                            dt['axes'][element][id] = value.localCoordSystem
                        if value.mises:
                            dt['mises'][element][id] = float(value.mises)
                        if value.maxPrincipal:
                            dt['maxPrincipal'][element][id] = float(value.maxPrincipal)
                        if value.minPrincipal:
                            dt['minPrincipal'][element][id] = float(value.minPrincipal)
                    for component in call:
                        fnm = '{0}{1}_{2}_{3}_{4}'.format(temp, name, step, field, component)
                        if output == 'json':
                            with open(fnm + '.json', 'w') as f:
                                json.dump(dt[component], f)
                        elif output == 'txt':
                            with open(fnm + '.txt', 'w') as f:
                                f.write('element id value\n')
                                for ekey in sorted(dt[component], key=int):
                                    for id in dt[component][ekey]:
                                        val = dt[component][ekey][id]
                                        f.write('{0} {1} {2}\n'.format(ekey, id, val))

            with open('{0}{1}_{2}_info.txt'.format(temp, name, step), 'w') as f:
                f.write(frame.description + '\n')
                f.write('Data extraction time: {0:.3g}s'.format(time() - tic))


# Run and extract data
name = sys.argv[-1]
path = sys.argv[-2]
temp = sys.argv[-3]
cpus = sys.argv[-4]
output = sys.argv[-5]
fnm = '{0}{1}.inp'.format(path, name)
job = mdb.JobFromInputFile(inputFileName=fnm, name=name, numCpus=int(cpus), multiprocessingMode=DEFAULT,
                           numDomains=int(cpus), parallelizationMethodExplicit=DOMAIN)
job.submit()
job.waitForCompletion()
odb_results(temp=temp, name=name, output=output)
