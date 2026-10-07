function exportCanonicalDataset(dataset, stem)
%EXPORTCANONICALDATASET Deterministic scientific double table and manifest.
% Unchanged imported fixtures preserve CSV/JSON bytes exactly. For newly
% interpreted data provide columns, values and a complete manifest struct.
    stem = char(stem);
    assert(strcmp(dataset.manifest.schema_version, 'research-operating-points-v1'), ...
        'Research:Schema', 'Unsupported schema.');
    assert(size(dataset.values, 2) == numel(dataset.columns), 'Research:Shape', 'Column count mismatch.');
    assert(~any(isinf(dataset.values), 'all'), 'Research:Finite', 'Infinite canonical value.');
    assert(isequal(dataset.columns(:), fieldnames(dataset.manifest.columns)), ...
        'Research:Columns', 'Column metadata mismatch.');
    [folder, basename] = fileparts(stem);
    if ~isempty(folder) && ~isfolder(folder), mkdir(folder); end
    lines = cell(size(dataset.values, 1) + 1, 1);
    lines{1} = strjoin(dataset.columns, ',');
    for row = 1:size(dataset.values, 1)
        fields = cell(1, numel(dataset.columns));
        for col = 1:numel(fields)
            value = dataset.values(row, col);
            if isnan(value), fields{col} = ''; else, fields{col} = sprintf('%.17g', value); end
        end
        lines{row + 1} = strjoin(fields, ',');
    end
    bytes = unicode2native([strjoin(lines, newline) newline], 'UTF-8').';
    digest = java.security.MessageDigest.getInstance('SHA-256');
    digest.update(bytes);
    hash = lower(reshape(dec2hex(typecast(digest.digest(), 'uint8'), 2).', 1, []));
    manifest = dataset.manifest;
    preserve = isfield(dataset, 'csvBytes') && isequal(bytes, dataset.csvBytes) ...
        && strcmp(manifest.csv_file, [basename '.csv']);
    if preserve
        manifestText = dataset.manifestText;
    else
        manifest.csv_file = [basename '.csv'];
        manifest.csv_sha256 = hash;
        manifest.row_count = size(dataset.values, 1);
        manifestText = [jsonencode(manifest, PrettyPrint=true) newline];
    end
    file = fopen([stem '.csv'], 'wb');
    assert(file >= 0, 'Research:Write', 'Cannot write CSV.');
    fwrite(file, bytes, 'uint8'); fclose(file);
    file = fopen([stem '.json'], 'wb');
    assert(file >= 0, 'Research:Write', 'Cannot write manifest.');
    fwrite(file, unicode2native(manifestText, 'UTF-8'), 'uint8'); fclose(file);
end
