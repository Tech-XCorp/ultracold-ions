% Quickly display snapshots of simulation to make a "movie"

cleanupObj = onCleanup(@CLEAN);

%FileLocation = 'C:\Users\ACKWinDesk\Documents\GitHub\ultracold-ions-notes\axialPhononSpectra\data\run4extra\';
FileLocation = 'C:\Users\ACKWinDesk\Desktop\PenningSimulationData\2014_1_15_4\';
setTrapParameters(44,160,127);
%global w % get rotation velocity
%dt = 5.0e-9;
%delta_theta = w*dt;

thetas = dlmread([FileLocation 'thetas.dat']);
%filename =[FileLocation 'run4_0.dat'];
%filename =[FileLocation '0.dat'];
%M = dlmread(filename);
%u = convertPythonDataToMatlab(M);
%theta = findTheta(u);
%theta = 1.6228; %original run4
%theta = 0.9896;  % run4 extra
%theta = 0.5850 * pi;
%u = rotate(u,theta);            % rotate to that config
%u = rotate(u,thetas(1));            % rotate to that config

%figure(1)
%scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
%axis([-25,25,-25,25])
% figure(2)
% scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
% axis([-25,25,-25,25])
% pause(.01)

vidpath = 'RotatingFrame127';
%vidpath = 'LabFrame127';
%vwr = VideoWriter(vidpath, 'Motion JPEG AVI');
%open(vwr);


for i = 2000:4999
%    theta = theta + delta_theta;
 %   filename =[FileLocation 'run4_' int2str(i) '.dat'];
    %filename =[FileLocation int2str(i) '_*.dat'];
    filename =[FileLocation int2str(i) '.dat'];
    M = dlmread(filename);
    u = convertPythonDataToMatlab(M);
  %  figure(1)
   % scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
   % axis([-25,25,-25,25])
    
   % u = rotate(u,theta);            % rotate to that config
    u = rotate(u,-thetas(i+1));            % rotate to that config
    
    figure(2)
    scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
    axis([-25,25,-25,25])
    %title('Lab Frame, N = 127, delta = 0.0036, w = 44 kHz, ')
    title('Rotating Frame, N = 127, delta = 0.0036, w = 44 kHz, ')
    xlabel('Scaled position')
    pause(.00001)

    %writeVideo(vwr,getframe(gcf));
    clf

end
%close(vwr);
