% Master Script
%% Load Data
cleanupObj = onCleanup(@CLEAN);
FileLocation = 'D:\PenningSimulationData\2014_4_17_SmallCrystalModes\';  
setTrapParameters(0,0,0);
global N m wr wc q ke B wz V0 w G Vw ww M l0 v0 params
params = dlmread([FileLocation 'params.dat']);
setTrapParameters(params(2),-params(3)/G,params(1));
thetas = dlmread([FileLocation 'thetas.dat']);
disp('Loading Simulation Data...')
[us,zs,vxs,vys,vzs] = convertPythonDataToMatlab2(FileLocation,5);
disp('Finished Loading')
% Move positions to rotating frame
for i = 0:params(5)-1
    us(i+1,:) = rotate(us(i+1,:),-thetas(i+1));           
end

%% Calculate Normal Modes for a particular Configuration
u0 = findEquilibrium(us(1,:));
% Use first configuration, equilibrium positions
[Ea,Da] = normalModes(u0,1); % Axial Modes
[Ep,Dp,junk,A] = normalModes(u0,0); % Planar Modes

%% View Simulation
disp('Viewing Data')

% vidpath = 'ExciteMagnetron2';
%  vwr = VideoWriter(vidpath, 'Motion JPEG AVI');
%  vwr.FrameRate = 30;
%  open(vwr);

%for i = 0
for i = 0:10:params(5)-1
%for i = 0:5:1000
    u = us(i+1,:);
    scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
    %axis([-1.2*max(u),1.2*max(u),-1.2*max(u),1.2*max(u)])
    axis([-9,9,-9,9])
    title(['Rotating Frame, N = ' num2str(params(1)) ', \delta = ' num2str(params(3)) ', w = ' num2str(params(2)) ' kHz, i = ' num2str(i)])
    xlabel('Scaled position')
   %  writeVideo(vwr,getframe(gcf));
    pause(.00001)
end
%close(vwr)



%%  Excite Axial Modes for Python Simulation

N = 19;
setTrapParameters(54.5,-80,N);
global N m wr wc q ke B wz V0 w G Vw ww M l0 v0
u0 = generateLattice(N,1);
u0 = rotate(u0,pi/2);     % get same major axis as dominics code
u0 = findEquilibrium(u0);
[Ea,Da] = normalModes(u0,1); % Axial Modes

date = '2014_4_21_SmallCrystalModes/';

