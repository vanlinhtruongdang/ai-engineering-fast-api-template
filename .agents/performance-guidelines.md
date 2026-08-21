# Performance Guidelines

## Core principles

- Profile before optimizing.
- Focus on measured hot paths and production-representative data.
- Prefer clarity until a measurement identifies a bottleneck.

## Investigation order

1. Use CPU profiling for compute-bound behavior.
2. Use memory profiling for allocation pressure or suspected leaks.
3. Use line profiling when a specific operation needs isolation.
4. Inspect the call graph when the expensive path is unclear.

## Python and FastAPI practices

- Prefer built-ins and the standard library for common operations.
- Avoid repeated object creation and copying inside loops.
- Stream large input with generators when full materialization is unnecessary.
- Batch I/O and use connection pooling for external systems.
- Avoid blocking work in asynchronous request paths.
- Keep handlers thin, avoid import-time work, and initialize resources through lifespan.
- Select only the fields a query or response needs and guard against N+1 access patterns.

## Benchmark evidence

Record the command, dataset characteristics, and result when a performance-sensitive change is made. Do not add caching or sacrifice readability without measured evidence.
