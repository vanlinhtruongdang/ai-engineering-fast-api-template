# Performance guidelines

Apply these rules when a change targets latency, throughput, memory use, or a path likely to handle large data. The template has no performance target or benchmark dataset; do not invent one.

## Establish the baseline

1. Name the operation, workload size, concurrency, environment, and metric that matters to the user.
2. Reproduce the costly path and record a baseline with a command or profile that another contributor can run.
3. Inspect the call graph to locate the actual cost. Use CPU profiling for compute, memory profiling for allocations, and line profiling only when a specific function needs it.
4. Change the responsible layer, then compare the same workload before and after. Keep correctness checks for the contract affected by the optimization.

Report median and tail latency or throughput only when the measurement method supports them. A single warm local request cannot establish a production capacity claim. For AI-backed routes added later, separate time spent in validation, provider or retrieval calls, and response serialization before deciding where to optimize; record provider call count and cost when they are part of the bottleneck.

## FastAPI and Python boundaries

- Do not block an async request handler with synchronous network or CPU work. Use an appropriate async client or move deliberate blocking work to the right execution boundary.
- Avoid repeated queries, provider calls, conversions, and large copies inside loops. Batch I/O only when the external API and failure semantics support it.
- Stream large inputs or outputs when materializing them would exceed the intended memory budget; preserve validation and error handling at the boundary.
- Use connection pooling and lifespan-managed clients for real external dependencies. Close resources on shutdown.
- Cache only data whose staleness and invalidation are defined. A cache is not a substitute for understanding a slow query or provider call.
- Select only required fields and inspect data-access patterns for repeated per-item reads when persistence is introduced.

Optimization must preserve API shape, validation, authorization, timeout behavior, and cleanup. If batching or concurrency changes the order of results, error aggregation, or retry behavior, treat that as a contract change and check callers explicitly.

Document the measured result, workload, and any tradeoff. If no representative measurement is available, describe the suspected risk as an assumption and prefer the clearer implementation.
