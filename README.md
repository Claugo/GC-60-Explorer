# GC-60 Explorer

GC-60 Explorer is a supporting repository for **GC-60**, a conceptual model for prime number exploration based on the elimination of internal products within a structured arithmetic domain.

This repository is provided for **preservation, transparency, and reproducibility purposes**.  
It is **not intended as a performance-oriented or competitive implementation** of existing prime sieves.

The authoritative and citable version of this work is archived on Zenodo:

**DOI:** 10.5281/zenodo.18082369

---

## Project Scope

GC-60 explores a conceptual perspective in which:

- prime numbers are **never identified or used operationally** during the elimination process;
- compositeness is addressed through **systematic elimination of internal products**;
- primality emerges as a **residual property**, not as a guiding principle.

This repository does **not** aim to document algorithmic optimizations, benchmarks, or comparisons with classical or segmented sieves.

---

## Software Requirements

To run the GC-60 Explorer program, the following environment is required:

### Required
- **Python 3.10 or later**
- **NumPy**
- **Numba**

### Optional (for interactive dialogs)
- **Tkinter**  
  (usually included with standard Python distributions on Windows)

## Notes

The GC-60 model does not rely on the operational identification of prime numbers.
Let $$( A \subset \mathbb{N} \)$$ be a structured arithmetic domain defined by modular constraints.
Elimination is performed exclusively by considering internal products of the form:

$$n = a \cdot b \quad \text{with} \quad a, b \in A$$

No element of \( A \) is ever treated as prime during the elimination process.
Primality emerges only as a residual property after all admissible internal products
have been eliminated.

Any computational implementation included in this repository serves solely to
demonstrate the operational consistency of the conceptual model.
No claims regarding algorithmic efficiency, optimality, or superiority over
classical sieves are intended.



GC-60 continues a line of exploratory research initiated with GC57, focused on alternative conceptual approaches to multiplicative structures and semiprimes.

## Memory Considerations

GC-60 Explorer relies on data structures whose size grows proportionally with the
selected search range. As a consequence, available system memory plays a significant
role in practical executions.

On systems with limited RAM, large search ranges may lead to increased memory pressure,
reduced performance, or execution failure. This behavior is an inherent consequence
of the exploratory nature of the implementation and is not addressed through
aggressive memory optimization.

This limitation is acknowledged explicitly, as the purpose of GC-60 Explorer is
conceptual investigation rather than resource-efficient prime enumeration.

## Installation

It is recommended to use a virtual environment.

```bash
pip install numpy numba
