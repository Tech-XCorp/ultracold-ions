# vi: ts=4 sw=4

import pyopencl.array as cl_array
import pyopencl as cl
import numpy
import sys
import os
import uci.TrapConfiguration as TrapConfiguration
import uci.CyclAdvance as CyclAdvance
import uci.AxialDampingAdvance as AxialDampingAdvance
import uci.AngularDampingAdvance as AngularDampingAdvance
import uci.CoolingAlongXAdvance as CoolingAlongXAdvance

class BendKickUpdater():


    def __init__(self, ctx = None, queue = None):

        self.trapConfiguration = TrapConfiguration.TrapConfiguration()
        self.axialDampingCoefficient = 0
        self.angularDampingCoefficient = 0

        self.ctx = ctx
        self.queue = queue
        if self.ctx == None:
            self.ctx = cl.create_some_context()
        if self.queue == None:
            self.queue = cl.CommandQueue(self.ctx,
                properties = cl.command_queue_properties.PROFILING_ENABLE)
        self.cyclAdvance = CyclAdvance.CyclAdvance(self.ctx, self.queue)
        self.axialDampingAdvance = AxialDampingAdvance.AxialDampingAdvance(self.ctx, self.queue)
        self.angularDampingAdvance = AngularDampingAdvance.AngularDampingAdvance(self.ctx, self.queue)

        absolutePathToKernels = os.path.dirname(
                os.path.realpath(__file__))
        src = open(absolutePathToKernels + '/velocity_kick_advance.cl', 
                'r').read()

        self.velKickAdvF = cl.Program(self.ctx, src)
        try:
            self.velKickAdvF.build()
        except:
              print("Error:")
              print(self.velKickAdvF.get_build_info(
                    self.ctx.devices[0],
                    cl.program_build_info.LOG))
              raise
        self.velKickAdvF.advance_ptcls_velocity_kick.set_scalar_arg_dtypes(
                [None, None, None, None, None, None, None, None,
                None, None, None, numpy.float32, numpy.int32])

        self.velKickAdvD = cl.Program(self.ctx, src)
        try:
            self.velKickAdvD.build()
        except:
              print("Error:")
              print(self.velKickAdvD.get_build_info(
                    self.ctx.devices[0],
                    cl.program_build_info.LOG))
              raise
        self.velKickAdvD.advance_ptcls_velocity_kick.set_scalar_arg_dtypes(
                [None, None, None, None, None, None, None, None,
                None, None, None, numpy.float64, numpy.int32])

    def update(self, xd, yd, zd, vxd, vyd, vzd, qd, md, accelerations,
            t, dt, numSteps):

        axd = cl_array.zeros(self.queue, xd.shape, xd.dtype)
        ayd = cl_array.zeros(self.queue, xd.shape, xd.dtype)
        azd = cl_array.zeros(self.queue, xd.shape, xd.dtype)

        # half step
        self.cyclAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                qd, md, self.trapConfiguration.Bz, 0.5 * dt)
        if self.axialDampingCoefficient != None:
            self.axialDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, self.axialDampingCoefficient, 0.5 * dt)
        if self.angularDampingCoefficient != None:
            self.angularDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, self.angularDampingCoefficient,
                    self.trapConfiguration.omega, 0.5 * dt)
        self.trapConfiguration.theta += 0.5 * dt * self.trapConfiguration.omega
        t += 0.5 * dt

        # full kick
        for acc in accelerations:
            acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
                    axd, ayd, azd, t, dt)
        self.applyVelocityKick(xd, yd, zd, vxd, vyd, vzd,
                qd, md, axd, ayd, azd, dt)

        # n - 1 full drift-kick pairs
        for i in range(numSteps - 1):
            self.cyclAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, self.trapConfiguration.Bz, dt)
            if self.axialDampingCoefficient != None:
                self.axialDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                        qd, md, self.axialDampingCoefficient, dt)
            if self.angularDampingCoefficient != None:
                self.angularDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                        qd, md, self.angularDampingCoefficient,
                        self.trapConfiguration.omega, dt)
            self.trapConfiguration.theta += dt * self.trapConfiguration.omega
            t += dt
            axd.fill(numpy.float32(0), queue = self.queue)
            ayd.fill(numpy.float32(0), queue = self.queue)
            azd.fill(numpy.float32(0), queue = self.queue)
            for acc in accelerations:
                acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
                        axd, ayd, azd, t, dt)
            self.applyVelocityKick(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, axd, ayd, azd, dt)

        if self.angularDampingCoefficient != None:
            self.angularDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, self.angularDampingCoefficient,
                    self.trapConfiguration.omega, 0.5 * dt)
        if self.axialDampingCoefficient != None:
            self.axialDampingAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                    qd, md, self.axialDampingCoefficient, 0.5 * dt)
        self.cyclAdvance.advancePtcls(xd, yd, zd, vxd, vyd, vzd,
                qd, md, self.trapConfiguration.Bz, 0.5 * dt)
        self.trapConfiguration.theta += 0.5 * dt * self.trapConfiguration.omega
        t += 0.5 * dt

        return t

    def applyVelocityKick(self, xd, yd, zd, vxd, vyd, vzd,
                qd, md, axd, ayd, azd, dt):
        prec = xd.dtype
        if prec == numpy.float32:
            self.velKickAdvF.advance_ptcls_velocity_kick(self.queue,
               (xd.size, ), None,
               xd.data, yd.data, zd.data,
               vxd.data, vyd.data, vzd.data,
               qd.data, md.data,
               axd.data, ayd.data, azd.data,
               numpy.float32(dt),
               numpy.int32(xd.size),
               g_times_l = False)
        elif prec == numpy.float64:
            self.velKickAdvD.advance_ptcls_velocity_kick(self.queue,
               (xd.size, ), None,
               xd.data, yd.data, zd.data,
               vxd.data, vyd.data, vzd.data,
               qd.data, md.data,
               axd.data, ayd.data, azd.data,
               numpy.float64(dt),
               numpy.int32(xd.size),
               g_times_l = False)
        else:
            print("Unknown float type.")

