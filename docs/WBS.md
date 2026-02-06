# WBS & Schedule (CombatTestGen)

> **Based on**: TASKS.md
> **Start Date**: 2026-02-06

## Development Roadmap

| Phase | Tasks | Duration | Deliverables |
|-------|-------|----------|--------------|
| **1. Planning** | T-001 ~ T-003 | 1.5 Days | PRD, TRD, WBS |
| **2. Infrastructure** | T-010 ~ T-011 | 1 Day | Git, Virtual Env |
| **3. Domain Model** | T-020 ~ T-021 | 1.5 Days | CombatParams, Validation |
| **4. Edge Case Engine** | T-030 ~ T-032 | 2 Days | Algorithm, Unit Tests |
| **5. Template Engine** | T-040 ~ T-043 | 3 Days | Jinja2 Templates (C#, Py, JSON) |
| **6. CLI Interface** | T-050 ~ T-052 | 2 Days | CLI (create, batch) |
| **7. GUI Interface** | T-060 ~ T-061 | 2 Days | CustomTkinter GUI |
| **8. Build & Deploy** | T-070 ~ T-071 | 1 Day | PyInstaller Spec, Scripts |
| **9. Test & Quality** | T-080 ~ T-082 | 3.5 Days | 90% Coverage, Integration Test |
| **10. Release** | T-090 ~ T-092 | 2.5 Days | User Guide, v1.0 Release |

**Total Estimated Duration**: ~20 Days

## Sprint Backlog

### Sprint 1: Core Engine (Days 1-5)
- [x] T-001 PRD
- [x] T-002 TRD
- [x] T-003 WBS
- [ ] T-010 Project Init
- [ ] T-011 Env Setup
- [ ] T-020 CombatParams
- [ ] T-021 Validation
- [ ] T-030 Scenarios
- [ ] T-031 Edge Cases

### Sprint 2: CLI & Templates (Days 6-10)
- [ ] T-032 Edge Case Tests
- [ ] T-040 C# Template
- [ ] T-041 Python Template
- [ ] T-042 JSON Template
- [ ] T-043 Renderer Facade
- [ ] T-050 CLI Skeleton

### Sprint 3: GUI & Integration (Days 11-15)
- [ ] T-051 CLI Create
- [ ] T-052 CLI Batch
- [ ] T-060 GUI UI
- [ ] T-061 GUI Logic

### Sprint 4: Polish & Release (Days 16-20)
- [ ] T-070 Build Spec
- [ ] T-071 Build Scripts
- [ ] T-080 Unit Tests
- [ ] T-081 Integration Tests
- [ ] T-082 Perf Tests
- [ ] T-090 User Guide
- [ ] T-091 Dev Guide
- [ ] T-092 Release
