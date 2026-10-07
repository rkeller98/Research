function demo_himmelblau_gradient_iso()
%DEMO_HIMMELBLAU_GRADIENT_ISO Demonstrates gradient-iso pipeline on Himmelblau.

    rng(7);

    n = 1200;
    x = -6 + 12*rand(n,1);
    y = -6 + 12*rand(n,1);

    f = (x.^2 + y - 11).^2 + (x + y.^2 - 7).^2;

    noise = 0.05 * std(f) * randn(size(f));
    f_noisy = f + noise;

    XYF = [x, y, f_noisy];

    result = gradient_iso_pipeline_2d(XYF, 30, 3, 1.0, 'centroid');

    figure('Name','Gradient Iso Pipeline - Himmelblau');

    subplot(2,2,1);
    scatter(x, y, 8, f_noisy, 'filled');
    axis equal tight;
    title('Punktewolke mit f(x,y)');
    xlabel('x'); ylabel('y'); colorbar;

    subplot(2,2,2);
    quiver(result.centroid_gradients(:,1), result.centroid_gradients(:,2), ...
           result.centroid_gradients(:,3), result.centroid_gradients(:,4), 1.2, 'k');
    axis equal tight;
    title('Gradientenvektorfeld (Simplex-basiert)');
    xlabel('x'); ylabel('y');

    subplot(2,2,3);
    scatter(result.centroid_gradients(:,1), result.centroid_gradients(:,2), ...
            10, result.confidence_score, 'filled');
    axis equal tight;
    title('Konfidenzscore (gauss-basiert)');
    xlabel('x'); ylabel('y'); colorbar;

    subplot(2,2,4);
    sel = result.confidence_mask;
    scatter(result.centroid_gradients(:,1), result.centroid_gradients(:,2), 8, [0.8 0.8 0.8], 'filled');
    hold on;
    scatter(result.centroid_gradients(sel,1), result.centroid_gradients(sel,2), 16, 'r', 'filled');
    axis equal tight;
    title('Konfidenzmaske (mu + sigma)');
    xlabel('x'); ylabel('y');
end
