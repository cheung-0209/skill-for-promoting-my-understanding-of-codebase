# Research and ML code

Use this route for paper implementations, tensor models, scientific pipelines, and geometry. Combine with `practice.md` when the learner wants to retype or implement components.

## Establish what is implemented

Find registry/config selection, model construction, data mapper, transforms, forward methods, losses, optimizer, inference postprocessing, and evaluator. Follow the selected configuration; unused alternatives do not describe the current model. Open source files before describing their internals.

If a paper is available, map:

| Paper concept / section | Code symbol and line range | Input/output contract | Evidence or discrepancy |
|---|---|---|---|
| Verified concept | Actual inspected symbol | Meaning and dimensions | Source / paper / inferred / run |

Do not invent equation numbers. A function sharing a concept's name is not enough to establish mathematical equivalence. Where implementation and paper differ, present both with sources. Unavailable weights or data limit reproduction, not source reading.

## Trace one sample

Explain image/file layout → decoded array → preprocessing → batch → features → prediction → postprocessing → metrics. Training and evaluation often differ; trace each path and show where labels are consumed or absent.

For each important tensor, record:

| Symbol at code location | Shape | Axis meaning | dtype/device | How established |
|---|---|---|---|---|
| Actual variable | Symbolic or measured dimensions | Batch/channel/spatial/point | Observed or unknown | Static derivation / measured run |

Use symbolic sizes where runtime sizes are unknown. Derive a numerical shape only from an inspected config and actual operations; account for padding, stride, interpolation, cropping, and batch semantics. Label any illustrative dimensions as synthetic.

For spatial or point-based code, explicitly trace:

- Voxel index vs physical coordinate; array axes vs `(x,y,z)`; spacing, origin, and direction when present.
- Normalized grid ranges, `align_corners`, axis ordering at sampling, and the inverse transform.
- Point ordering, edges/topology, control points vs interpolated samples, distance units, and boundary treatment where relevant.

Do not assume these conventions from library defaults; inspect arguments and verify defaults against the relevant installed version or official documentation when needed.

## Explain optimization

Show each actual loss's inputs, reduction, coefficient, and gradient path. Point out detach/no-grad, thresholds, CPU/NumPy operations, discrete indexing, or conditional branches when they affect differentiation. Do not claim an end-to-end differentiable pipeline without tracing it.

Keep separate: training supervision, inference inputs, prediction targets, reported metrics, and checkpoint selection. Explain learning rate, optimizer, precision, and distributed batch conventions only to the depth needed for the task.

## Build useful lessons

A practical arc can be: task and environment → one sample's data path → backbone/features → core paper mechanism → losses/training → inference/evaluation and debugging. Adapt or merge topics rather than filling a fixed syllabus.

Prefer interactions that answer a concrete question: predict a tensor size, follow a point through coordinate transforms, step through one deformation, vary an interpolation parameter, or identify which loss receives a gradient. Any browser simulation must say whether it runs real model code or illustrates an equation with synthetic inputs.

## Execution ladder

Progress only as far as the task and environment justify: source inspection → stdlib/CPU example → small isolated tensor operation → model forward with synthetic input → real-data inference → training/benchmark reproduction. A CUDA-oriented research repository can still support a useful course on a CPU-only host. Describe exact blockers without rewriting its dependency stack speculatively. Do not download large datasets/weights or start full training merely to create a tutorial.
