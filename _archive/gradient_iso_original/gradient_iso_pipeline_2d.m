function result = gradient_iso_pipeline_2d(XYF, M, validity_range, sigma_factor, point_mode)
%GRADIENT_ISO_PIPELINE_2D Backward-compatible 2D wrapper around ND pipeline.

    if nargin < 2 || isempty(M), M = 25; end
    if nargin < 3 || isempty(validity_range), validity_range = 3; end
    if nargin < 4 || isempty(sigma_factor), sigma_factor = 1; end
    if nargin < 5 || isempty(point_mode), point_mode = 'centroid'; end

    validateattributes(XYF, {'numeric'}, {'2d','ncols',3,'finite','real'});

    X = XYF(:,1:2);
    f = XYF(:,3);

    opts = struct();
    opts.M = M;
    opts.validity_range = validity_range;
    opts.sigma_factor = sigma_factor;
    opts.point_mode = point_mode;

    nd = gradient_iso_pipeline_nd(X, f, 1, opts);
    lvl1 = nd.orders{2};

    result = struct();
    result.triangles = nd.orders{1}.triangulation;
    result.centroid_gradients = [lvl1.domain_points, lvl1.values(:,1:2)];
    result.iso_levels_dfdx = lvl1.iso.levels{1};
    result.iso_levels_dfdy = lvl1.iso.levels{2};
    result.iso_points_dfdx = lvl1.iso.points{1};
    result.iso_points_dfdy = lvl1.iso.points{2};
    result.confidence_score = nd.confidence.score;
    result.confidence_mask = nd.confidence.mask;
    result.confidence_threshold = nd.confidence.threshold;
    result.nd_result = nd;
end
