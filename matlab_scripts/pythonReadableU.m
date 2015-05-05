% Save configuration in data file in format that dominics code can read it
%
% Call setTrapParameters()

function pythonReadableU( u, saveas)

global N l0 q m

u = u*l0;

M = zeros(8,N);
M(1,:) = u(1:N);
M(2,:) = u(N+1:end);
% M(3,:); % keep zero
% same for 4-6 no momentum

M(7,:) = q*ones(1,N);
M(8,:) = m*ones(1,N);

dlmwrite(saveas,M,' ');

end

