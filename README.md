# PHYSICS2026
## An open, reproducible archive of mathematical physics results

**Author:** Tony Newton — Newton Astro Labs, London, UK.

PHYSICS2026 collects precisely stated results in physics and mathematical physics, along with complete arguments, machine-reproducible checks, source manuscripts, and transparent limitations. Every numbered investigation is an independent, versioned research unit.

### What counts as a result?

- **PROVED (internal):** a precise theorem with a complete human-readable argument and independently repeatable checks. Not peer reviewed.
- **CERTIFIED:** a theorem whose computational steps are covered by explicitly documented rigorous certificates and a completed independent proof audit. Certification describes a verification method, not external endorsement.
- **CONDITIONAL:** a result that depends on clearly listed assumptions or an unproved lemma.
- **NUMERICAL:** an empirical or computational observation without a rigorous general proof.
- **OPEN:** an outstanding problem or a failed/inconclusive attack.
- **REFUTED:** a proposed assertion with a counterexample.

A restricted theorem is **not** advertised as the solution of a broader open problem. Prior discoveries are cited, and novelty is assessed separately from mathematical correctness.

### Research collection

See [INDEX.md](INDEX.md) for the numbered inventory, paper locations, proof artifacts, and verification status.

### Reproducing an investigation

Each investigation includes a statement of scope, a paper source, proof notes, a verifier, explicit software requirements, and a manifest describing what the tests do *and do not* establish. GitHub Actions runs the public verification suite and builds a PDF manuscript.

### Research protocol

Read [RELEASE_PROTOCOL.md](RELEASE_PROTOCOL.md). Every result receives an independent adversarial second pass, assumption audit, known-prior-art check, and claim-calibration review before being marked internally proved.

### Attribution

Tony Newton  
Newton Astro Labs*  
London, UK  
tony.newton79@gmail.com

*Newton Astro Labs is the trading name under which Tony Newton conducts independent computational research in the United Kingdom; it is not a limited company.*

### Disclaimer

A reproducibility test is not itself a proof of a universal mathematical claim. The proof is the mathematical argument; tests verify important identities, arithmetic, and implementations. Repository publication does not imply peer review, journal acceptance, or priority.
