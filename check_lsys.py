import sys
import matplotlib
matplotlib.use('agg')

import lsys.tests as tests
status = tests.test(*sys.argv[1:])
sys.exit(status)
