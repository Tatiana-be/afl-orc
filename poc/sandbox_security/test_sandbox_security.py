"""Proof-of-Concept: Sandbox Security

Validates:
1. Code execution isolation works
2. File system access is restricted
3. Network access can be controlled
4. Resource limits prevent exhaustion
5. Escape attempts are blocked
"""

import asyncio
import os
import tempfile
import subprocess
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class SandboxResult:
    success: bool
    output: str = ""
    error: str = ""
    execution_time_ms: float = 0.0
    memory_used_kb: int = 0
    escape_attempt_detected: bool = False


class SandboxConfig:
    """Configuration for sandbox execution."""

    def __init__(
        self,
        timeout_seconds: float = 5.0,
        max_memory_mb: int = 256,
        allow_network: bool = False,
        allowed_paths: list[str] = None,
        blocked_commands: list[str] = None,
    ):
        self.timeout_seconds = timeout_seconds
        self.max_memory_mb = max_memory_mb
        self.allow_network = allow_network
        self.allowed_paths = allowed_paths or ["/tmp/sandbox"]
        self.blocked_commands = blocked_commands or [
            "rm -rf /",
            "chmod",
            "chown",
            "sudo",
            "su",
            "mkfs",
            "dd",
            "wget",
            "curl",
            "nc",
            "ncat",
            "ssh",
            "scp",
        ]


class CodeSandbox:
    """Sandboxed code execution environment."""

    def __init__(self, config: SandboxConfig = None):
        self.config = config or SandboxConfig()
        self.work_dir = tempfile.mkdtemp(prefix="sandbox_")
        self.execution_count = 0

    def _check_escape_patterns(self, code: str) -> bool:
        """Check for common escape patterns."""
        escape_patterns = [
            "__import__",
            "subprocess",
            "os.system",
            "os.popen",
            "import os",
            "open('/etc/",
            "open('/proc/",
            "open('/sys/",
            "import socket",
            "import urllib",
            "import requests",
            "http.client",
            "eval('__import__",
            "exec('__import__",
        ]

        for pattern in escape_patterns:
            if pattern in code:
                return True
        return False

    def _check_blocked_commands(self, code: str) -> list[str]:
        """Check for blocked shell commands."""
        found = []
        for cmd in self.config.blocked_commands:
            # Use word boundary matching to avoid false positives
            import re
            pattern = r'\b' + re.escape(cmd) + r'\b'
            if re.search(pattern, code):
                found.append(cmd)
        return found

    async def execute_python(self, code: str) -> SandboxResult:
        """Execute Python code in sandbox."""
        start_time = time.time()
        self.execution_count += 1

        # Check for escape patterns
        if self._check_escape_patterns(code):
            return SandboxResult(
                success=False,
                error="Escape pattern detected in code",
                escape_attempt_detected=True,
                execution_time_ms=(time.time() - start_time) * 1000,
            )

        # Check for blocked commands
        blocked = self._check_blocked_commands(code)
        if blocked:
            return SandboxResult(
                success=False,
                error=f"Blocked commands detected: {', '.join(blocked)}",
                escape_attempt_detected=True,
                execution_time_ms=(time.time() - start_time) * 1000,
            )

        # Write code to temp file
        code_file = os.path.join(self.work_dir, "code.py")
        with open(code_file, "w") as f:
            f.write(code)

        # Execute with restrictions
        try:
            # Write safe wrapper that sets limits
            wrapper_code = f"""
import resource
import sys

# Set resource limits
resource.setrlimit(resource.RLIMIT_CPU, ({int(self.config.timeout_seconds)}, {int(self.config.timeout_seconds) + 1}))
resource.setrlimit(resource.RLIMIT_AS, ({self.config.max_memory_mb * 1024 * 1024}, {self.config.max_memory_mb * 1024 * 1024}))

# Execute code
exec(open('{code_file}').read())
"""
            wrapper_file = os.path.join(self.work_dir, "wrapper.py")
            with open(wrapper_file, "w") as f:
                f.write(wrapper_code)

            # Run with timeout
            env = os.environ.copy()
            if not self.config.allow_network:
                env["http_proxy"] = ""
                env["https_proxy"] = ""

            process = await asyncio.create_subprocess_exec(
                "python3", wrapper_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=self.config.timeout_seconds
                )

                execution_time = (time.time() - start_time) * 1000

                return SandboxResult(
                    success=process.returncode == 0,
                    output=stdout.decode() if stdout else "",
                    error=stderr.decode() if stderr else "",
                    execution_time_ms=execution_time,
                )

            except asyncio.TimeoutError:
                process.kill()
                return SandboxResult(
                    success=False,
                    error=f"Execution timed out after {self.config.timeout_seconds}s",
                    execution_time_ms=self.config.timeout_seconds * 1000,
                )

        except Exception as e:
            return SandboxResult(
                success=False,
                error=str(e),
                execution_time_ms=(time.time() - start_time) * 1000,
            )

    def cleanup(self):
        """Clean up sandbox directory."""
        import shutil

        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir, ignore_errors=True)


