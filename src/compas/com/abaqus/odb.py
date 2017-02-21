"""brg_fea.odb : Abaqus .odb file."""

from abaqus import *
from abaqusConstants import *
from job import *

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def odb_results(odb, temp, name):
    """ Extracts results from the .odb file for all steps.

    Parameters:
        odb (str): Path of the .odb file to open.
        temp (str): Temp folder for storing data.
        name (str): Name of the Structure.

    Returns:
        None
    """
    print('EXTRACTING DATA.....')
    od = openOdb(path=odb)
    fo_nodes = ['RF', 'RM', 'U', 'UR']
    fo_elements = ['SF', 'SM', 'SK', 'SE', 'S']
    # print od.steps['S2_LOADS'].frames[-1].fieldOutputs['SF'].values[4]
    for step in od.steps.keys():
        frames = od.steps[step].frames
        for frame in [frames[-1]]:
            fo = frame.fieldOutputs
            fields = fo.keys()
            description = frame.description
            with open('{0}{1}_{2}_info.txt'.format(temp, name, step), 'w') as f:
                f.write(description)
            # no = str(frame.incrementNumber)

            # Node data
            for field in fo_nodes:
                if field in fields:
                    components = list(fo[field].componentLabels)
                    cadd = ['magnitude']
                    dt = {component: {} for component in components + cadd}
                    values = fo[field].values
                    for value in values:
                        data = value.data
                        node = str(value.nodeLabel - 1)
                        for c, component in enumerate(components):
                            dt[component][node] = float(data[c])
                        dt['magnitude'][node] = float(value.magnitude)
                    for component in components + cadd:
                        json_name = '{0}{1}_{2}_{3}_{4}.json'.format(
                            temp, name, step, field, component)
                        with open(json_name, 'w') as f:
                            json.dump(dt[component], f)

            # Element data
            for field in fo_elements:
                if field in fields:
                    components = list(fo[field].componentLabels)
                    cadd = ['magnitude', 'mises', 'maxPrincipal', 'axes',
                            'minPrincipal']
                    dt = {component: {} for component in components + cadd}
                    values = fo[field].values
                    for value in values:
                        data = value.data
                        element = str(value.elementLabel - 1)
                        ip = value.integrationPoint
                        if value.sectionPoint:
                            sp = value.sectionPoint.number
                        else:
                            sp = 0
                        id = 'ip{0}_sp{1}'.format(ip, sp)
                        for c, component in enumerate(components):
                            try:
                                dt[component][element][id] = float(data[c])
                            except:
                                for ic in components + cadd:
                                    dt[ic][element] = {}
                                try:
                                    dt[component][element][id] = float(data[c])
                                except:
                                    pass
                        if value.magnitude:
                            dt['magnitude'][element][id] = float(value.magnitude)
                        if value.localCoordSystem:
                            dt['axes'][element][id] = value.localCoordSystem
                        if value.mises:
                            dt['mises'][element][id] = float(value.mises)
                        maxP = float(value.maxPrincipal)
                        minP = float(value.minPrincipal)
                        if maxP:
                            dt['maxPrincipal'][element][id] = maxP
                        if minP:
                            dt['minPrincipal'][element][id] = minP
                    for component in components + cadd:
                        json_name = '{0}{1}_{2}_{3}_{4}.json'.format(
                            temp, name, step, field, component)
                        with open(json_name, 'w') as f:
                            json.dump(dt[component], f)

    print('DATA EXTRACTION COMPLETE')


# Run and extract data
name = sys.argv[-1]
path = sys.argv[-2]
temp = sys.argv[-3]
cpus = sys.argv[-4]
fnm = '{0}{1}.inp'.format(path, name)
print('Submitting job {0}'.format(fnm))
job = mdb.JobFromInputFile(inputFileName=fnm, name=name, numCpus=int(cpus),
                           parallelizationMethodExplicit=DOMAIN,
                           numDomains=int(cpus),
                           multiprocessingMode=DEFAULT)
job.submit()
job.waitForCompletion()
odb_results(odb='{0}{1}.odb'.format(temp, name), temp=temp, name=name)
