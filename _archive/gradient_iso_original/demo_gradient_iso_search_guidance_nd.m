function demo_gradient_iso_search_guidance_nd()
%DEMO_GRADIENT_ISO_SEARCH_GUIDANCE_ND
% Generic N-D demo for search guidance from scalar potential samples.

    rng(21);

    d = 4;
    N = 1400;
    lim = [-5.12, 5.12];

    X = lim(1) + (lim(2)-lim(1))*rand(N, d);
    F = 10*d + sum(X.^2 - 10*cos(2*pi*X), 2);
    F = F + 0.02*std(F)*randn(size(F));

    opts = struct();
    opts.M = 28;
    opts.validity_range = 3;
    opts.point_mode = 'centroid';
    opts.sigma_factor = 1.0;

    res = gradient_iso_pipeline_nd(X, F, 2, opts);

    G = res.search_guidance;
    D = res.derivatives;

    fprintf('\n=== Generic N-D Search Guidance Demo ===\n');
    fprintf('d=%d, N=%d\n', d, N);
    fprintf('Guidance points: %d\n', size(G.points,1));
    fprintf('Mean confidence: %.4f\n', mean(G.confidence));
    fprintf('Mean step size: %.4f\n', mean(G.step_size));
    fprintf('Mean improvement proxy: %.4f\n', mean(G.improvement_proxy));

    if isfield(D, 'laplacian')
        fprintf('Laplacian stats (mean/std): %.4f / %.4f\n', ...
            mean(D.laplacian.values), std(D.laplacian.values));
    end

    % 2D projection for visual intuition (first two coordinates only)
    figure('Name','Generic N-D Search Guidance (2D projection)');

    subplot(1,2,1);
    scatter(G.points(:,1), G.points(:,2), 9, G.confidence, 'filled');
    axis equal tight; colorbar;
    title('Confidence on Guidance Points');
    xlabel('x1'); ylabel('x2');

    subplot(1,2,2);
    qidx = 1:max(1,floor(size(G.points,1)/500)):size(G.points,1);
    quiver(G.points(qidx,1), G.points(qidx,2), ...
           G.direction_maximize(qidx,1), G.direction_maximize(qidx,2), ...
           0.9, 'k');
    axis equal tight;
    title('Maximization Direction (projected)');
    xlabel('x1'); ylabel('x2');
end
