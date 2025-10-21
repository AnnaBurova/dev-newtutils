# 🤝 Contributing Guidelines — *NewtUtils (NewtCode)*

Welcome to the **NewtUtils** project — a collection of developer utilities by *NewtCode*.
To keep this repository clean, consistent, and easy to maintain, please follow the rules below when contributing.

---

## 1. 💬 General Conduct

* Be respectful, constructive, and professional when discussing issues or reviews.
* Focus contributions on improving functionality, maintainability, or documentation.
* Do not include unrelated or sensitive content in commits or pull requests.

---

## 2. 🧩 Types of Contributions

You can contribute by:

* 🧠 **Improving code** — adding features, fixing bugs, or refactoring.
* 📝 **Updating documentation** — improving `README.md`, `INSTALL.md`, or `CHANGELOG.md`.
* ⚙️ **Improving configuration** — updating `.editorconfig`, `.gitattributes`, or build settings.
* 🧪 **Enhancing tests** — adding new test cases under `tests/`.

---

## 3. 🌿 Branching and Commits

### Branch Names

Use clear prefixes for branches:

```
feature/<short-description>
fix/<short-description>
chore/<short-description>
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
feat(scope): Add a new feature
fix(scope): Correct a bug
chore(scope): Routine maintenance or configuration
docs(scope): Documentation updates
style(scope): Formatting or code style only
```

✅ **Tips:**

* Use the **imperative mood** — «Add», «Fix», «Update».
* Keep messages short (~50 characters).
* Make each commit **atomic** — one logical change per commit.

---

## 4. 🔄 Pull Requests

Before submitting a PR:

1. Ensure your branch is up to date with `master`.
2. Describe clearly what was changed and why.
3. Reference related issues or previous discussions.
4. Ensure that the code passes all tests (see below).

---

## 5. 🧪 Testing

All scripts and utilities should be tested in the `tests/` directory.

When adding new functionality:

* Provide at least one test case that demonstrates correct behavior.
* Avoid committing large test data files — use minimal reproducible examples.

---

## 6. 🧰 Code Style and Formatting

* Respect `.editorconfig` and `.gitattributes` settings for line endings and encoding.
* Use meaningful docstrings in **Google style** (`"""Args: Returns: Raises:"""`).
* Avoid wildcard imports (`from x import *`).

---

## 7. 🚀 Versioning and Releases

This project follows **Semantic Versioning (SemVer)**.

* Update `__version__` in `newtutils/__init__.py` and `pyproject.toml` together.
* Document all changes in [CHANGELOG](CHANGELOG.md).
* Use GitHub Releases to create new versions (`v0.x.x` tags).

Example release message:

```
v0.1.3 — Sorting utilities and validation improvements
```

---

## 8. 🧾 Review Process

* All contributions are reviewed before merging.
* Be open to feedback and suggested revisions.
* Once approved, the branch will be merged into `master` and the next release prepared.

---

## ❤️ Thank You

Every contribution helps make **NewtUtils** more useful, reliable, and fun to work with.
Your attention to detail and consistency keeps the *NewtCode* ecosystem growing!
