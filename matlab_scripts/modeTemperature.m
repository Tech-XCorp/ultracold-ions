% Plot extracted amplitudes for each mode over the time bin
% to see how amplitude for each mode changes over time

setTrapParameters(0,0,0);
global m wz
binsize = 1000;
hbar = 1.05457173e-34;
kB = 1.38e-23;
binsize = 1000;  

%FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_5_NormalModeExpansionTestWithLaserCooling\';
%FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_9_NormalModeExpansionTestWithLaserCooling\';
FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_5_NonEquilibriumTest_Mode45_zvels\';
%FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_6_NormalModeExpansionTest_zvels\';
%FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_2_7_AxialLaserCooling_COM1e-5\';

params = dlmread([FileLocation 'params.dat']);

% If haven't calculated amps and freqs, do so now
if ~exist([FileLocation 'amps' num2str(params(5)/binsize) '.dat'],'file')
    axialModeAmplitude(FileLocation,1:params(1),binsize);
end

amps = dlmread([FileLocation 'amps' num2str(params(5)/binsize) '.dat']);
freqs = dlmread([FileLocation 'freqs' num2str(params(5)/binsize) '.dat']);

ionEnergy = zeros(1,params(5)/binsize); % Store energies calculated from ion velocities and potentials
modeEnergy = zeros(1,params(5)/binsize); % Store energies calculated from amplitude of harmonic oscillation from modes

for i = 1:params(5)/binsize
%for i = 1:500000

    filename = [FileLocation int2str((i-1)*params(5)/binsize) '.dat']; 
    %filename = [FileLocation int2str(i) '.dat']; 

    M = dlmread(filename);
    z = M(3,:);
    %vz = 0;
    vz = M(4,:);
    energy = ionAxialEnergy(z,vz);
    
    ionEnergy(i) = sum(energy);
    %scatter(i,ionEnergy/kB)
    %  hold off
% %     %plot(energy)
  %    semilogy(energy)
   %   hold on
    
    for j = 1:127
        %const = 2*sqrt(hbar/(2*m*wz*D(j)));
        %semilogy([j j],[1e-12 abs(amps(i,j))])
        %plot([j j],[0 abs(amps(i,j))])
        
        %plot([wz*freqs(i,j)/2/pi wz*freqs(i,j)/2/pi],[0 abs(amps(i,j))])
        %semilogy([wz*freqs(i,j)/2/pi wz*freqs(i,j)/2/pi],[1-12 abs(amps(i,j))])
        %plot([j j],[0 abs(hbar*wz*freqs(j)*abs(amps(i,j))/const)])
        %semilogy([j j],[1e-34 abs(hbar*wz*freqs(j)*abs(amps(i,j))/const)])
        %semilogy([j j],[1e-34 abs(0.5*m*(wz*freqs(j))^2*abs(amps(i,j)).^2)])
       % hold on
        %E(i) = E(i) + hbar*wz*freqs(j)*abs(amps(i,j))/const;
        modeEnergy(i) = modeEnergy(i) + 0.5*m*(wz*freqs(j))^2*abs(amps(i,j)).^2;
    end
  % title([num2str(E(i)) ' ' num2str(ionEnergy(i))])
    %axis([1 127 1e-12 1e-6])
    %axis([1 127 0 5e-6])
    %axis([1 127 1e-35 1e-22])
    %axis([0.6e6 0.8e6  0 4e-6])
   % pause(.000001)
    %hold off
end


