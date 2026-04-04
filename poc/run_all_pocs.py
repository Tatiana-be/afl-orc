"""Run all Proof-of-Concept tests."""

import asyncio
import os
import sys
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def run_all_pocs():
    """Run all PoC tests and report results."""
    print("\n" + "=" * 70)
    print(" " * 15 + "AFL ORCHESTRATOR: PROOF-OF-CONCEPT")
    print(" " * 20 + "Key Risk Validation")
    print("=" * 70)

    start_time = time.time()
    results = {}

    # PoC 1: LLM Integration
    try:
        print("\n" + "─" * 70)
        print("Running PoC 1: LLM Integration...")
        from poc.llm_integration.test_llm_integration import test_llm_integration

        await test_llm_integration()
        results["LLM Integration"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 1 FAILED: {e}")
        results["LLM Integration"] = f"❌ FAILED: {e}"

    # PoC 2: Context Manager
    try:
        print("\n" + "─" * 70)
        print("Running PoC 2: Context Manager...")
        from poc.context_manager.test_context_manager import test_context_manager

        await test_context_manager()
        results["Context Manager"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 2 FAILED: {e}")
        results["Context Manager"] = f"❌ FAILED: {e}"

    # PoC 3: Guardrail Engine
    try:
        print("\n" + "─" * 70)
        print("Running PoC 3: Guardrail Engine...")
        from poc.guardrail_engine.test_guardrail_engine import test_guardrail_engine

        await test_guardrail_engine()
        results["Guardrail Engine"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 3 FAILED: {e}")
        results["Guardrail Engine"] = f"❌ FAILED: {e}"

    # PoC 4: Budget Tracking
    try:
        print("\n" + "─" * 70)
        print("Running PoC 4: Budget Tracking...")
        from poc.budget_tracking.test_budget_tracking import test_budget_tracking

        await test_budget_tracking()
        results["Budget Tracking"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 4 FAILED: {e}")
        results["Budget Tracking"] = f"❌ FAILED: {e}"

    # PoC 5: Workflow Recovery
    try:
        print("\n" + "─" * 70)
        print("Running PoC 5: Workflow Recovery...")
        from poc.workflow_recovery.test_workflow_recovery import test_workflow_recovery

        await test_workflow_recovery()
        results["Workflow Recovery"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 5 FAILED: {e}")
        results["Workflow Recovery"] = f"❌ FAILED: {e}"

    # PoC 6: Sandbox Security
    try:
        print("\n" + "─" * 70)
        print("Running PoC 6: Sandbox Security...")
        from poc.sandbox_security.test_sandbox_security import test_sandbox_security

        await test_sandbox_security()
        results["Sandbox Security"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 6 FAILED: {e}")
        results["Sandbox Security"] = f"❌ FAILED: {e}"

    # PoC 7: Database Scaling
    try:
        print("\n" + "─" * 70)
        print("Running PoC 7: Database Scaling...")
        from poc.db_scaling.test_db_scaling import test_db_scaling

        await test_db_scaling()
        results["Database Scaling"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 7 FAILED: {e}")
        results["Database Scaling"] = f"❌ FAILED: {e}"

    # PoC 8: Concurrent Workflows
    try:
        print("\n" + "─" * 70)
        print("Running PoC 8: Concurrent Workflows...")
        from poc.concurrent_workflows.test_concurrent_workflows import test_concurrent_workflows

        await test_concurrent_workflows()
        results["Concurrent Workflows"] = "✅ PASSED"
    except Exception as e:
        print(f"\n❌ PoC 8 FAILED: {e}")
        results["Concurrent Workflows"] = f"❌ FAILED: {e}"

    # Summary
    total_time = time.time() - start_time
    passed = sum(1 for r in results.values() if "PASSED" in r)
    failed = sum(1 for r in results.values() if "FAILED" in r)

    print("\n" + "=" * 70)
    print(" " * 25 + "POC SUMMARY")
    print("=" * 70)
    print(f"\nTotal time: {total_time:.1f}s")
    print(f"Passed: {passed}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    print()

    for name, result in results.items():
        print(f"  {name:30s} {result}")

    print()
    if failed == 0:
        print("🎉 ALL PROOFS-OF-CONCEPT PASSED!")
        print("   Architecture validated, ready for MVP development.")
    else:
        print(f"⚠️  {failed} PoC(s) failed. Review failures above.")

    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_pocs())
    sys.exit(0 if success else 1)
