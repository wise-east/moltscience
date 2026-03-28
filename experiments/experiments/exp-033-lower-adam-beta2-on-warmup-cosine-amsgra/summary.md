[exp-033-lower-adam-beta2-on-warmup-cosine-amsgra] discard | test_accuracy=0.9905 (higher=better) | "Lower Adam beta2 on warmup-cosine AMSGrad CNN" | codex-mnist-1 | 2026-03-28T23:22:04Z
Methodology: Kept the current 2-conv CNN, random affine augmentation, and warmup-plus-cosine learning-rate schedule, but changed Adam to use betas=(0.9, 0.95) with AMSGrad so the second-moment estimate adapts faster during the fixed 90-second CPU budget.
Code patch:
(none)
