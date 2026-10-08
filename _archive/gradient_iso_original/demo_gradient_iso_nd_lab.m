function demo_gradient_iso_nd_lab()
%DEMO_GRADIENT_ISO_ND_LAB
% Interactive lab demo for N-D gradient-iso outlier detection.
%
% What this lab shows:
%   1) Synthetic point cloud from a selectable benchmark function.
%   2) Injected outliers in function values f(x).
%   3) N-D Delaunay-based derivative approximation via gradient_iso_pipeline_nd.
%   4) Confidence score derived from iso-derivative point density.
%   5) Outlier prediction and classification metrics (P/R/F1, ROC, PR).
%
% Practical reading:
%   - "Ground Truth": red points are true injected outliers.
%   - "Prediction": red points are predicted outliers (low confidence).
%   - Good setup: high Precision + high Recall + high F1.

    s = struct();
    s.basis_list = {'Himmelblau','Rosenbrock (Banana)','Rastrigin','Sphere','Ackley'};
    s.basis = 'Himmelblau';
    s.d = 2;
    s.n = 1800;
    s.order = 1;
    s.M = 28;
    s.validity = 3.0;
    s.sigma = 1.0;
    s.noise = 0.03;
    s.outlier_frac = 0.08;
    s.outlier_strength = 1.4;
    s.seed = 11;

    f = figure('Name','Gradient-Iso N-D Lab','Color',[0.08 0.09 0.11], ...
               'NumberTitle','off','Position',[40 40 1550 900]);

    ctrl = uipanel(f,'Title','Controls','FontSize',10,'ForegroundColor',[0.95 0.95 0.95], ...
                   'BackgroundColor',[0.12 0.13 0.16],'Position',[0.01 0.02 0.21 0.96]);

    mklabel(ctrl, 'Basis Function', [0.05 0.93 0.90 0.04]);
    hBasis = uicontrol(ctrl,'Style','popupmenu','Units','normalized','Position',[0.05 0.89 0.90 0.04], ...
                       'String',s.basis_list,'Value',1,'Callback',@onBasisChange);

    mklabel(ctrl, 'Dimension d', [0.05 0.84 0.90 0.04]);
    hDim = uicontrol(ctrl,'Style','edit','Units','normalized','Position',[0.05 0.80 0.90 0.04], ...
                     'String',num2str(s.d));

    mklabel(ctrl, 'Samples N', [0.05 0.75 0.90 0.04]);
    hN = uicontrol(ctrl,'Style','edit','Units','normalized','Position',[0.05 0.71 0.90 0.04], ...
                   'String',num2str(s.n));

    mklabel(ctrl, 'Approx Order K', [0.05 0.66 0.90 0.04]);
    hOrd = uicontrol(ctrl,'Style','edit','Units','normalized','Position',[0.05 0.62 0.90 0.04], ...
                     'String',num2str(s.order));

    mklabel(ctrl, 'Iso Levels M', [0.05 0.57 0.90 0.04]);
    hM = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.54 0.70 0.03], ...
                   'Min',8,'Max',60,'Value',s.M,'SliderStep',[1/52 4/52]);
    hMtxt = mkval(ctrl, s.M, [0.78 0.54 0.17 0.03]);

    mklabel(ctrl, 'Validity Range', [0.05 0.49 0.90 0.04]);
    hVal = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.46 0.70 0.03], ...
                     'Min',1.2,'Max',6.0,'Value',s.validity,'SliderStep',[0.02 0.10]);
    hValtxt = mkval(ctrl, s.validity, [0.78 0.46 0.17 0.03]);

    mklabel(ctrl, 'Sigma Factor', [0.05 0.41 0.90 0.04]);
    hSigma = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.38 0.70 0.03], ...
                       'Min',-1.0,'Max',3.0,'Value',s.sigma,'SliderStep',[0.01 0.08]);
    hSigmatxt = mkval(ctrl, s.sigma, [0.78 0.38 0.17 0.03]);

    mklabel(ctrl, 'Noise Level', [0.05 0.33 0.90 0.04]);
    hNoise = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.30 0.70 0.03], ...
                       'Min',0.0,'Max',0.2,'Value',s.noise,'SliderStep',[0.01 0.10]);
    hNoisetxt = mkval(ctrl, s.noise, [0.78 0.30 0.17 0.03]);

    mklabel(ctrl, 'Outlier Fraction', [0.05 0.25 0.90 0.04]);
    hFrac = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.22 0.70 0.03], ...
                      'Min',0.0,'Max',0.30,'Value',s.outlier_frac,'SliderStep',[0.01 0.08]);
    hFractxt = mkval(ctrl, s.outlier_frac, [0.78 0.22 0.17 0.03]);

    mklabel(ctrl, 'Outlier Strength', [0.05 0.17 0.90 0.04]);
    hStr = uicontrol(ctrl,'Style','slider','Units','normalized','Position',[0.05 0.14 0.70 0.03], ...
                     'Min',0.3,'Max',3.0,'Value',s.outlier_strength,'SliderStep',[0.01 0.10]);
    hStrtxt = mkval(ctrl, s.outlier_strength, [0.78 0.14 0.17 0.03]);

    hRun = uicontrol(ctrl,'Style','pushbutton','Units','normalized','Position',[0.05 0.08 0.90 0.045], ...
                     'String','Run / Refresh','FontWeight','bold','Callback',@onRun);

    hInfo = uicontrol(ctrl,'Style','text','Units','normalized','Position',[0.05 0.01 0.90 0.06], ...
                      'String','Ready','HorizontalAlignment','left', ...
                      'ForegroundColor',[0.95 0.95 0.95],'BackgroundColor',[0.12 0.13 0.16]);

    set([hM hVal hSigma hNoise hFrac hStr], 'Callback', @onSliderChange);

    ax1 = subplot('Position',[0.26 0.57 0.22 0.36]);
    ax2 = subplot('Position',[0.51 0.57 0.22 0.36]);
    ax3 = subplot('Position',[0.76 0.57 0.22 0.36]);
    ax4 = subplot('Position',[0.26 0.09 0.22 0.36]);
    ax5 = subplot('Position',[0.51 0.09 0.22 0.36]);
    ax6 = subplot('Position',[0.76 0.09 0.22 0.36]);

    setDarkAxes([ax1 ax2 ax3 ax4 ax5 ax6]);
    onRun();

    function onBasisChange(~,~)
        idx = get(hBasis,'Value');
        s.basis = s.basis_list{idx};
        if strcmpi(s.basis,'Himmelblau')
            s.d = 2;
            set(hDim,'String','2');
        end
    end

    function onSliderChange(~,~)
        s.M = round(get(hM,'Value')); set(hMtxt,'String',num2str(s.M));
        s.validity = get(hVal,'Value'); set(hValtxt,'String',sprintf('%.2f',s.validity));
        s.sigma = get(hSigma,'Value'); set(hSigmatxt,'String',sprintf('%.2f',s.sigma));
        s.noise = get(hNoise,'Value'); set(hNoisetxt,'String',sprintf('%.3f',s.noise));
        s.outlier_frac = get(hFrac,'Value'); set(hFractxt,'String',sprintf('%.3f',s.outlier_frac));
        s.outlier_strength = get(hStr,'Value'); set(hStrtxt,'String',sprintf('%.2f',s.outlier_strength));
    end

    function onRun(~,~)
        onSliderChange();

        s.d = max(2, round(str2double(get(hDim,'String'))));
        s.n = max(400, round(str2double(get(hN,'String'))));
        s.order = max(1, round(str2double(get(hOrd,'String'))));

        if strcmpi(s.basis,'Himmelblau')
            s.d = 2;
            set(hDim,'String','2');
        end

        set(hInfo,'String','Computing...'); drawnow;

        try
            [X, F, gtOut] = synthData(s);

            opts = struct();
            opts.M = s.M;
            opts.validity_range = s.validity;
            opts.point_mode = 'centroid';
            opts.sigma_factor = s.sigma;

            res = gradient_iso_pipeline_nd(X, F, s.order, opts);
            L1 = res.orders{2};
            pts = L1.domain_points;
            g = L1.values(:,1:s.d);
            score = res.confidence.score;

            thr = mean(score) + s.sigma * std(score);
            predOut = score < thr;

            nn = dsearchn(X, pts);
            gtAt = gtOut(nn);

            [tp,fp,fn,tn,prec,rec,f1] = metrics(gtAt, predOut);

            [fpr,tpr] = rocCurve(gtAt, score);
            [recall,precision] = prCurve(gtAt, score);

            cla(ax1); cla(ax2); cla(ax3); cla(ax4); cla(ax5); cla(ax6);

            axes(ax1);
            scatter(X(~gtOut,1), X(~gtOut,2), 7, [0.70 0.70 0.70], 'filled'); hold on;
            scatter(X(gtOut,1), X(gtOut,2), 15, [0.95 0.25 0.25], 'filled');
            axis equal tight; title('Ground Truth (Outlier=rot)'); xlabel('x1'); ylabel('x2');

            axes(ax2);
            qidx = 1:max(1,floor(size(pts,1)/500)):size(pts,1);
            if s.d >= 2
                quiver(pts(qidx,1), pts(qidx,2), g(qidx,1), g(qidx,2), 2.0, 'Color',[0.1 0.9 0.9]);
            else
                scatter(pts(:,1), zeros(size(pts,1),1), 7, g(:,1), 'filled');
            end
            axis equal tight; title('Gradient Projection (Order 1)'); xlabel('x1'); ylabel('x2');

            axes(ax3);
            scatter(pts(:,1), pts(:,2), 10, score, 'filled');
            axis equal tight; title(sprintf('Score (thr=%.3g)',thr)); xlabel('x1'); ylabel('x2'); colorbar;

            axes(ax4);
            scatter(pts(~predOut,1), pts(~predOut,2), 7, [0.70 0.70 0.70], 'filled'); hold on;
            scatter(pts(predOut,1), pts(predOut,2), 15, [0.95 0.25 0.25], 'filled');
            axis equal tight;
            title(sprintf('Prediction | P=%.2f R=%.2f F1=%.2f',prec,rec,f1)); xlabel('x1'); ylabel('x2');

            axes(ax5);
            plot(fpr,tpr,'LineWidth',2,'Color',[0.99 0.7 0.2]); hold on;
            plot([0 1],[0 1],'--','Color',[0.5 0.5 0.5]);
            xlim([0 1]); ylim([0 1]); grid on;
            title('ROC'); xlabel('FPR'); ylabel('TPR');

            axes(ax6);
            plot(recall,precision,'LineWidth',2,'Color',[0.35 0.9 0.5]);
            xlim([0 1]); ylim([0 1]); grid on;
            title(sprintf('PR  | TP=%d FP=%d FN=%d TN=%d',tp,fp,fn,tn));
            xlabel('Recall'); ylabel('Precision');

            setDarkAxes([ax1 ax2 ax3 ax4 ax5 ax6]);
            renderMeshFigureIf2D(s, X, F, pts, score, predOut);
            set(hInfo,'String',sprintf('Done | basis=%s d=%d N=%d K=%d',s.basis,s.d,s.n,s.order));

            fprintf('\n=== Gradient-Iso N-D Lab ===\n');
            fprintf('basis=%s d=%d N=%d K=%d M=%d validity=%.2f sigma=%.2f\n', ...
                s.basis,s.d,s.n,s.order,s.M,s.validity,s.sigma);
            fprintf('TP=%d FP=%d FN=%d TN=%d | P=%.4f R=%.4f F1=%.4f\n\n', ...
                tp,fp,fn,tn,prec,rec,f1);

        catch ME
            set(hInfo,'String',['Error: ' ME.message]);
            rethrow(ME);
        end
    end
