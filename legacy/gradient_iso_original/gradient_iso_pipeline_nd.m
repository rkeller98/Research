function result = gradient_iso_pipeline_nd(X, f, approx_order, opts)
%GRADIENT_ISO_PIPELINE_ND
%   General N-dimensional derivative approximation from point clouds using
%   local simplex-wise affine fits and iso-search over derivative components.
%
% INPUT
%   X             [N x d] domain points
%   f             [N x 1] scalar field values
%   approx_order  derivative order K (K>=1)
%   opts          struct with optional fields:
%                 .M              number of iso-levels per component (default 25)
%                 .validity_range  edge filter factor for valid_vectors (default 3)
%                 .point_mode      'centroid' | 'circumcenter' (default 'centroid')
%                 .sigma_factor    threshold = mean + sigma*std (default 1)
%                 .bandwidth       gaussian density bandwidth (default auto)
%
% OUTPUT
%   result.orders{k+1} for k=0..approx_order
%     k=0: original field on X
%     k>=1: derivative tensor components of order k, sampled at simplex reps
%   result.confidence: confidence info for highest order derivative level

    if nargin < 4
        opts = struct();
    end

    validateattributes(X, {'numeric'}, {'2d','finite','real'});
    validateattributes(f, {'numeric'}, {'column','finite','real'});
    if size(X,1) ~= size(f,1)
        error('X und f muessen gleich viele Zeilen haben.');
    end
    validateattributes(approx_order, {'numeric'}, {'scalar','integer','>=',1});

    d = size(X,2);
    N = size(X,1);
    if N < d + 1
        error('Zu wenige Punkte fuer eine %d-dimensionale Delaunay-Triangulation.', d);
    end

    M = get_opt(opts, 'M', 25);
    validity_range = get_opt(opts, 'validity_range', 3);
    point_mode = lower(string(get_opt(opts, 'point_mode', 'centroid')));
    sigma_factor = get_opt(opts, 'sigma_factor', 1);
    bandwidth_user = get_opt(opts, 'bandwidth', []);

    validateattributes(M, {'numeric'}, {'scalar','integer','>=',2});
    validateattributes(validity_range, {'numeric'}, {'scalar','positive'});
    validateattributes(sigma_factor, {'numeric'}, {'scalar','real'});

    if point_mode ~= "centroid" && point_mode ~= "circumcenter"
        error('point_mode muss ''centroid'' oder ''circumcenter'' sein.');
    end

    orders = cell(approx_order + 1, 1);

    level0 = struct();
    level0.order = 0;
    level0.domain_points = X;
    level0.values = f;
    level0.component_labels = {"f"};
    level0.triangulation = delaunayn(X);
    level0.valid_vectors = [];
    level0.iso = [];
    orders{1} = level0;

    current_X = X;
    current_V = f;
    current_labels = {"f"};

    for ord = 1:approx_order
        DT = delaunayn(current_X);
        n_simplex = size(DT,1);
        n_comp_prev = size(current_V,2);

        reps = NaN(n_simplex, d);
        grads = NaN(n_simplex, n_comp_prev * d);
        keep = false(n_simplex, 1);

        for s = 1:n_simplex
            ids = DT(s,:);
            pts = current_X(ids,:);
            rep = get_simplex_point(pts, point_mode);

            A = [pts, ones(size(pts,1),1)];
            if rank(A) < d + 1
                continue;
            end

            grad_row = NaN(1, n_comp_prev * d);
            ok = true;
            for c = 1:n_comp_prev
                vals = current_V(ids, c);
                coeff = A \ vals;
                g = coeff(1:d).';
                if any(~isfinite(g))
                    ok = false;
                    break;
                end
                idx0 = (c-1)*d + 1;
                grad_row(idx0:idx0+d-1) = g;
            end

            if ok && all(isfinite(rep))
                reps(s,:) = rep;
                grads(s,:) = grad_row;
                keep(s) = true;
            end
        end

        reps = reps(keep,:);
        grads = grads(keep,:);

        if size(reps,1) < d + 1
            error('Ableitungsordnung %d: Zu wenige gueltige Stuetzpunkte.', ord);
        end

        DT_rep = delaunayn(reps);
        packed = [reps, grads];
        [valid_vectors, mean_edge_length] = get_valid_triangulation_vectors(packed, DT_rep, validity_range);

        labels = build_component_labels(current_labels, d);
        iso = build_iso_bundle(packed, d, labels, M, DT_rep, valid_vectors);

        level = struct();
        level.order = ord;
        level.domain_points = reps;
        level.values = grads;
        level.component_labels = labels;
        level.triangulation = DT_rep;
        level.valid_vectors = valid_vectors;
        level.iso = iso;
        level.mean_edge_length = mean_edge_length;
        orders{ord+1} = level;

        current_X = reps;
        current_V = grads;
        current_labels = labels;
    end

    top = orders{end};
    bw = bandwidth_user;
    if isempty(bw)
        bw = max(top.mean_edge_length, eps);
    end
    confidence = compute_confidence(top.domain_points, top.iso, d, sigma_factor, bw);

    result = struct();
    result.dimension = d;
    result.approx_order = approx_order;
    result.options = struct('M',M,'validity_range',validity_range,'point_mode',char(point_mode), ...
                            'sigma_factor',sigma_factor,'bandwidth',bw);
    result.orders = orders;
    result.confidence = confidence;

    if d == 2 && approx_order >= 1
        g = orders{2}.values;
        if size(g,2) >= 2
            result.vector_field = struct();
            result.vector_field.points = orders{2}.domain_points;
            result.vector_field.grad = g(:,1:2);
        end
    end

    result.derivatives = build_derivative_outputs(orders, d, approx_order);
    result.search_guidance = build_search_guidance(orders, confidence, d, approx_order);
