from os.path import dirname, realpath, sep, pardir
import sys
sys.path.append(dirname(realpath(__file__)) + sep + pardir + sep +
         "examples")
import simExample

def test_sim():
    simExample.run_simulation()


