% quickly display snapshots of simulation to make a "movie"

FileLocation = 'C:\Users\ACKWinDesk\Documents\GitHub\ultracold-ions-notes\axialPhononSpectra\data\run4extra\';
setTrapParameters(44,160,127);
global w % get rotation velocity
%dt = 5.0e-9;
dt = 1.26770e-6;
delta_theta = w*dt;

filename =[FileLocation 'run4_0.dat'];
M = dlmread(filename);
u = convertPythonDataToMatlab(M);
%theta = findTheta(u);
%theta = 1.6228; %original run4
theta = 0.9896;  % run4 extra
u = rotate(u,theta);            % rotate to that config

figure(1)
scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
axis([-25,25,-25,25])
figure(2)
scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
axis([-25,25,-25,25])
pause(.1)

disp('Found theta_0')
for i = 1:1999
    theta = theta + delta_theta;
    filename =[FileLocation 'run4_' int2str(i) '.dat'];
    M = dlmread(filename);
    u = convertPythonDataToMatlab(M);
    figure(1)
    scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
    axis([-25,25,-25,25])
    
    u = rotate(u,theta);            % rotate to that config
    
    figure(2)
    scatter(u(1:end/2),u(end/2+1:end),'ko', 'filled');
    axis([-25,25,-25,25])
    pause(.1)

end

