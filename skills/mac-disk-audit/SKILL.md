---
name: mac-disk-audit
description: Audit macOS disk usage when the Mac is low on space, System Data is large, stale files need review, or storage maintenance and external-drive relocation are requested. Measure actual allocation, account for external-volume symlinks, rank cleanup candidates by evidence and risk, and recommend efficient alternatives and ongoing maintenance.
---

# Mac Disk Audit

Produce a measured, ranked storage report and a concrete cleanup proposal. An audit request authorizes inspection and report creation; obtain authorization for the exact cleanup or migration targets before changing existing data.

## Measure the actual storage

- Read relevant home guidance and storage documentation. On Riley's Mac, `/Volumes/Apfspace` participates in the runtime through symlinks; check its mount and free capacity before proposing more relocation. Existing app-support targets belong under `/Volumes/Apfspace/Library/Application Support`, not `Applikations/Application Support`.
- Start with `df -h / /System/Volumes/Data /Volumes/Apfspace`, `diskutil apfs list`, and read-only snapshot listings. APFS volumes share container capacity: root-volume usage alone does not describe the internal drive.
- Use `scripts/inventory.py --depth 1 <roots...>` for allocated directory sizes and immediate symlink targets. Drill into the largest children. It uses physical, same-filesystem `du`, reports errors, and does not traverse symlink roots. Inspect external targets separately; do not attribute them to internal storage or add parent and child totals together.
- Distinguish allocated bytes from logical file size. Sparse VM images, hard links, APFS clones, snapshots, cloud placeholders, and inaccessible directories make folder totals differ from actual reclaimable storage. State gaps rather than forcing reconciliation.
- Check `sysctl hw.memsize`, `sysctl vm.swapusage`, and the APFS VM volume. Large swap is current memory pressure, not a stale file to delete; suggest saving work and reviewing heavy concurrent apps. A restart can reduce swap temporarily, but do not promise a fixed saving.
- Keep long inventories observable: measure independent roots in separate invocations and preserve their JSON output. Do not repeatedly rescan the same large tree while a scan is running. Use bounded scans and report incomplete roots rather than silently treating them as zero.
  For example, run `python3 scripts/inventory.py --depth 1 --timeout 120 ~/Library > library.json`. The timeout is per root; partial rows remain available with `complete: false`. A permission failure also marks the root incomplete.
- Avoid opening cloud placeholder files or recursively hashing the home directory. Hash only specific duplicate candidates when justified.

## Decide what is reclaimable

For each substantial candidate, record its exact path, volume, allocated size, role, evidence, proposed action, likely saving, and uncertainty. File age alone does not establish that it is unused.

- Downloads: inspect installer versions, extracted/archive pairs, embedded build environments, and dirty repositories. Verify intended installed apps and archive contents before calling a copy redundant.
- App support: separate caches, updater leftovers, language servers, history, databases, credentials, and user documents. Match orphaned data to bundle IDs, installed apps on both volumes, and running services. Missing local app bundles alone do not prove orphaning.
- Developer storage: inspect active runtime/toolchain versions, package stores, build artifacts and virtual environments. Prefer supported package-manager cleanup with previews where available. Do not bulk-delete unknown environments or runtime caches.
- Containers: inspect the active Docker context and `docker system df` only if reachable. Never start a VM for the audit or equate an unreachable daemon with unused data. Volumes may contain unique application data.
- Trash and quarantine: moving files within the internal volume does not free space. Explain this when estimating savings; permanent removal or verified external transfer is a separate decision.
- Preserve music metadata, exact releases, staging boundaries, user histories, backups, and dirty work. Do not treat agent sessions or memory stores as caches.

## Relocation and ongoing maintenance

Prefer native storage/cache settings when supported. Symlink migration requires a mounted destination, sufficient headroom, app shutdown, verified copy, a reversible cutover, and a live app smoke test before retiring the source. Do not relocate macOS system directories wholesale. For Python caches, consider that cross-filesystem placement can prevent hard-link reuse and increase copies.

Recommend maintenance proportional to measured growth: a read-only baseline, periodic comparisons, free-space alerts, targeted cache retention, review of completed downloads, and removal of superseded toolchains after dependency checks. Reuse existing maintenance utilities when suitable; do not install cleaners or schedule destructive jobs merely to finish the audit.

Use the user's preferred free-space target, or propose a practical local target such as 25–30 GiB on a 256 GB system disk. Label this as a maintenance target rather than a macOS requirement. Prefer native package stores and reproducible lockfiles over multiple downloaded copies, and app-native relocation over symlinks when supported. Moving a cache to another filesystem can increase environment duplication; assess cache and project placement together.

## Evidence and delivery

Save a dated report and machine-readable inventory in the task's output folder. Include exact candidate paths, allocation, volume, confidence, dependencies, and the next verification needed. Separate confirmed disposable artifacts from possible orphaned data and user-owned archives. Record metadata-only age and app-use evidence where available, but do not call something unused from an old modification date alone.

For maintenance comparisons, reuse the same roots and measurement method. Compare completed root totals and largest children, and disclose changing files, permission errors, hardlinks, and clone-sharing limits. Propose read-only checks weekly and a deliberate review monthly; create a scheduled job only when requested.

If files disappear or free capacity changes during inspection, explicitly record concurrent activity and refresh only affected candidates. Never attribute those changes to the audit or present old allocation as a current reclaim estimate.

Run `python3 -m unittest discover -s tests` after changing the inventory collector. Synthetic report scenarios live in `evals/evals.json` and `evals/fixture.json`; these check safe reasoning, not live cleanup success.

Write a concise summary plus a detailed report with ranked candidates, separate internal/external totals, non-additive savings, and verification limits. Verify any authorized cleanup with before/after free-space measurements and application behavior. Check current primary documentation before recommending version-sensitive commands or alternative tools.
