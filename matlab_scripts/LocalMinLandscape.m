% Compute equilibrium positions a lot, see the "landscape" of potential
% energies


FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_10_NormalModeExpansionTestWithLaserCooling\';
thetas = dlmread([FileLocation 'thetas.dat']);
params = dlmread([FileLocation 'params.dat']);
setTrapParameters(44,-80,127);

binsize = 1000;
pot = zeros(1,params(5)/binsize);
%pot = zeros(1,100);
%u0 = generateLattice(127,1);
for i = 0:binsize:params(5)-1
%for i = 1:100
    i
    filename =[FileLocation int2str(i) '.dat'];
    M = dlmread(filename);
    u = convertPythonDataToMatlab(M);
    u = rotate(u,-thetas(i+1));            % rotate to that config
    [u pot((i/1000)+1)] = findEquilibrium(u);
    %[u pot(i)] = findEquilibrium(u0);

end