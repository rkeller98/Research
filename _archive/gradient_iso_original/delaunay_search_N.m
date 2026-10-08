function iso_points = delaunay_search_N(X, search_dim, iso_val, DT, valid_vectors)
%DELAUNAY_SEARCH_N Computes isocontour points of a scalar field over a
%Delaunay triangulation in N-dimensional space.
%
%   This function interpolates points along the edges of the simplices
%   defined by the Delaunay triangulation `DT` such that the scalar field
%   (given by column `search_dim` of `X`) equals a specified `iso_val`.
%
%   The scalar field is assumed to be defined over a (d???1)-dimensional
%   domain, where d = size(DT,2). The triangulation `DT` must be obtained
%   using delaunayn(X_domain), where X_domain consists of the first d???1 
%   dimensions of X.
%
%   INPUTS:
%       X           - An N-by-D matrix where each row corresponds to a data point.
%                     The first (d???1) columns (where d = size(DT,2)) define the
%                     domain used to construct the Delaunay triangulation.
%                     The remaining columns can hold scalar or vector field values.
%
%       search_dim  - The column index in X corresponding to the scalar field
%                     used for isocontouring. Must satisfy:
%                           size(DT,2) <= search_dim <= size(X,2)
%
%       iso_val     - Scalar value defining the isocontour level to extract.
%
%       DT          - The connectivity matrix of the Delaunay triangulation
%                     (as returned by delaunayn). Each row represents a simplex
%                     by listing the indices of its vertices in X.
%
%       valid_vectors - (Optional) A logical matrix indicating which edges within
%                       the triangulation should be considered valid for interpolation.
%                       This matrix is typically returned by the function
%                       `get_valid_triangulation_vectors`. It serves to exclude
%                       poorly defined edges ??? for instance, edges that are
%                       excessively long and would yield unreliable interpolation
%                       results. If not provided, all edges are considered valid.
%
%   OUTPUT:
%       iso_points  - An M-by-D matrix containing the interpolated points where
%                     the scalar field equals `iso_val`. These points lie on
%                     the edges of the Delaunay simplices and are returned in
%                     the full D-dimensional space (including all columns of X).
    if nargin < 5
        valid_vectors = true; 
    end 
        

    persistent per_vertex_pairs vp1 vp2 last_dim
    
    N_dim = size(DT, 2); 
    
    if isempty(per_vertex_pairs)
        % Initialize persistent variables
        per_vertex_pairs = containers.Map('KeyType', 'double', 'ValueType', 'any');
        vp1 = [];
        vp2 = [];
        last_dim = -1; % Use an invalid dimension to force first update
    end
    
    % Only update if the dimension has changed
    if N_dim ~= last_dim
        if ~isKey(per_vertex_pairs, N_dim)
            % Compute and store vertex pairs for the new dimension
            per_vertex_pairs(N_dim) = nchoosek(1:N_dim, 2);
        end
        vertex_pairs = per_vertex_pairs(N_dim);
        vp1 = vertex_pairs(:,1);
        vp2 = vertex_pairs(:,2);
        
        % Update the last used dimension
        last_dim = N_dim;
    end

    % Extract the scalar field values at the Delaunay triangulation vertices
    target_values = X(:, search_dim);
    target_points = target_values(DT);

    % Compute interpolation factors (lambda) along each edge
    numerator_diffs = iso_val - target_points(:, vp1);
    denominator_diffs = target_points(:, vp2) - target_points(:, vp1);
    lambda = numerator_diffs ./ denominator_diffs;

    % Determine which interpolated points lie within the edge bounds
    valid_lambda = (lambda >= 0) & (lambda <= 1) & valid_vectors;

    % Number of valid isocontour points
    num_valid = sum(valid_lambda(:));

    % Preallocate output matrix and insert known scalar value
    N_rows = size(X,2); 
    iso_points = NaN(num_valid, N_rows);
    iso_points(:, search_dim) = iso_val;

    % Prepare list of dimensions to interpolate (excluding search_dim)
    dim_vec = 1:N_rows;
    dim_vec(dim_vec == search_dim) = [];

    % Interpolate all other dimensions for valid isocontour points
    for dim_idx = dim_vec
        dim_values = X(:, dim_idx);
        dim_points = dim_values(DT);
        start_points = dim_points(:, vp1);
        direction_vectors = dim_points(:, vp2) - start_points;
        interpolated_points = start_points + lambda .* direction_vectors;

        % Extract only valid interpolated values
        iso_points(:, dim_idx) = interpolated_points(valid_lambda);
    end
end
