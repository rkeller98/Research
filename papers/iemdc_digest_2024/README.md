Read the repository `WRITING_GUIDE.md` first.

# IEMDC digest 2024

Integrated from `IEMDC_Digest_2024_MA_Keller.zip`. The content uses the global
publication framework. IEMDC-specific letter-paper geometry and line spacing
are isolated in `venue.tex`; notation and colors are canonical in `shared/`. Build it with:

    .\scripts\build.ps1 iemdc_digest_2024

The paper depends on the canonical ../../shared/ infrastructure. The figures include their TikZ sources and
the prime-factor CSV data; the original IEEE bibliography is migrated to the
framework's Biber database.

It can also be compiled directly from this directory:

    latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
