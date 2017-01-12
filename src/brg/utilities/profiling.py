import cStringIO
import cProfile
import pstats


def print_profile(func):
	def wrapper(*args, **kwargs):
	    profile = cProfile.Profile()
	    profile.enable()
	    res = func(*args, **kwargs)
	    profile.disable()
	    stream = cStringIO.StringIO()
	    stats  = pstats.Stats(profile, stream=stream)
	    stats.strip_dirs()
	    stats.sort_stats(1)
	    stats.print_stats(20)
	    print stream.getvalue()
	    return res
	return wrapper