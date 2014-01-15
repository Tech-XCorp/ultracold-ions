N = 217; % S = 8 complete hex shells
setTrapParameters(45,35,N);
u0 = generateLattice(N,1);
u0 = idealLatticeScale(u0,1,0.01);
u = addDefects(u0,0,1.128,0,2.8863,0,0.1118);
[Eaxial,Daxial,st_ax] = normalModes(u,1);
%[Eplanar,Dplanar,st_pl] = normalModes(u,0);

