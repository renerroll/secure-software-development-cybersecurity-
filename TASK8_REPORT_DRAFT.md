# Task 8 — Аналіз результатів CI/CD та DevSecOps

**Репозиторій (GitHub):** https://github.com/renerroll/secure-software-development-cybersecurity-/tree/lesson8-1

**Репозиторій (GitLab):** https://gitlab.com/renerroll/cybersecurity/-/tree/lesson8-1

---

## Короткий огляд (мета)
Мета — показати розуміння принципів інтеграції безпеки в CI/CD, проаналізувати два запуски пайплайну (успішний і провальний) та підготувати рекомендації.

---

## Практична частина — докази
- Релевантні коміти:
  - `2521f4a` — tests: GOOD — expected pass
  - `cb45a93` — tests: BAD — expected fail
- Архів для здачі: `lab8_submission.zip` (створено локально)

### Локальні тести — GOOD (очікувано PASS)
```
3 passed in 0.10s
```
(Файл з виводом: `pytest_good_local.txt`)

### Локальні тести — BAD (очікувано FAIL)
```
FAILED test_app.py::test_hello_world - AssertionError: assert b'Hello, Evil World!' in b'<p>Hello, World!</p>'
FAILED test_app.py::test_dangerous_endpoint - AssertionError: expected call not found.
2 failed, 1 passed in 0.08s
```
(Файл з виводом: `pytest_bad_local.txt`)

---

## Аналітична частина — відповіді на завдання

### Завдання 1 — Успіх vs. Провал
Ключова різниця: різні тестові набори (`good` vs `bed`) — у `bed` є навмисні помилки, що викликають провал на етапі тестів. Доказ: лог `pytest_bad_local.txt` (див. вивід вище).

### Завдання 2 — Безпека першого випадку
`Good` код не означає «нуль вразливостей». Автоматичні SAST/SCA/DAST не завжди виявляють: логіку бізнес‑помилок, 0‑day, runtime misconfiguration, уразливості у зовнішніх сервісах, ланцюжки постачання (supply‑chain).

### Завдання 3 — Принцип Fail Fast
Подвійний запуск ілюструє fail‑fast: невірний код зупиняє пайплайн на ранньому етапі (тести/сканери), що економить ресурси і дає швидкий фідбек розробнику.

### Завдання 4 — Етапи CI/CD (з `gitlab-ci.yml`)
- `secret-scan` — пошук секретів у коді
- `sast` — статичний аналіз коду
- `test` — юніт‑тести (pytest)
- `build` — збірка Docker‑образу
- `sca` — аналіз залежностей / container scanning
- `deploy` — розгортання контейнера (локально в CI‑job)
- `dast` — динамічний аналіз запущеного додатку

### Завдання 5 — Які сканери використовуються
- SAST — шукає небезпечні виклики в коді (наприклад, eval, command injection)
- DAST — виявляє вразливості на працюючому хості (XSS, auth flaws)
- Secret detection — пошук секретів у репо
- Dependency scanning / SCA — виявлення вразливих пакетів (CVE)

### Завдання 6 — Реакція на вразливості
Логіка у `gitlab-ci.yml`: jobs мають `allow_failure: false` → при виявленні критичних знахідок job падає, CI зупиняється; шаблони GitLab генерують звіти в UI і можуть надсилати повідомлення через інтеграції (e‑mail, webhook, issue creation).

### Завдання 7 — Реакція на CVE (playbook)
1. Оцінка впливу (SBOM → виявити використання у проєкті)
2. Пошук рішення (оновлення пакета, patch, заміна або mitigation)
3. Тестування змін у feature branch + CI
4. Розгортання through staged environment (canary, blue/green)
5. Документування (incidence ticket, CVE reference)
6. Post‑incident review (root cause, KPT)

### Завдання 8 — Автоматизація SBOM‑аналізу
Інструменти: Trivy, Grype, OSV‑Scanner, Dependabot/ Renovate. Ідеальний workflow: CI створює SBOM → SCA сканує → тригерити автo‑MR для безпечних оновлень або створювати high‑severity issues/alerts.

### Завдання 9 — Покращення пайплайну (2–3 ідеї)
1. Авто‑MR для оновлення залежностей (Renovate) — знижує час на ремедіацію CVE.
2. Дашборд вразливостей + метрики SLA на фікс (Time‑to‑fix) — підвищує прозорість.
3. Політики gating (severity thresholds) та зручні звіти у MR — кращий фідбек для розробників.

---

## Додатки (файли)
- `pytest_good_local.txt` — успішний прогін тестів
- `pytest_bad_local.txt` — провальний прогін тестів
- `gitlab-ci_snippet.txt` — уривок `gitlab-ci.yml`
- `gitlog.txt` — останні коміти
- `lab8_submission.zip` — архів репозиторію (підготовлено)

---

_Підпис:_ `renerroll` — готово для фіналізації та завантаження в Google Docs.
