%%
%% init_playrec(fs)
% Initialize playrec for the current setup
% Input: 
% sampling freq

% Dependencies: playrec.mexw64 

function init_playrec(fs)

    if playrec('isInitialised')
        playrec('reset');
    end

    playrec('init',fs,0,0)

    disp('Playrec successfully initialized!')
end

