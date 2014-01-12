#ifdef USE_DOUBLE
#ifdef cl_khr_fp64
#pragma OPENCL EXTENSION cl_khr_fp64: enable
#define REAL double
#define REAL3 double3
#define REAL4 double4
#define EPS2 1.0e-30
#endif
#else
#define REAL float
#define REAL3 float3
#define REAL4 float4
#define EPS2 1.0e-18f
#endif

__kernel void compute_acceleration(
// positions of particles
    const __global REAL* vxGlob,
    const __global REAL* vyGlob,
    const __global REAL* vzGlob,
// mass of particles
    const __global REAL* mass,
// Friction coefficient
    REAL alpha,
// Number of particles
    int nPtcls,
// accelerations (output)
    __global REAL* axGlob,
    __global REAL* ayGlob,
    __global REAL* azGlob)
{
  __private int n = get_global_id(0);
  if (n < nPtcls) {
    __private REAL vx = vxGlob[n];
    __private REAL vy = vyGlob[n];
    __private REAL vz = vzGlob[n];
    __private REAL m = mass[n];

    __private REAL ax = 0;
    __private REAL ay = 0;
    __private REAL az = -alpha * vz / m;

    axGlob[n] += ax;
    ayGlob[n] += ay;
    azGlob[n] += az;
  }
}


