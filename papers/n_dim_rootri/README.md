Read the repository `WRITING_GUIDE.md` first.

# N-dimensional RooTri paper

Integrated from `N_dim_RooTri.zip`. The paper uses the repository publication
framework while retaining its MATLAB listings, TikZ illustration, and local
bibliography. Build it from the repository root with:

    .\scripts\build.ps1 n_dim_rootri

The paper depends on the canonical ../../shared/ infrastructure. Paper text is under `sections/`, the Delaunay
figure under `figures/`, MATLAB code under `listings/`, and bibliography data
under `bibliography/`.

It can also be compiled directly from this directory:

    latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
