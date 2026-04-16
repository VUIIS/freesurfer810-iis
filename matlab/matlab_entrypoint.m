function matlab_entrypoint(varargin)

fcn = varargin{2};

feval(fcn,varargin{3:end});