end

function renderMeshFigureIf2D(s, X, F, pts, score, predOut)
    if s.d ~= 2
        return;
    end

    fh = findobj('Type','figure','Name','Gradient-Iso Mesh View');
    if isempty(fh)
        fh = figure('Name','Gradient-Iso Mesh View','Color',[0.08 0.09 0.11], ...
                    'NumberTitle','off','Position',[80 70 1300 520]);
    else
        figure(fh);
        clf(fh);
    end

    axA = subplot(1,2,1);
    axB = subplot(1,2,2);
    setDarkAxes([axA axB]);

    x = X(:,1); y = X(:,2);
    gx = linspace(min(x), max(x), 90);
    gy = linspace(min(y), max(y), 90);
    [GX, GY] = meshgrid(gx, gy);

    Ffun = scatteredInterpolant(x, y, F, 'natural', 'nearest');
    Gf = Ffun(GX, GY);

    axes(axA);
    surf(GX, GY, Gf, 'EdgeColor','none', 'FaceAlpha',0.95);
    hold on;
    title(sprintf('%s Surface f(x) + Samples', s.basis));
    xlabel('x1'); ylabel('x2'); zlabel('f');
    colormap(axA, turbo); colorbar;
    view(48, 34);
    scatter3(x, y, F, 8, [0.9 0.9 0.9], 'filled');

    Sfun = scatteredInterpolant(pts(:,1), pts(:,2), score, 'natural', 'nearest');
    Gs = Sfun(GX, GY);

    axes(axB);
    surf(GX, GY, Gs, 'EdgeColor','none', 'FaceAlpha',0.95);
    hold on;
    title('Confidence Score Surface + Predicted Outliers');
    xlabel('x1'); ylabel('x2'); zlabel('score');
    colormap(axB, turbo); colorbar;
    view(48, 34);
    scatter3(pts(~predOut,1), pts(~predOut,2), score(~predOut), 8, [0.75 0.75 0.75], 'filled');
    scatter3(pts(predOut,1), pts(predOut,2), score(predOut), 14, [0.95 0.25 0.25], 'filled');
