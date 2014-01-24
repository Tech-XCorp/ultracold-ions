setTrapParameters(0,0,0)
%FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_1_22_NonEquilibriumTest\';
FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_1_23_NormalModeExpansionTest_BigData_smallZ\';

psd = dlmread([FileLocation 'psd.dat']);
params = dlmread([FileLocation 'params.dat']);
global G

setTrapParameters(params(2),-params(3)/G,params(1));
u0 = generateLattice(params(1),1);
u = findEquilibrium(u0);
[E,D,st] = normalModes(u,1);
global wz

freq = (0:0.5/(params(6)*params(7))/length(psd):0.5/(params(6)*params(7)));
freq = 1.0e-6*freq(1:end-1);
semilogy(freq,psd,'k')
hold on
for i=1:params(1)
    plot([1e-6*wz/(2*pi)*D(i) 1e-6*wz/(2*pi)*D(i)],[1e-12,1],'g')
end
axis([0.6 .8 1e-11 1e-2])
xlabel('Frequency MHz')
ylabel('PSD')
title(['Compare Axial Freq, N = ' num2str(params(1)) ', w = ' num2str(params(1)) ' kHz, delta = ' num2str(params(3))])
set(gca,'FontSize',24)