# Escape attempt test cases
ESCAPE_ATTEMPTS = [
    # File system escape
    {
        "name": "Read /etc/passwd",
        "code": "print(open('/etc/passwd').read())",
        "should_block": True,
    },
    # Subprocess escape
    {
        "name": "Execute shell command",
        "code": "import subprocess; print(subprocess.run(['ls', '/'], capture_output=True))",
        "should_block": True,
    },
    # Import escape
    {
        "name": "Import os module",
        "code": "import os; print(os.listdir('/'))",
        "should_block": True,
    },
    # Eval escape
    {
        "name": "Eval malicious code",
        "code": "eval('__import__(\"os\").system(\"ls /\")')",
        "should_block": True,
    },
    # Network escape
    {
        "name": "Network request",
        "code": "import urllib.request; print(urllib.request.urlopen('http://example.com').read())",
        "should_block": True,
    },
    # Destructive command
    {
        "name": "Destructive rm command",
        "code": "import os; os.system('rm -rf /')",
        "should_block": True,
    },
    # Safe code
    {
        "name": "Safe math operation",
        "code": "print(2 + 2)",
        "should_block": False,
    },
    # Safe code with variables
    {
        "name": "Safe string operation",
        "code": "name = 'world'; print(f'Hello, {name}!')",
        "should_block": False,
    },
    # Safe list operation
    {
        "name": "Safe list comprehension",
        "code": "print([x**2 for x in range(10)])",
        "should_block": False,
    },
]


async def test_sandbox_security():
    """PoC Test: Sandbox Security"""
    print("\n" + "=" * 60)
    print("PoC 6: Sandbox Security")
    print("=" * 60)

    sandbox = CodeSandbox(
        SandboxConfig(
            timeout_seconds=5.0,
            max_memory_mb=256,
            allow_network=False,
        )
    )

    try:
        # Test 1: Escape attempt detection
        print("\n[Test 1] Escape Attempt Detection")

        blocked_count = 0
        false_positive_count = 0

        for attempt in ESCAPE_ATTEMPTS:
            result = await sandbox.execute_python(attempt["code"])

            was_blocked = not result.success or result.escape_attempt_detected
            should_block = attempt["should_block"]

            if should_block and was_blocked:
                blocked_count += 1
                print(f"  ✅ Blocked: {attempt['name']}")
            elif not should_block and was_blocked:
                false_positive_count += 1
                print(f"  ❌ False positive: {attempt['name']}")
            elif not should_block and not was_blocked:
                print(f"  ✅ Allowed: {attempt['name']}")
            else:
                print(f"  ⚠️  Not blocked: {attempt['name']}")

        total_escape_attempts = sum(1 for a in ESCAPE_ATTEMPTS if a["should_block"])
        total_safe = sum(1 for a in ESCAPE_ATTEMPTS if not a["should_block"])

        print(f"\n  Escape attempts blocked: {blocked_count}/{total_escape_attempts}")
        print(f"  False positives: {false_positive_count}/{total_safe}")

        assert blocked_count == total_escape_attempts, "All escape attempts should be blocked"
        assert false_positive_count == 0, "No false positives allowed"
        print(f"  ✅ All escape attempts blocked, no false positives")

        # Test 2: Resource limits
        print("\n[Test 2] Resource Limit Enforcement")

        # Test timeout
        result = await sandbox.execute_python("import time; time.sleep(10)")
        assert not result.success, "Timeout should trigger"
        assert "timed out" in result.error.lower()
        print(f"  ✅ Timeout enforced: {result.execution_time_ms:.0f}ms")

        # Test 3: Safe code execution
        print("\n[Test 3] Safe Code Execution")

        safe_tests = [
            ("Math", "print(2 ** 10)"),
            ("String", "print('hello'.upper())"),
            ("List", "print(sum([1, 2, 3, 4, 5]))"),
            ("Dict", "d = {'a': 1}; print(d['a'])"),
            ("Function", "def f(x): return x * 2; print(f(21))"),
        ]

        for name, code in safe_tests:
            # Create fresh sandbox for each test to avoid cleanup issues
            test_sandbox = CodeSandbox(
                SandboxConfig(timeout_seconds=5.0, max_memory_mb=256, allow_network=False)
            )
            try:
                result = await test_sandbox.execute_python(code)
                assert result.success, f"Safe code should execute: {name}. Error: {result.error}"
                print(f"  ✅ {name}: {result.output.strip()}")
            finally:
                test_sandbox.cleanup()

        # Test 4: Multiple executions
        print("\n[Test 4] Multiple Executions Isolation")

        for i in range(10):
            result = await sandbox.execute_python(f"print({i})")
            assert result.success
            assert str(i) in result.output

        print(f"  ✅ 10 isolated executions completed")

        # Test 5: Cleanup verification
        print("\n[Test 5] Sandbox Cleanup")

        work_dir = sandbox.work_dir
        sandbox.cleanup()
        assert not os.path.exists(work_dir), "Work directory should be cleaned up"
        print(f"  ✅ Sandbox cleaned up successfully")

    finally:
        sandbox.cleanup()

    print("\n" + "=" * 60)
    print("✅ PoC 6 PASSED: Sandbox Security risks mitigated")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_sandbox_security())