zmax = 5e-7;
for mode = 1:N
    filename = ['D:\PenningSimulationData\' date '\19_54.5_-80_Amode' num2str(mode) '.dat'];
    z = Ea(:,mode)*zmax; % scale 
    pythonReadableU(u0,z,filename)
end
        
%% Load Axial Excitations and plot PSD (2014-4-17)
FileLocation = 'D:\PenningSimulationData\2014_4_21_SmallCrystalModes\';  
setTrapParameters(0,0,0);
global N m wr wc q ke B wz V0 w G Vw ww M l0 v0 params
params = dlmread([FileLocation 'params.dat']);
setTrapParameters(params(2),-params(3)/G,params(1));
thetas = dlmread([FileLocation 'thetas.dat']);

freq = (0:0.5/(params(6)*params(7))/(params(5)/2):0.5/(params(6)*params(7)));
freq = 1.0e-6*freq(1:end-1); % chop of last one, because of Matlab ranges...
cmp = colormap(hsv(19));
for mode = 15:19
    mode
    [us,zs,vxs,vys,vzs] = convertPythonDataToMatlab2(FileLocation,mode);
    u0 = findEquilibrium(us(1,:));
    [Ea,Da] = normalModes(u0,1); % Axial Modes
    
    %Project Axial Motion in to Normal Modes
    norm_coords = zeros(params(5),params(1)); 
    norm_vels = zeros(params(5),params(1)); 
    
    for k = 1:params(5)

        norm_coords(k,:) = modeBasis(zs(k,:),Ea);
        norm_vels(k,:) = modeBasis(vzs(k,:),Ea);

    end

    save([FileLocation 'axialModeDecomposition_amode ' num2str(mode) '.mat'],'norm_coords')
    save([FileLocation 'axialVelModeDecomposition_amode ' num2str(mode) '.mat'],'norm_vels')
    
    
%     spectra = abs(fft(zs)).^2;
%     Zpsd = sum(spectra, 2);
%     Zpsd = Zpsd(1:(length(Zpsd)/2))+Zpsd(end:-1:length(Zpsd)/2+1);
%     semilogy(freq,Zpsd,'Color',cmp(mode,:))
%     hold on
%     pause(.01)
end
   
%     
% for i=1:params(1)
%     plot([1e-6*wz/(2*pi)*Da(i) 1e-6*wz/(2*pi)*Da(i)],[1e-20,1e-5],'k')
% end


%% Find maximum amplitude over several periods for normal coordinates
FileLocation = 'D:\PenningSimulationData\2014_4_21_SmallCrystalModes\';
%params = dlmread([FileLocation 'params.dat']);
mode = 14;
load([FileLocation 'axialModeDecomposition_amode ' num2str(mode) '.mat'],'norm_coords')
dims = size(norm_coords);
blocksize = 100;
envelope = reshape(max(reshape(norm_coords,blocksize,dims(1)*dims(2)/blocksize)),dims(1)/blocksize,dims(2));
cmp = colormap(hsv(dims(2)));
semilogy(envelope)
figure
envelope(:,mode)=[];
plot(envelope)

%% Movie of Planar Modes

mg = abs(Ep);
ph = angle(Ep);

%vidpath = 'CyclotronModes19';
 %vwr = VideoWriter(vidpath, 'Motion JPEG AVI');
 %vwr.FrameRate = 30;
 %open(vwr);

%for mode = N+1:2*N
for mode = 2
%u = us(1,:);
stretch = 0.5;
for wt = 0 : 2*pi/50 : 6*pi
    scatter(u0(1:end/2),u0(end/2+1:end),'ko', 'filled');
    hold on
    scatter(u0(1:N)'+stretch*mg(1:N,mode).*cos(ph(1:N,mode)+wt),u0(N+1:2*N)'+stretch*mg(N+1:2*N,mode).*cos(ph(N+1:2*N,mode)+wt),'go', 'filled');

    hold off
    %quiver(u(1:N)',u(N+1:2*N)',stretch*mg(1:N,mode).*cos(ph(1:N,mode)+wt),...
    %    stretch*mg(N+1:2*N,mode).*cos(ph(N+1:2*N,mode)+wt),0,'k','LineWidth',1)
        axis([-1.2*max(u0),1.2*max(u0),-1.2*max(u0),1.2*max(u0)])
        title(['Cyclotron Mode: ' num2str(mode)])
 %          writeVideo(vwr,getframe(gcf));
    pause(.001)
end
end
%close(vwr)


%% Radial Kinetic Energy vs Radius (new data loading)

PlanarKineticIons_rotframe = [];
R = [];

for i = 1:100:params(5)

    u = rotate(us(i,:),thetas(i));  % rotate back to spin down
    R = [R; sqrt(u(1:N).^2 + u(N+1:end).^2)]; % Find distance from origin
    v = spin_down(u,[vxs(i,:) vys(i,:)],params(2));
    vx = v(1:N);
    vy = v(N+1:end);
    PlanarKineticIons_rotframe = [PlanarKineticIons_rotframe; 0.5*m*(vx.^2+vy.^2)];
end

kB = 1.3806488e-23;

[Rsort ind] = sort(mean(R));
PlanarKinetic = mean(PlanarKineticIons_rotframe);
scatter(Rsort,PlanarKinetic/kB/1e-3)

%% Calculate PSDs
disp('Calculating PSDs')
freq = (0:0.5/(params(6)*params(7))/(params(5)/2):0.5/(params(6)*params(7)));
freq = 1.0e-6*freq(1:end-1); % chop of last one, because of Matlab ranges...

% Calculate PSD for Axial Motion
spectra = abs(fft(zs)).^2;
Zpsd = sum(spectra, 2);
Zpsd = Zpsd(1:(length(Zpsd)/2))+Zpsd(end:-1:length(Zpsd)/2+1);

% Calculate PSD for Planar Motion
motion = us - repmat(us(1,:),params(5),1); % subtract off equilibrium positions
spectra = abs(fft(motion)).^2;
Ppsd = sum(spectra, 2);
Ppsd = Ppsd(1:(length(Ppsd)/2))+Ppsd(end:-1:length(Ppsd)/2+1);

%% Plot PSDs

figure
semilogy(freq,Zpsd)
hold on
for i=1:params(1)
    plot([1e-6*wz/(2*pi)*Da(i) 1e-6*wz/(2*pi)*Da(i)],[1e-16,1],'g')
end

figure
semilogy(freq,Ppsd)
hold on

for i=1:params(1)
    plot([1e-6*wz/(2*pi)*Dp(i) 1e-6*wz/(2*pi)*Dp(i)],[1e-15,1e15],'g')
end
xlabel('Frequency MHz','FontSize',24)
ylabel('Planar PSD','FontSize',24)
set(gca,'FontSize',24)
    

%% Load Data through files - for some reason this doesn't work very well
clear all

FileLocation = 'D:\PenningSimulationData\2014_3_28_SmallCrystalModes\';  
setTrapParameters(0,0,0);
global N m wr wc q ke B wz V0 w G Vw ww M l0 v0 params
params = dlmread([FileLocation 'params.dat']);
setTrapParameters(params(2),-params(3)/G,params(1));
thetas = dlmread([FileLocation 'thetas.dat']);
disp('Loading Simulation Data')

us = zeros(params(5),2*params(1));
for i = 0:params(5)-1
    if ~mod(i,1000)
       disp(i)
    end
    filename =[FileLocation int2str(i) '.dat'];
    M = dlmread(filename);
    us(i+1,:) = convertPythonDataToMatlab(M);
    us(i+1,:) = rotate(us(i+1,:),-thetas(i+1));     
    us(i+1,:) = us(i+1,:) - us(1,:);
end

%% Radial Kinetic Energy vs Radius
clear all
setTrapParameters(0,0,0);
global G
FileLocation = 'D:\PenningSimulationData\2014_3_25_AxialTemp_LaserCooling\';   
params = dlmread([FileLocation 'params.dat']);
setTrapParameters(params(2),-params(3)/G,params(1));
thetas = dlmread([FileLocation 'thetas.dat']);
N = params(1);
global m
%PlanarKineticIons_rotframe = zeros(params(5),N);
PlanarKineticIons_rotframe = [];
R = [];
for i = 1:1000:params(5)
    
    filename =[FileLocation int2str(i-1) '.dat'];
    M = dlmread(filename);
    u = convertPythonDataToMatlab(M); % dimensionless positions
    %u = rotate(u,-thetas(i)); 
    R = [R; sqrt(u(1:N).^2 + u(N+1:end).^2)]; % Find distance from origin

    vx = M(4,:);
    vy = M(5,:);
    v = spin_down(u,[vx vy],params(2));
    vx = v(1:N);
    vy = v(N+1:end);
    
    %PlanarKineticIons_rotframe(i,:) = 0.5*m*(vx.^2+vy.^2);
    PlanarKineticIons_rotframe = [PlanarKineticIons_rotframe; 0.5*m*(vx.^2+vy.^2)];
    
    
    if ~mod(i-1,1000)
       disp(i)
    end

end

[Rsort ind] = sort(mean(R));
PlanarKinetic = mean(PlanarKineticIons_rotframe);
scatter(Rsort,PlanarKinetic/kB/1e-3)

%% Calculate Equilibrium Positions and Save for Python Simulation

setTrapParameters(54.5,-80,19);
global N
u0 = generateLattice(N,1);
u0 = rotate(u0,pi/2);     % get same major axis as dominics code
u0 = findEquilibrium(u0);
filename = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\MatlabData\19_54.5_-80_eq.dat';
pythonReadableU(u0,0,filename)


%% Compare PolyEig to Matrix Pencil Linearization

N = 19;
setTrapParameters(54.5,-80,N);
global N
u0 = generateLattice(N,1);
u0 = rotate(u0,pi/2);     % get same major axis as dominics code
u = findEquilibrium(u0);
[Ep,Dp,st,A,T] = normalModes(u,0); % Planar Modes
pencil = [1i*T A; -eye(2*N) zeros(2*N)];
[E, D] = eig(pencil);
D = diag(D);
D = real(D);
gz = (D>0);
E = E(:,gz);
D = D(gz);
[D ind] = sort(D);
E = E(:,ind); %sorted eigenvectors

for i=1:2*N
    for j=1:2*N
        ortho1(i,j) = dot(Ep(:,i),Ep(:,j));
        ortho2(i,j) = dot(E(1:38,i),E(1:38,j));
    end
end

real(E(1:2*N,mode))'*A*real(E(1:2*N,mode))
real(E(2*N+1:end,mode))'*real(E(2*N+1:end,mode))

real(Ep(:,mode))'*A*real(Ep(:,mode))
imag(Ep(:,mode))'*imag(Ep(:,mode))/Dp(mode)^2

% test = -eig(A);
% 
% l=1;
% k=2;
% %sum((Dp(l)*Dp(k) + test'.^2).*(conj(Ep(:,l)).*Ep(:,k)))
% ortho = 0;
% for i=1:2*19
%    ortho = ortho + (Dp(l)*Dp(k)+ test(i)^2)*(conj(Ep(i,l))*Ep(i,k));
% end
