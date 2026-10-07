# Flux correction from independent reference quantities

## Status
Research framework, not yet a standalone paper.

## Question
Given a reconstructed flux vector and an independent measured quantity \(y=h(\psi,i,\ldots)\), which component of flux does that reference observe, what nullspace remains, and which correction representative is justified?

Torque is the first developed case and now has its own paper in `papers/torque_flux_consistency/`. Its real CAN reference remains conditional on sensor calibration and shaft-loss qualification. Future reference channels should be promoted only when they supply a distinct observation operator, uncertainty model, and validation dataset. A generic umbrella paper would currently be too meta and would recreate the mixing problem this reorganization removes.
