function dataset = importCanonicalDataset(stem)
%IMPORTCANONICALDATASET Portable OP fixture; no MeasEval dependency.
% Preserves original manifest bytes so JSON nulls and metadata round-trip.
    stem = char(stem);
    dataset.manifestText = fileread([stem '.json']);
    dataset.manifest = jsondecode(dataset.manifestText);
    assert(strcmp(dataset.manifest.schema_version, 'research-operating-points-v1'), ...
        'Research:Schema', 'Unsupported canonical dataset schema.');
    [~, basename] = fileparts(stem);
    assert(strcmp(dataset.manifest.csv_file, [basename '.csv']), ...
        'Research:Filename', 'Manifest must bind the selected CSV.');
    file = fopen([stem '.csv'], 'rb');
    assert(file >= 0, 'Research:MissingCsv', 'Cannot open CSV.');
    cleanup = onCleanup(@() fclose(file));
    dataset.csvBytes = fread(file, Inf, '*uint8');
    digest = java.security.MessageDigest.getInstance('SHA-256');
    digest.update(dataset.csvBytes);
    hash = lower(reshape(dec2hex(typecast(digest.digest(), 'uint8'), 2).', 1, []));
    assert(strcmp(hash, dataset.manifest.csv_sha256), 'Research:Checksum', 'CSV hash mismatch.');
    text = native2unicode(dataset.csvBytes.', 'UTF-8');
    lines = splitlines(string(text));
    dataset.columns = cellstr(split(lines(1), ','));
    declared = fieldnames(dataset.manifest.columns);
    assert(isequal(dataset.columns(:), declared(:)), 'Research:Columns', 'Column metadata mismatch.');
    dataset.values = nan(dataset.manifest.row_count, numel(dataset.columns));
    assert(numel(lines) == dataset.manifest.row_count + 2, 'Research:Rows', 'Unexpected CSV row count.');
    for row = 1:dataset.manifest.row_count
        fields = split(lines(row + 1), ',');
        assert(numel(fields) == numel(dataset.columns), 'Research:Shape', 'Malformed CSV row.');
        dataset.values(row, :) = str2double(fields).';
    end
    assert(~any(isinf(dataset.values), 'all'), 'Research:Finite', 'Infinite canonical value.');
end
