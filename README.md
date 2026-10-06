# Chiplet-D2D-High-Speed-Serial-Interface-HSSI-Subsystem

## 1. Project Overview

### 1.1 Description
> A synthesizable SystemVerilog physical coding sublayer and digital communication subsystem designed for low-latency, high-bandwidth Die-to-Die (D2D) chiplet interconnects. The project integrates an 8b/10b Physical Coding Sublayer (PCS) with an asynchronous elastic buffer, a 3-tap TX Feed-Forward Equalizer (FFE), a 1-tap speculative Decision Feedback Equalizer (DFE), a 2-Virtual-Channel Network-on-Chip (NoC) router port, and an All-Digital Phase-Locked Loop (ADPLL) digital control core. System workloads and packet burstiness are characterized using gem5 trace-driven injection models, while mixed-signal boundaries are verified using SystemVerilog Real Number Modeling (RNM).

### 1.2 Goals & Objectives
- Implement an 8b/10b Physical Coding Sublayer (PCS) supporting standard comma alignment (K28.5) and rate-matching ordered sets (K28.0).
- Construct a dual-clock asynchronous elastic buffer using Gray-coded pointers to absorb clock frequency drift (+/- 300 ppm) across independent clock domains.
- Develop high-speed signal equalization: a 3-tap FIR TX FFE for high-frequency channel de-emphasis and a 1-tap loop-unrolled speculative RX DFE for post-cursor Inter-Symbol Interference (ISI) cancellation.
- Design a 2-Virtual-Channel (VC) NoC interface with credit-based flow control to prevent head-of-line blocking during off-chip memory transactions.
- Implement an all-digital clock synthesis engine comprising a Time-to-Digital Converter (TDC) interface, a pipelined fixed-point Proportional-Integral (PI) digital loop filter, and a MASH 1-1 Sigma-Delta dither modulator.
- Model realistic switching activity factors and bursty coherence traffic by configuring an Out-of-Order CPU in gem5.
- Verify mixed-signal boundaries using SystemVerilog nettype real models compiled via Verilator and visualized in GTKWave.

### 1.3 Key Features
- **DC-Balanced 8b/10b Codec:** Strict running disparity (RD = +/- 1) tracking, disparity error detection, and support for all 12 special K-codes.
- **Dynamic Bit-Slip Word Aligner:** 20-bit sliding-window shift register with hunting, locking, and monitoring states for comma synchronization.
- **Clock Domain Crossing (CDC) Elastic Buffer:** Dual-clock asynchronous circular FIFO with 2-flip-flop Gray synchronizers, watermark thresholds, and automatic  add/drop logic.
- **High-Speed Equalization Blocks:** Parameterized 3-tap FIR TX FFE with programmable coefficients (c-1, c0, c1) and a 1-tap speculative DFE with twin parallel slicers to eliminate tight feedback latency constraints.
- **Credit-Controlled NoC Port:** 2-VC input buffer architecture separating memory requests and coherence responses with round-robin arbitration.
- **High-Resolution ADPLL Digital Core:** Pipelined fixed-point loop dynamics with 1st-order noise shaping to optimize Digitally Controlled Oscillator (DCO) frequency resolution.
- **Architectural Coherence Workload Injection:** Injection traces capturing cache-miss burstiness and lock contention from a multi-core gem5 environment running MESI_Two_Level directory coherence.
