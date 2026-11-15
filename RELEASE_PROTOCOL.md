# PHYSICS2026 — Proof and release standard

**Unit of release:** One numbered problem folder. Keep distinct folders for distinct theorems rather than mixing incompatible claims.

Each folder should contain:
1. A precise question and all assumptions.
2. The paper source (LaTeX), a directly readable proof summary, and references.
3. Executable verifier code, pinned dependencies, deterministic expected output.
4. A declaration of which facts are known prior art and what, if anything, is plausibly new.
5. A first proof pass and a genuinely independent adversarial second pass.
6. An honest status label, limitations, and next unresolved target.
7. CI that checks the code and builds the PDF from source.

### Evidence tiers

- **OPEN:** unproved or unresolved.
- **NUMERICAL:** computationally indicated, not proven.
- **CONDITIONAL:** proven only when explicit assumptions hold.
- **INTERNAL PROOF:** a complete scoped mathematical proof has been produced and independently checked in the project, but not externally reviewed.
- **CERTIFIED:** additionally accompanied by documented formal/rigorous certificate coverage (state exactly what is certified).
- **EXTERNAL REVIEWED:** specific human review or peer-review records can be cited.
- **REFUTED:** a counterexample or contradiction has been proved.

These are not rankings of importance. A theorem about a restricted grammar does not settle integrability of a full nonlinear PDE.

### Mandatory adversarial audit

Perform a second pass using a different derivation or independent computational implementation. Search for sign errors, hidden regularity assumptions, boundary effects, missing cases, circular tests, exceptional parameter values, and previously known formulations. State failures and unresolved prior-art uncertainty plainly.

### Repository workflow

A new investigation should be developed on a numbered branch, tested in CI, and incorporated through a reviewable PR. Never silently replace already published claims: preserve the historical correction and explain any downgrade.

### Author

Tony Newton, Newton Astro Labs, London, UK. Newton Astro Labs is an independent UK trading name, not a limited company.
