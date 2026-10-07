function demo_himmelblau_gradient_iso_nd()
%DEMO_HIMMELBLAU_GRADIENT_ISO_ND Example usage of the N-D pipeline in 2D.

    rng(7);

    n = 1500;
    x = -6 + 12*rand(n,1);
    y = -6 + 12*rand(n,1);
    f = (x.^2 + y - 11).^2 + (x + y.^2 - 7).^2;
    f = f + 0.05*std(f)*randn(size(f));

    X = [x, y];

    opts = struct();
    opts.M = 30;
    opts.validity_range = 3;
    opts.point_mode = 'centroid';      % or 'circumcenter'
    opts.sigma_factor = 1.0;           % threshold = mean + 1*sigma

    result = gradient_iso_pipeline_nd(X, f, 2, opts);

    first = result.orders{2};
    pts = first.domain_points;
    g = first.values(:,1:2);

    figure('Name','N-D Gradient Iso Pipeline (Himmelblau)');

    subplot(1,2,1);
    quiver(pts(:,1), pts(:,2), g(:,1), g(:,2), 1.1, 'k');
    axis equal tight;
    xlabel('x'); ylabel('y');
    title('1. Ordnung: Gradientenfeld');

    subplot(1,2,2);
    scatter(pts(:,1), pts(:,2), 10, result.confidence.score, 'filled');
    hold on;
    sel = result.confidence.mask;
    scatter(pts(sel,1), pts(sel,2), 20, 'r', 'filled');
    axis equal tight;
    xlabel('x'); ylabel('y'); colorbar;
    title('Konfidenzscore + Maske (rot)');
end
