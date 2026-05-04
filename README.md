# Mini vLLM Inference Engine Simulator

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Progress-M1%20Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-orange.svg)

---

## 📌 Overview

Modern LLM systems must serve **many concurrent users** under strict **compute and memory constraints**.

This project is a **from-scratch simulation of a vLLM-style inference engine**, built to understand:

* Scheduling
* Memory (KV cache)
* Batching strategies
* Latency vs throughput tradeoffs

---

## ⚡ What is vLLM?

**vLLM** is a high-performance LLM inference engine designed for **maximum throughput and memory efficiency**.

### Journey of a Prompt
[![Understanding VLLLM](https://img.youtube.com/vi/HMUZjitt0ts/0.jpg)](https://youtu.be/HMUZjitt0ts)

### 🔑 Core Ideas

* 🧠 **PagedAttention (KV cache paging)**
* ⚡ **Continuous batching**
* 📦 **Efficient memory reuse**

---

## 🤯 Why vLLM is Fast

| Challenge | Traditional Systems | vLLM        |
| --------- | ------------------- | ----------- |
| Memory    | Fragmented          | Paged       |
| GPU usage | Idle gaps           | Always busy |
| Batching  | Static              | Dynamic     |
| Latency   | High under load     | Stable      |

👉 Result: **Higher throughput + lower latency**

---

## 🧠 Project Goal

> Rebuild the **core systems ideas behind vLLM** through a step-by-step simulator.

Instead of real GPUs, we simulate:

* Token generation
* Request scheduling
* Memory allocation
* System behavior under load

---

## 🏗️ Project Roadmap

```
M1 → Basic simulator ✅
M2 → KV cache (memory model)
M3 → Fragmentation modeling
M4 → Continuous batching
M5 → Eviction policies
M6 → Prefill vs Decode
M7 → Scheduling & fairness
M8 → Multi-tenant simulation
M9 → Metrics & visualization
M10 → Interactive system
```

---


## 🎯 Why This Project Matters

This project gives you **real systems intuition** for:

* LLM serving infrastructure
* GPU utilization strategies
* Memory management at scale
* Scheduling tradeoffs

