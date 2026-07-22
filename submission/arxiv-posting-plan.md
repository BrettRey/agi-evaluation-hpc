# arXiv posting plan
<!-- SUMMARY: Post the rewrite as a new arXiv submission with a supersession note; back-annotate 2510.15236 to point forward · status: ready, not yet posted · updated: 2026-07-22 -->

**Decision:** post as a **new submission** with a note stating the relationship, and let
moderation reclassify or reject it as a replacement if they prefer that. Moderators make
this call at submission; the support desk is for technical problems, not editorial
judgment, so there's nothing to ask in advance.

**Rationale:** the rewrite shares topic, author, and some sources with arXiv:2510.15236
and little else. The homeostatic-property-cluster thesis is withdrawn rather than
revised, both proposed measures are retired, and an empirical component has been added.
Posting it as v2 would leave the identifier pointing at something a v1 reader wouldn't
recognise. If moderation disagrees, converting to a replacement is cheap; the reverse is
not.

---

## 1. Comments field on the new submission

> Substantially rewritten and retitled; supersedes arXiv:2510.15236, whose homeostatic
> property-cluster account of general intelligence, centrality-prior score, and cluster
> stability index family are withdrawn. Shares the topic and part of the source base with
> that paper; the argument, apparatus, and empirical companion are new.

## 2. Replacement comment on arXiv:2510.15236

This is the part that matters most, and it can only be done after the new identifier
exists. Without it, v1 stays live and citable as a position that has been abandoned.

> Superseded by arXiv:NNNN.NNNNN. The homeostatic property-cluster account of general
> intelligence argued here, and the centrality-prior and cluster-stability measures
> proposed, are withdrawn.

## 3. Sequence

1. Post the new submission with the comment in §1.
2. Wait for the identifier to be assigned and announced.
3. Replace 2510.15236 with the comment in §2, filling in the new identifier.
4. Update the DOI recorded in `CLAUDE.md`, `STATUS.md`, and `PORTFOLIO.md` to the new
   item, keeping 2510.15236 named as the withdrawn predecessor.
5. Record the supersession in the *Minds and Machines* cover letter and in the venue
   decision record.

## 4. If moderation asks for a replacement instead

Then the §1 text becomes the v2 Comments field, §2 and step 3 fall away, and the recorded
DOI is unchanged. Nothing else in the plan moves.

---

## Open dependencies

- The venue decision record is still unmade, and prior-posting disclosure belongs in it.
- The sibling paper (PhilSci-Archive item 30582, *Projectibility: A History and a
  Diagnostic Framework*) is awaiting editorial release. Once live, both papers should
  cross-reference; neither currently cites the other.
