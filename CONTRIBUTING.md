# Contributing to e-Citizen Kenya

Thank you for your interest in contributing to Kenya's digital government platform. This document outlines the process for contributing code, reporting issues, and proposing improvements.

## Code of Conduct

This project adheres to a standard code of conduct. By participating, you agree to:

- **Be respectful** — Treat all contributors with respect. Harassment, personal attacks, and discriminatory language are not tolerated.
- **Be collaborative** — Work together constructively. Assume good faith in others' contributions and feedback.
- **Be patient** — Not everyone has the same context or expertise. Take time to explain your reasoning.
- **Follow Kenyan law** — This is a government platform. Contributions must comply with the Constitution of Kenya, the Data Protection Act (2019), and all applicable Kenyan laws.

## How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:

1. **Title** — A clear, concise description of the problem
2. **Environment** — Python version, Django version, database, browser
3. **Steps to reproduce** — Exact steps that trigger the bug
4. **Expected behavior** — What you expected to happen
5. **Actual behavior** — What actually happened, including error messages and screenshots
6. **Severity** — How critical is this? (critical / major / minor / cosmetic)

### Suggesting Features

Feature requests are welcome. Open an issue with:

1. **Problem statement** — What problem does this solve for Kenyan citizens?
2. **Proposed solution** — How should it work? Include mockups or examples if possible.
3. **Alternatives considered** — What other approaches did you think about?
4. **Scope** — Is this national, county-level, or both?

### Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Name your branch** descriptively: `feature/county-weather-alerts`, `fix/mpesa-callback-timeout`, `docs/api-authentication`
3. **Keep changes focused** — One PR should address one concern
4. **Follow the code style** — Match the existing patterns in the codebase:
   - Django class-based views for APIs, function-based views for web pages
   - Tailwind CSS utility classes matching the design system (`#0b6e4f` green, `#111418` dark, `#60758a` muted, `#dbe0e6` border)
   - Responsive breakpoints: `sm:` 640px, `md:` 768px, `lg:` 1024px
   - Template includes for reusable UI components
   - `@login_required` on all citizen-facing views that need authentication
5. **Write tests** for new functionality
6. **Update documentation** if your changes affect the API, setup process, or user-facing features
7. **Run checks before submitting**:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

### Commit Messages

Write commits in the imperative mood:

```
add passport renewal workflow with document checklist
fix session expiry during M-Pesa payment callback
update county geolocation to use Haversine formula
```

Keep the first line under 72 characters. Add detail in the body if needed.

## Development Setup

See the [README](README.md#getting-started) for setup instructions.

### Project Conventions

- **URL names**: Use descriptive names — `county_detail`, `service_detail`, `ministry_list`
- **Template paths**: `apps/<app>/templates/<app>/<page>.html`
- **Static files**: App-specific static files go in `apps/<app>/static/<app>/`
- **Forms**: Use Django forms with explicit widget attrs (Tailwind classes)
- **Views**: Web views in `views/web.py`, API views in `views/api.py`
- **URLs**: Web URLs in `urls/web.py`, API URLs in `urls/api.py`
- **Services**: Business logic in `services.py`, not in views or models
- **Tasks**: Async processing in `tasks.py` with Celery
- **Tests**: Mirror the app structure in `tests/` directories

### Database Changes

- Always create migrations with `python manage.py makemigrations`
- Include both the migration file and the model change in your PR
- For seed data, use management commands or fixtures
- Do not include `db.sqlite3` or any database dumps in commits

### Security

- Never commit secrets, API keys, or credentials — use environment variables
- All user input must be validated server-side
- Payment flows must verify callbacks from M-Pesa
- Personal data handling must comply with Kenya's Data Protection Act (2019)
- Run `python manage.py check --deploy` before submitting security-sensitive changes

## Review Process

1. A maintainer will review your PR within 3-5 business days
2. Automated checks must pass (Django checks, migrations, tests)
3. At least one approving review is required before merge
4. The reviewer may request changes — this is normal and collaborative
5. Once approved, a maintainer will merge your PR

## Getting Help

- [README](README.md) — Project overview and setup
- [SUPPORT.md](SUPPORT.md) — Where to ask questions
- [Issue Tracker](https://github.com/Kandemark/ecitizen/issues) — Bug reports and feature requests

Thank you for helping build a better digital government for Kenya.
