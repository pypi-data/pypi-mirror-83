import sys

from coverage import Coverage

cov = Coverage()
cov.erase()
cov.start()

from unit_tests import unit_tests
test = unit_tests.run()
cov.stop()
cov.html_report(directory="unit_tests/htmlcov", omit=["/usr/*", "*/.local/*", "*venv/*"])

if test is not None:
    sys.exit(not test.result.wasSuccessful())
else:
    sys.exit(-1)
