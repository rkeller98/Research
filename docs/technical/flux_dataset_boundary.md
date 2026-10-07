# Scientific data transport boundary

Raw measurement loading, signal aggregation and scientific interpretation are
different operations. Current MeasEval loading preserves raw MATLAB structs;
`DataConversion` erases spaces in signal names, groups by `PE_Index_meas`,
optionally applies its legacy iterative outlier policy and emits a signal-only
`Meas`. Channel units/descriptions, recording metadata and repeat dispersion
are not part of that output. Legacy default injection and missing-to-zero
normalization may erase distinctions essential for scientific interpretation.

Research therefore extracts OP fixtures explicitly, preserving requested versus
measured values, missingness, medians/deviations/counts, source hashes, state
keys and convention qualifications. No outlier or settling policy is guessed.
Unknown machine type or phase configuration stays unknown. Reconstructed flux
and CAN indication retain their distinct evidence status.

The portable schema is `research-operating-points-v1`. Python and MATLAB
implementations validate transport; MeasEval's optional `adapter.canonical`
package accepts a prepared table/manifest without making it a new production
calculation mode. Contract changes require synchronized schema/reference-code
and transport tests, not a local installed-app dependency in paper scripts.

UI classes, product run controllers and deployment details are not necessary
to understand the scientific projection, integrability or rank arguments and
are excluded from the active papers. Reproduction requires numeric recipes, units, assumptions and solver details, which remain documented there.