end

function [X, F, gtOut] = synthData(s)
    rng(s.seed);

    d = s.d;
    n = s.n;
    frac = s.outlier_frac;
    nOut = max(1, round(frac * n));

    lim = domainLimits(s.basis, d);
    X = lim(1) + (lim(2)-lim(1))*rand(n, d);

    fClean = evalBasis(s.basis, X);
    F = fClean + s.noise * std(fClean) * randn(n,1);

    outIdx = randperm(n, nOut);
    jump = s.outlier_strength * std(fClean) .* sign(randn(nOut,1)) .* (1 + 0.5*rand(nOut,1));
    F(outIdx) = F(outIdx) + jump;

    gtOut = false(n,1);
    gtOut(outIdx) = true;
end

function y = evalBasis(name, X)
    switch lower(name)
        case 'himmelblau'
            if size(X,2) ~= 2
                error('Himmelblau ist nur fuer d=2 definiert.');
            end
            x = X(:,1); y2 = X(:,2);
            y = (x.^2 + y2 - 11).^2 + (x + y2.^2 - 7).^2;

        case 'rosenbrock (banana)'
            y = zeros(size(X,1),1);
            for i = 1:size(X,2)-1
                y = y + 100*(X(:,i+1)-X(:,i).^2).^2 + (1-X(:,i)).^2;
            end

        case 'rastrigin'
            d = size(X,2);
            y = 10*d + sum(X.^2 - 10*cos(2*pi*X), 2);

        case 'sphere'
            y = sum(X.^2, 2);

        case 'ackley'
            d = size(X,2);
            a = 20; b = 0.2; c = 2*pi;
            t1 = -a * exp(-b * sqrt(sum(X.^2,2) / d));
            t2 = -exp(sum(cos(c*X),2) / d);
            y = t1 + t2 + a + exp(1);

        otherwise
            error('Unbekannte Basisfunktion: %s', name);
    end
