# Pinned VICE numerical subset

Three source files are exact Git blobs from the revision in `provenance.json`:
`point_set.py`, `sampled_field.py`, `edge_intersector.py`. They remain under
their original Python module names. The `__init__.py` files only make this
subset importable and give it precedence over unrelated installed packages.

Do not edit these modules to change the research method. Update the explicit
upstream revision, refresh the three blobs and hashes, and regenerate tests
and experiments together. `VICE_MEASEVAL_SOURCE` opts into a live checkout.
