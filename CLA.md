<!-- SKELETON / OUTLINE — proposed Contributor License Agreement for brand-loom.
     This is a starting outline, NOT legal advice. Have counsel review before adopting.
     Model on the Apache Software Foundation ICLA/CCLA. -->

# Contributor License Agreement (CLA) — Outline

`brand-loom` is maintained by Hogan Lin / Meridian Global LLC ("the Maintainer") and a hosted commercial product
(Neoxra) is built on top of it. To keep the right to use contributions in that product unambiguous, contributors
grant the license below. Two variants: **Individual (ICLA)** and **Entity (CCLA)**.

## Why a CLA (not just Apache-2.0)

Apache-2.0 governs the *repository's* license to users. The CLA additionally secures, from each contributor to the
Maintainer, a clear, irrevocable grant that includes the right to relicense/use the contribution in the **closed,
commercial hosted product** — so the Maintainer never has to chase permissions later or when moving the repo under
a company org.

## Individual CLA — key terms (outline)

1. **Definitions** — "Contribution," "Submit," "Work."
2. **Copyright license grant.** Contributor grants the Maintainer a perpetual, worldwide, non-exclusive, royalty-
   free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display/perform,
   sublicense, and distribute the Contribution and derivative works — **including in commercial and closed-source
   products.**
3. **Patent license grant.** Same scope, royalty-free, irrevocable (with the standard defensive-termination clause
   if the contributor initiates patent litigation over the Work).
4. **Original work / right to grant.** Contributor certifies the Contribution is their original creation (or they
   have the rights) and that no third-party license conflicts.
5. **Employer rights.** If the work was made in the scope of employment, the contributor has permission from the
   employer, or the employer signs the Entity CLA.
6. **No obligation.** The Maintainer is not required to use or merge any Contribution.
7. **Retained rights.** Contributor retains copyright and may use their Contribution elsewhere.
8. **Disclaimer.** Contribution provided "as is," no warranties.
9. **Signature.** Name, GitHub handle, email, date (captured via CLA-assistant bot).

## Entity CLA — additional terms (outline)

- Authorizing signatory binds the legal entity and its designated employees.
- Schedule of authorized contributors (or a domain-based allowlist), updatable by the entity.
- Same copyright + patent grants as the ICLA, at entity scope.

## Mechanism

- Enforce via a **CLA-assistant GitHub App**: first-time contributors are blocked from merge until they sign;
  signatures stored against GitHub identity.
- Store signed records in a private location; reference the version signed.

## Open items for counsel

- Confirm grantee entity: **Meridian Global LLC** vs. Hogan Lin personally (recommend the LLC for the E-2 /
  company-value narrative and clean assignment).
- Confirm choice-of-law / venue.
- Confirm whether a lighter **DCO (Developer Certificate of Origin)** sign-off would suffice for v0.1 while
  contribution volume is low, upgrading to the full CLA if the project grows. (Trade-off: DCO is lower friction but
  does **not** grant the explicit commercial/relicensing rights the CLA does.)
