name: Pull Request Template
about: Create a pull request to contribute to AFL Orchestrator
title: ''
labels: ''
assignees: ''

---

## Description

<!-- Describe your changes in detail -->

## Related Issue

<!-- Please link to the relevant issue using the format: Fixes #123 or Closes #123 -->

Fixes #

## Type of Change

<!-- Mark the appropriate option with an [x] -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📝 Documentation update
- [ ] 🎨 Style/formatting changes
- [ ] ♻️ Code refactoring
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test update (adding or fixing tests)
- [ ] 🔒 Security fix
- [ ] 🚀 CI/CD or deployment changes

## Testing

<!-- Please describe the tests you ran to verify your changes -->

- [ ] Unit tests pass: `pytest tests/unit/`
- [ ] Integration tests pass: `pytest tests/integration/`
- [ ] Linting passes: `pre-commit run --all-files`
- [ ] Type checking passes: `mypy src/`
- [ ] Manual testing performed

### Test Evidence

<!-- Paste test output or screenshots here -->

```bash
# Example:
# pytest tests/unit/test_parser.py -v
```

## Checklist

<!-- Mark items with [x] as you complete them -->

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged and published
- [ ] I have updated the CHANGELOG.md (if applicable)
- [ ] I have updated the API documentation (if applicable)

## Screenshots (if applicable)

<!-- Add screenshots to help explain your changes -->

## Additional Notes

<!-- Any additional information that reviewers should know -->

## Security Considerations

<!-- If your changes affect security, describe the impact -->

- [ ] This change does not expose sensitive data
- [ ] This change does not introduce new security vulnerabilities
- [ ] This change has been reviewed for security implications

## Performance Impact

<!-- If your changes affect performance, describe the impact -->

- [ ] No performance impact expected
- [ ] Performance improved
- [ ] Performance degraded (explain why and mitigation plan)

### Benchmarks (if applicable)

```bash
# Example:
# pytest tests/benchmarks/ -v
```

---

<!-- For more information, see our contributing guidelines -->
