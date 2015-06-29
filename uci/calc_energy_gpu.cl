//
// OpenCL kernel for computing total energy
// 

#ifdef USE_DOUBLE
#ifdef cl_khr_fp64
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
#define REAL double
#define REAL3 double3
#define EPS2 1.0e-30
#endif
#else
#define REAL float
#define REAL3 float3
#define EPS2 1.0e-20f
#endif

REAL Vij(REAL3 r1, REAL q1, REAL3 r2, REAL q2);

__kernel void calc_potential_energy(__global REAL* x,
    __global REAL* y, __global REAL* z, __global REAL* charge, 
    __global REAL* potEnergy,
     int nPtcls) {

  int tid = get_global_id(0) + get_global_id(1) * get_global_size(0);

  REAL energy = 0;
  if (tid < nPtcls) {
    REAL3 r1 = (REAL3)(x[tid], y[tid], z[tid]);
    REAL q1 = k * charge[tid];
    for (int i = 0; i < nPtcls; ++i) {
      if (tid != i) {
        REAL3 r2 = (REAL3)(x[i], y[i], z[i]);
        REAL q2 = charge[i];
        energy += Vij(r1, q1, r2, q2);
      }
    }
    potEnergy[tid] = energy / (REAL)2;
  }
}

REAL Vij(REAL3 r1, REAL q1, REAL3 r2, REAL q2) {
  REAL3 dr = r1 - r2;
  REAL r12 = fma(dr.x, dr.x, fma(dr.y, dr.y, fma(dr.z, dr.z, IMPACTFACT + EPS2)));
  return q1 * q2 / sqrt(r12);
}

