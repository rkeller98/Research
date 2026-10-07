function test_canonical_datasets(repoRoot)
% Verify MATLAB -> export -> import with exact doubles and original JSON.
    addpath(fullfile(repoRoot, 'shared', 'matlab'));
    fixtures = dir(fullfile(repoRoot, 'datasets', '*.csv'));
    destination = fullfile(repoRoot, 'tmp', 'matlab_roundtrip');
    if ~isfolder(destination), mkdir(destination); end
    for entry = fixtures.'
        [~, name] = fileparts(entry.name);
        dataset = importCanonicalDataset(fullfile(entry.folder, name));
        stem = fullfile(destination, name);
        exportCanonicalDataset(dataset, stem);
        again = importCanonicalDataset(stem);
        assert(isequaln(dataset.values, again.values));
        assert(isequal(dataset.csvBytes, again.csvBytes));
        assert(strcmp(dataset.manifestText, again.manifestText));
        fprintf('MATLAB exact round-trip: %s (%d OPs)\n', name, size(dataset.values, 1));
    end
end
