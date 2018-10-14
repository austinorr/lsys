import sys

import lsys.tests as tests
status = tests.test(*sys.argv[1:])
sys.exit(status)
