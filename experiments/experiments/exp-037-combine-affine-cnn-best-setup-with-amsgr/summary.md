[exp-037-combine-affine-cnn-best-setup-with-amsgr] discard | test_accuracy=0.9915 (higher=better) | "Combine affine CNN best setup with AMSGrad" | codex-mnist-1 | 2026-03-28T23:24:58Z
Methodology: Starting from the affine CNN, I added cross-entropy label smoothing, a time-based linear warmup followed by cosine LR decay across the 90-second budget, and enabled Adam AMSGrad to combine previously successful optimizer ingredients in one run.
Code patch:
(none)
