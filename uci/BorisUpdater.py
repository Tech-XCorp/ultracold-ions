# vi: ts=4 sw=4

import numpy
import uci.Ptcls as Ptcls
import pyopencl as cl
import pyopencl.array as cl_array
import sys
import os


class BorisUpdater():

    def __init__(self, ctx = None, queue = None):
        self.ctx = ctx
        self.queue = queue
        if self.ctx == None:
            self.ctx = cl.create_some_context()
        if self.queue == None:
            self.queue = cl.CommandQueue(self.ctx,
                properties=cl.command_queue_properties.PROFILING_ENABLE)

    def update(self, xd, yd, zd, vxd, vyd, vzd, qd, md, forces,
            t, dt, num_steps):

        axd = cl_array.zeros_like(xd)
        ayd = cl_array.zeros_like(xd)
        azd = cl_array.zeros_like(xd)

        for i in range(numSteps):

            # First half of position advance
            xd += (0.5 * dt) * vxd
            yd += (0.5 * dt) * vyd
            zd += (0.5 * dt) * vzd

            t += 0.5 * dt

            axd.fill(0.0, self.queue)
            ayd.fill(0.0, self.queue)
            azd.fill(0.0, self.queue)
            for acc in forces:
                acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
                        axd, ayd, azd, t)
            vxd += dt * axd
            vyd += dt * ayd
            vzd += dt * azd

            # Second half of position advance
            xd += (0.5 * dt) * vxd
            yd += (0.5 * dt) * vyd
            zd += (0.5 * dt) * vzd

            t += 0.5 * dt

        return t
