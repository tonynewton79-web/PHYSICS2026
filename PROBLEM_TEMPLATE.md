# PHYSICS2026 — New problem template

## Publication title-page rule
The LaTeX paper title page must contain only the scientific title, author, affiliation and appropriate footnote; do **not** print a date, repository/project ID, internal-proof status, external-priority note, verification label or other administrative release metadata on the manuscript title page. Use `\\date{}` in LaTeX. Keep version, date, ID and verification status in the problem README, INDEX and AUDIT documents instead.

## Identity
- ID: PHY-XXX
- Precise title:
- Physics area:
- Authors and affiliations:
- Version / date:
- Status: OPEN initially.

## Question
State the exact mathematical conjecture/problem, domains, parameters, regularity assumptions and boundary conditions.

## Previous results
List precise citations and contrast known facts with proposed new claims.

## Main claim
State the theorem/counterexample, including quantifiers and exceptional cases. List what it does NOT prove.

## Proof
Give a complete human-readable mathematical argument. Separate analytically derived statements from numerical conjectures.

## Reproducible verification
- Pinned software versions
- Entrypoint and exact expected output
- Independent reference implementation or alternate derivation
- Certificates and their trust assumptions
- Negative and boundary tests

## Adversarial second pass
Record counterexample searches, failed pathways, revised claims, unresolved limitations, and citation/priority audit.

## Release
Maintain README.md, paper.tex, verify.py, requirements.txt, AUDIT.md, PDF_FILENAME.txt and CI in this problem folder. `PDF_FILENAME.txt` contains an ASCII-safe, underscore-separated rendering of the full manuscript title (without `.pdf`); automated builds use this to give the PDF a descriptive title-based filename. Publish only the evidence tier supported by the completed audit.
