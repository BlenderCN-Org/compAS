import time


def test(n=10, pause=0.1, config=None):
    for i in range(n):
        print i
        time.sleep(pause)


if __name__ == '__main__':

    import sys
    import json
    import cStringIO
    import cProfile
    import pstats
    import traceback

    ipath = sys.argv[1]
    opath = sys.argv[2]

    with open(ipath, 'rb') as f:
        idict = json.load(f)

    try:
        profile = cProfile.Profile()
        profile.enable()
        # ======================================================================
        # profiler enabled
        # ======================================================================
        config = idict.get('config', {})
        n = idict['n']
        pause = idict['pause']
        test(n=n, pause=pause, config=config)
        data = {'test': 'success'}
        # ======================================================================
        # profiler disabled
        # ======================================================================
        profile.disable()
        stream = cStringIO.StringIO()
        stats  = pstats.Stats(profile, stream=stream)
        stats.strip_dirs()
        stats.sort_stats(1)
        stats.print_stats(20)
        odict = {}
        odict['data']       = data
        odict['error']      = None
        odict['profile']    = stream.getvalue()
        odict['iterations'] = None
    except:
        odict = {}
        odict['data']       = None
        odict['error']      = traceback.format_exc()
        odict['profile']    = None
        odict['iterations'] = None

    with open(opath, 'wb+') as f:
        json.dump(odict, f)
