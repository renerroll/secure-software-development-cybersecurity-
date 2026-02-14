# Task 8 — Розв'язання (DevSecOps / CI·CD аналіз)

Рішення повністю відповідає вимогам з `task8.md` (усі відповіді 1–9, докази, інструкції для перевірки).

## Репозиторій / гілки
- GitHub (branch): `lesson8-1` — https://github.com/renerroll/secure-software-development-cybersecurity-/tree/lesson8-1
- GitLab (branch): `lesson8-1` — https://gitlab.com/renerroll/cybersecurity/-/tree/lesson8-1
- Релевантні коміти:
  - `2521f4a` — tests: GOOD — expected pass
  - `cb45a93` — tests: BAD — expected fail
  - `d51c1ec` — docs: add Task8 report draft + artifacts zip. 

--- 

## Короткий огляд — що зроблено ✅
- Показано два запуски pipeline: **успішний** (GOOD tests) та **провальний** (BAD tests) — демонстрація принципу *fail fast*. 
- Підготовлено аналітичний звіт (в `TASK8_REPORT_DRAFT.md` / `README.md`) та архів `lab8_submission.zip`.
- Додано локальні артефакти тестів (`lab/pytest_good.txt`, `lab/pytest_bad.txt`) і уривок `gitlab-ci.yml` для перевірки.

---

## Практична частина — як відтворити (команди)
1. Створити та активувати venv:
   - python3 -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
2. Перевірити "Good" тест (має пройти):
   - cp good/test_app.py test_app.py
   - pytest -q test_app.py
3. Перевірити "Bad" тест (має впасти):
   - cp bed/test_app.py test_app.py
   - pytest -q test_app.py
4. Коміти для демонстрації в CI:
   - git add test_app.py && git commit -m "tests: GOOD — expected pass" && git push
   - git add test_app.py && git commit -m "tests: BAD — expected fail" && git push

---

## Аналітична частина — відповіді на завдання 1–9

### 1) Успіх vs. Провал
- Причина: різні набори тестів. `good/test_app.py` містить коректні очікування → pipeline проходить; `bed/test_app.py` навмисно має помилки (assertion на інший рядок; перевірка неіснуючого виклику) → юніт‑тести падають і pipeline зупиняється.  
- Доказ: логи `pytest_good_local.txt` (3 passed) і `pytest_bad_local.txt` (2 failed, 1 passed).

### 2) Безпека першого випадку
- "Good" ≠ абсолютна безпека. Автоматичні сканери часто **пропускають**:
  - бізнес‑логіку, ланцюги авторизації/прав доступу;
  - runtime misconfigurations (наприклад, неправильні ACL, привілеї);
  - 0‑day в залежностях та supply‑chain вразливості; 
  - логічні помилки, що не виражаються у сигнатурах сканера.

### 3) Принцип Fail Fast
- Пайплайн зупиняється на ранньому етапі (тести/сканери) — це знижує витрати CI, дає миттєвий зворотний зв'язок розробнику і не пропускає дефекти у наступні етапи (build/deploy).

### 4) Етапи CI/CD (реалізація в `gitlab-ci.yml`)
- `secret-scan` → `sast` → `test` → `build` → `sca`/`container_scanning` → `deploy` → `dast`.
- Для кожного: коротко — пошук секретів, статичний аналіз, юніт‑тести, створення Docker образу, SCA/SBOM + container scan, розгортання у job, динамічний аналіз працюючого сервісу.

### 5) Використовувані сканери і їх роль
- SAST — аналіз вихідного коду (SQLi, command injection, unsafe calls). Ранній етап.
- DAST — сканування працюючої аплікації (runtime issues, втручання через HTTP).
- Secret detection — пошук ключів/паролів у репо.
- Dependency scanning / SCA — пошук уразливих пакетів (CVE), SBOM.

### 6) Реакція на вразливості
- Jobs мають `allow_failure: false` → при критичних знахідках job падає і pipeline зупиняється.  
- GitLab генерує security‑reports (SAST/DAST/SCA) і може відсилати нотифікації/створювати issues/пул‑реквести.

### 7) Реагування на CVE — чіткий протокол
1. Ідентифікація та оцінка впливу (SBOM → визначити версії, де використовується).
2. Швидке рішення: перевірити патч/оновлення → якщо доступне — планувати оновлення; інакше — mitigation/заміну або тимчасовий workaround.
3. Тестування змін у feature‑branch + прогін CI (SAST/SCA/unit/integration).
4. Розгортання через staged rollout (canary/blue‑green) та моніторинг.
5. Документування інциденту (ticket, CVE ID, рішення, ризики).
6. Post‑incident аналіз і оновлення політик (lessons learned).

### 8) Автоматизація SBOM‑аналізу
- Інструменти: **Trivy**, **Grype**, **OSV‑Scanner**, **Dependabot / Renovate**.
- Ідеальний workflow: при build CI генерує SBOM → SCA сканер перевіряє на CVE → при low/medium — автоматичний MR (Renovate); при high/critical — створюється urgent issue + alert на Slack/Email + block merge до фіксу.

### 9) Покращення пайплайну (конкретні ідеї)
1. Авто‑MR для оновлення залежностей (Renovate) — скорочує time‑to‑remediate.  
2. Security‑dashboard + метрики (Time‑to‑Fix, #critical open) — підвищує прозорість і пріоритезацію.  
3. Політики gating (severity thresholds) + ясні MR‑security‑checks — краще UX для розробників.

---

## Докази / артефакти для перевірки
- Логи тестів: `lab/pytest_good.txt`, `lab/pytest_bad.txt`  
- Уривок CI: `lab/gitlab-ci_snippet.txt`  
- Коміти: `2521f4a` (GOOD), `cb45a93` (BAD), `d51c1ec` (документи)  
- Архів для здачі: `lab8_submission.zip` (у корені гілки)

---

## Покрокові рекомендації для здачі
1. Переконайтесь, що у GitLab є два запуску pipeline (успішний і провальний) для `lesson8-1` — зробіть скриншоти і додайте їх у звіт.
2. Додайте у звіт короткі уривки логів (які вже є у `lab/`), хеші комітів та посилання на гілку.
3. Підготуйте Google Doc (можна експорт з цього README) і додайте посилання у LMS.

---

Якщо хочеш — перенесу цей README у Google Doc та додам скриншоти pipeline (попроси «Зроби Google Doc»).