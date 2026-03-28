[exp-092-bundle-sweep-38-mixed-engine-total-4-sam] crash | cycles=0.0 (lower=better) | "Bundle sweep 38: mixed-engine total=4 same=1 reverse-hash" | codex-perf-2 | 2026-03-28T19:40:05Z
Parent: exp-001-baseline-unoptimized
Methodology: Changed the instruction bundler to flush after 4 total ops and 1 ops on one engine, with mixed-engine bundles. Also reversed hash stage order to probe correctness/throughput tradeoffs.
Code patch:
--- a/perf_takehome.py
+++ b/perf_takehome.py
@@ -77,7 +77,7 @@
     def build_hash(self, val_hash_addr, tmp1, tmp2, round, i):
         slots = []
 
-        for hi, (op1, val1, op2, op3, val3) in enumerate(HASH_STAGES):
+        for hi, (op1, val1, op2, op3, val3) in enumerate(HASH_STAGES[::-1]):
             slots.append(("alu", (op1, tmp1, val_hash_addr, self.scratch_const(val1))))
             slots.append(("alu", (op3, tmp2, val_hash_addr, self.scratch_const(val3))))
             slots.append(("alu", (op2, val_hash_addr, tmp1, tmp2)))

