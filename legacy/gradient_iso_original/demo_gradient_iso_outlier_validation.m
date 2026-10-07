function demo_gradient_iso_outlier_validation()
%DEMO_GRADIENT_ISO_OUTLIER_VALIDATION
%   Clear validation demo with synthetic outliers and quantitative metrics.

    rng(12);

    n_in = 1400;
    x_in = -6 + 12*rand(n_in,1);
    y_in = -6 + 12*rand(n_in,1);
    f_in = (x_in.^2 + y_in - 11).^2 + (x_in + y_in.^2 - 7).^2;
    f_in = f_in + 0.02*std(f_in)*randn(size(f_in));

    n_out = 120;
    x_out = -6 + 12*rand(n_out,1);
    y_out = -6 + 12*rand(n_out,1);
    f_clean_out = (x_out.^2 + y_out - 11).^2 + (x_out + y_out.^2 - 7).^2;
    f_out = f_clean_out + 1.2*std(f_in).*sign(randn(n_out,1)).*(1 + 0.5*rand(n_out,1));

    X = [x_in; x_out];
    Y = [y_in; y_out];
    F = [f_in; f_out];
    is_outlier_gt = [false(n_in,1); true(n_out,1)];

    opts = struct();
    opts.M = 28;
    opts.validity_range = 3;
    opts.point_mode = 'centroid';
    opts.sigma_factor = 1.0;

    res = gradient_iso_pipeline_nd([X,Y], F, 1, opts);
    pts = res.orders{2}.domain_points;
    score = res.confidence.score;
    inlier_mask = res.confidence.mask;

    gt_at_pts = knnsearch([X,Y], pts);
    gt_out = is_outlier_gt(gt_at_pts);
    pred_out = ~inlier_mask;

    tp = sum(pred_out & gt_out);
    fp = sum(pred_out & ~gt_out);
    fn = sum(~pred_out & gt_out);
    tn = sum(~pred_out & ~gt_out);

    precision = tp / max(tp + fp, 1);
    recall = tp / max(tp + fn, 1);
    f1 = 2*precision*recall / max(precision + recall, eps);

    figure('Name','Gradient-Iso Outlier Validation');

    subplot(2,2,1);
    scatter(X(~is_outlier_gt), Y(~is_outlier_gt), 9, [0.70 0.70 0.70], 'filled');
    hold on;
    scatter(X(is_outlier_gt), Y(is_outlier_gt), 16, [0.95 0.25 0.25], 'filled');
    axis equal tight;
    title('Ground Truth: Outlier = rot');
    xlabel('x'); ylabel('y');

    subplot(2,2,2);
    qidx = 1:6:size(pts,1);
    g = res.orders{2}.values(:,1:2);
    quiver(pts(qidx,1), pts(qidx,2), g(qidx,1), g(qidx,2), 2.2, 'k');
    axis equal tight;
    title('Gradientenfeld (ausgeduennt)');
    xlabel('x'); ylabel('y');

    subplot(2,2,3);
    scatter(pts(:,1), pts(:,2), 12, score, 'filled');
    axis equal tight;
    colorbar;
    title(sprintf('Konfidenzscore (thr = %.4g)', res.confidence.threshold));
    xlabel('x'); ylabel('y');

    subplot(2,2,4);
    scatter(pts(pred_out,1), pts(pred_out,2), 16, [0.95 0.25 0.25], 'filled');
    hold on;
    scatter(pts(~pred_out,1), pts(~pred_out,2), 9, [0.70 0.70 0.70], 'filled');
    axis equal tight;
    title(sprintf('Vorhersage: Outlier = rot | P=%.2f R=%.2f F1=%.2f', precision, recall, f1));
    xlabel('x'); ylabel('y');

    fprintf('\n=== Gradient-Iso Outlier Validation ===\n');
    fprintf('TP=%d  FP=%d  FN=%d  TN=%d\n', tp, fp, fn, tn);
    fprintf('Precision=%.4f  Recall=%.4f  F1=%.4f\n\n', precision, recall, f1);
end
