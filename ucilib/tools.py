import numpy as np
import sys
import os
import glob
import re
import pyopencl as cl
import pyopencl.array as cl_array

def allFiles(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]

def runFiles(path, run):
    return glob.glob(path + '*' + str(run) + '_*')

numberRegex = re.compile("(\d+\.*\d*|\d*\.\d+)((e|E)(\+|\-)(\d+))*")

def getTime(filename):
    results = numberRegex.findall(filename)
    return eval("%s" % results[1][0])

def getData(filenames):
    return np.array([np.loadtxt(f) for f in filenames])


class FourierTransform:

    _src = """//CL//

__kernel void transform(
        __global float *zValues,
        __global const float2* phaseFactors,
        __global float2 *result,
        unsigned int numPtcls,
        unsigned int numOmegas,
        unsigned int numSlices)
{
    __private size_t nPtcl = get_global_id(0);
    __private size_t nOmega = get_global_id(1);

    if (nPtcl < numPtcls) {
        zValues += nPtcl;
        phaseFactors += numSlices * nOmega;
        __private float2 resReg = (float2)0;
        for (int s = 0; s < numSlices; ++s) {
            resReg += zValues[0] * phaseFactors[s];
            zValues += numPtcls;
        }
        result[nOmega * numPtcls + nPtcl] = resReg;
    }
}

"""

    def __init__(self, ctx=None, queue=None):
        self.ctx = ctx
        self.queue = queue
        if self.ctx == None:
            self.ctx = cl.create_some_context()
        if self.queue == None:
            self.queue = cl.CommandQueue(self.ctx,
                properties=cl.command_queue_properties.PROFILING_ENABLE)
        self.kernel = cl.Program(self.ctx, self._src).build().transform

    def __call__(self, zArray, tArray, omegaArray, queue=None):

        assert zArray.dtype == np.float32
        assert tArray.dtype == np.float32
        assert omegaArray.dtype == np.float32

        if queue == None:
            queue = self.queue

        numSlices = zArray.shape[0]
        numPtcls = zArray.shape[1]
        numOmegas = omegaArray.shape[0]
        assert numSlices == tArray.shape[0]

        zArrayD = cl_array.to_device(queue, zArray.flatten(), async=True)
        omegaArrayD = cl_array.to_device(queue, omegaArray.flatten(),
                async = True)
        phaseFactors = np.empty([numOmegas, numSlices]).astype(np.complex64)
        for i in range(numOmegas):
            phaseFactors[i] = np.exp(-1j * omegaArray[i] * tArray)
        phaseFactorsD = cl_array.to_device(queue, phaseFactors.flatten(),
                async=True)

        result = cl_array.empty(queue, numPtcls * numOmegas, dtype=np.complex64)

        self.kernel(queue, (numPtcls, numOmegas), None,
                zArrayD.data, phaseFactorsD.data, result.data,
                np.uint32(numPtcls), np.uint32(numOmegas),
                np.uint32(numSlices))

        return result.get(queue=queue).reshape(numOmegas, numPtcls)


# vi: ts=4 sw=4 filetype=pyopencl
