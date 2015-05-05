% Get z positions for axial mode i at time zero, phase zero
%
% mode can be vector of modes - will get superposition of modes for z
%
% call setTrapParameters!

function z = getZforAxialMode(u,mode)

E = normalModes(u,1);
N = length(u)/2;

if (mode == 'all')
    mode=1:N;
end

zmax = 1e-7/length(mode);     % largest z value to have in crystal

z = zeros(N,1);

for m = mode
    z = z + E(:,m)/max(abs(E(:,m)))*zmax; % scale 
end
        
end



