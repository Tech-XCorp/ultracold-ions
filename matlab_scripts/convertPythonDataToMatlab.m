% Convert python data file and to format for matlab scripts
%
% Read parameters first and call setTrapParameters()

function u = convertPythonDataToMatlab(M)

global l0

%M = dlmread(filename);
u = M(1,:);     % First column is x values
u = [u M(2,:)]; % Second column is y values, append to u
u = u/l0;  % Divide by characteristic length

end