end

function val = get_opt(opts, name, default_val)
    if isfield(opts, name)
        val = opts.(name);
    else
        val = default_val;
    end
end

function rep = get_simplex_point(pts, mode)
    rep = mean(pts,1);
    if mode == "circumcenter"
        p1 = pts(1,:).';
        A = 2 * (pts(2:end,:) - pts(1,:));
        b = sum(pts(2:end,:).^2, 2) - sum(pts(1,:).^2, 2);
        if rank(A) == size(A,2)
            c = A \ b;
            rep = c(:).';
        end
    end
end

function labels = build_component_labels(prev_labels, d)
    axes = cell(1,d);
    for j = 1:d
        axes{j} = sprintf('x%d', j);
    end

    labels = cell(numel(prev_labels) * d, 1);
    idx = 1;
    for p = 1:numel(prev_labels)
        base = prev_labels{p};
        for j = 1:d
            labels{idx} = sprintf('d(%s)/d%s', base, axes{j});
            idx = idx + 1;
        end
    end
end

function iso = build_iso_bundle(packed, d, labels, M, DT, valid_vectors)
    n_comp = numel(labels);
    iso_levels = cell(n_comp,1);
    iso_points = cell(n_comp,1);

    for c = 1:n_comp
        search_dim = d + c;
        v = packed(:, search_dim);
        lv = linspace(min(v), max(v), M);
        iso_levels{c} = lv;
        iso_points{c} = cell(M,1);
        for m = 1:M
            iso_points{c}{m} = delaunay_search_N(packed, search_dim, lv(m), DT, valid_vectors);
        end
    end

    iso = struct();
    iso.levels = iso_levels;
    iso.points = iso_points;
    iso.labels = labels;
end

function conf = compute_confidence(domain_points, iso, d, sigma_factor, bandwidth)
    n = size(domain_points,1);
    n_comp = numel(iso.labels);
    comp_scores = zeros(n, n_comp);

    for c = 1:n_comp
        P = [];
        for m = 1:numel(iso.points{c})
            pm = iso.points{c}{m};
            if ~isempty(pm)
                P = [P; pm(:,1:d)]; %#ok<AGROW>
            end
        end

        if isempty(P)
            continue;
        end

        for i = 1:n
            dp = P - domain_points(i,:);
            dist2 = sum(dp.^2, 2);
            comp_scores(i,c) = mean(exp(-dist2 / (2*bandwidth^2)));
        end
    end

    score = exp(mean(log(comp_scores + eps), 2));
    mu = mean(score);
    sig = std(score);
    thr = mu + sigma_factor * sig;
    mask = score >= thr;

    conf = struct();
    conf.score = score;
    conf.mean = mu;
    conf.std = sig;
    conf.threshold = thr;
    conf.mask = mask;
end

function deriv = build_derivative_outputs(orders, d, approx_order)
    deriv = struct();

    if approx_order >= 1
        l1 = orders{2};
        deriv.gradient = struct();
        deriv.gradient.points = l1.domain_points;
        deriv.gradient.values = l1.values(:,1:d);
        deriv.gradient.labels = l1.component_labels(1:d);
    end

    if approx_order >= 2
        l2 = orders{3};
        n = size(l2.values,1);
        hess = NaN(d, d, n);
        lap = NaN(n,1);

        for i = 1:n
            block = l2.values(i,1:d*d);
            H = reshape(block, [d, d]).';
            hess(:,:,i) = H;
            lap(i) = trace(H);
        end

        deriv.hessian = struct();
        deriv.hessian.points = l2.domain_points;
        deriv.hessian.values = hess;

        deriv.laplacian = struct();
        deriv.laplacian.points = l2.domain_points;
        deriv.laplacian.values = lap;
    end
end

function guide = build_search_guidance(orders, confidence, d, approx_order)
    guide = struct();

    if approx_order < 1
        guide.available = false;
        guide.reason = 'approx_order muss >= 1 sein.';
        return;
    end

    l1 = orders{2};
    pts = l1.domain_points;
    g = l1.values(:,1:d);
    gnorm = sqrt(sum(g.^2, 2));
    dir_max = g ./ (gnorm + eps);
    dir_min = -dir_max;

    base_step = max(l1.mean_edge_length, eps);

    conf_pts = confidence.score;
    conf_at_l1 = conf_pts;
    top_pts = orders{end}.domain_points;
    if size(top_pts,1) ~= size(pts,1) || any(size(top_pts) ~= size(pts))
        idx = dsearchn(top_pts, pts);
        conf_at_l1 = conf_pts(idx);
    end

    conf_at_l1 = conf_at_l1(:);
    cmax = max(conf_at_l1);
    if cmax <= eps
        cmax = 1;
    end
    conf_norm = conf_at_l1 / cmax;

    step = base_step .* (0.25 + 0.75 * conf_norm);
    x_next_max = pts + dir_max .* step;
    x_next_min = pts + dir_min .* step;

    improve_proxy = gnorm .* step .* conf_norm;

    guide.available = true;
    guide.points = pts;
    guide.gradient = g;
    guide.gradient_norm = gnorm;
    guide.direction_maximize = dir_max;
    guide.direction_minimize = dir_min;
    guide.confidence = conf_at_l1;
    guide.step_size = step;
    guide.next_point_maximize = x_next_max;
    guide.next_point_minimize = x_next_min;
    guide.improvement_proxy = improve_proxy;
    guide.notes = ['All outputs are N-dimensional and model-agnostic. ', ...
                   'Use direction_* and next_point_* for search proposals; ', ...
                   'use confidence to gate risky updates.'];
end