end

function lim = domainLimits(name, d)
    switch lower(name)
        case 'himmelblau'
            lim = [-6, 6];
        case 'rosenbrock (banana)'
            lim = [-3, 3];
        case 'rastrigin'
            lim = [-5.12, 5.12];
        case 'sphere'
            lim = [-6, 6];
        case 'ackley'
            lim = [-5, 5];
        otherwise
            lim = [-6, 6];
    end

    if d > 8
        lim = lim * 0.7;
    end
end

function [tp,fp,fn,tn,precision,recall,f1] = metrics(gtOut, predOut)
    tp = sum(predOut & gtOut);
    fp = sum(predOut & ~gtOut);
    fn = sum(~predOut & gtOut);
    tn = sum(~predOut & ~gtOut);

    precision = tp / max(tp + fp, 1);
    recall = tp / max(tp + fn, 1);
    f1 = 2*precision*recall / max(precision + recall, eps);
end

function [fpr,tpr] = rocCurve(gtOut, score)
    thr = linspace(min(score), max(score), 140);
    tpr = zeros(size(thr));
    fpr = zeros(size(thr));

    for i = 1:numel(thr)
        predOut = score < thr(i);
        tp = sum(predOut & gtOut);
        fp = sum(predOut & ~gtOut);
        fn = sum(~predOut & gtOut);
        tn = sum(~predOut & ~gtOut);

        tpr(i) = tp / max(tp + fn, 1);
        fpr(i) = fp / max(fp + tn, 1);
    end
end

function [recall, precision] = prCurve(gtOut, score)
    thr = linspace(min(score), max(score), 140);
    recall = zeros(size(thr));
    precision = zeros(size(thr));

    for i = 1:numel(thr)
        predOut = score < thr(i);
        tp = sum(predOut & gtOut);
        fp = sum(predOut & ~gtOut);
        fn = sum(~predOut & gtOut);

        recall(i) = tp / max(tp + fn, 1);
        precision(i) = tp / max(tp + fp, 1);
    end
end

function h = mklabel(parent, txt, pos)
    h = uicontrol(parent,'Style','text','Units','normalized','Position',pos, ...
                  'String',txt,'HorizontalAlignment','left', ...
                  'ForegroundColor',[0.95 0.95 0.95],'BackgroundColor',[0.12 0.13 0.16]);
end

function h = mkval(parent, val, pos)
    h = uicontrol(parent,'Style','text','Units','normalized','Position',pos, ...
                  'String',num2str(val), 'HorizontalAlignment','right', ...
                  'ForegroundColor',[0.95 0.95 0.95],'BackgroundColor',[0.12 0.13 0.16]);
end

function setDarkAxes(ax)
    for i = 1:numel(ax)
        set(ax(i),'Color',[0.10 0.11 0.13], 'XColor',[0.9 0.9 0.9], 'YColor',[0.9 0.9 0.9]);
        grid(ax(i),'on');
    end
    colormap(turbo);
end
