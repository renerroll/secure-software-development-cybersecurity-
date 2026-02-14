# Підсумок домашнього завдання — Аналіз безпеки (SAST / DAST / IAST / RASP)

Коротко: цей файл — стисла та структурована відповідь на пункти з `task.md` (завдання 1–3). Усі технічні артефакти — у робочій папці (Semgrep звіт: `results_semgrep.json`; DAST — ручні PoC записані в `lab6.md`).

---

## 1) Комбінація підходів (Task 1) ✅
Таблиця: вразливість → метод виявлення → інструмент → етап SSDLC

| Вразливість | Можна виявити через | Інструмент | Етап SSDLC |
|---|---:|---|---|
| Hard‑coded JWT secret | ✅ SAST | Semgrep (`lib/insecurity.ts`) | Pull request / pre‑commit |
| SQL Injection (raw queries / ORM) | ✅ SAST, ✅ DAST, ✅ IAST | Semgrep; ручний DAST PoC; IAST (agent) | Code review + Integration tests |
| Stored XSS (reviews) | ✅ DAST, ✅ SAST (частково) | OWASP ZAP (DAST) / manual PoC; Semgrep (pattern) | Staging / runtime testing |
| Unsafe `eval` / Code injection | ✅ SAST, ✅ IAST | Semgrep (`routes/userProfile.ts`); IAST taint traces | Commit / Integration tests |
| Directory listing / exposed keys | ✅ SAST (config), ✅ DAST (runtime) | Semgrep (`fileServer.ts`) + manual HTTP checks (`/encryptionkeys`) | Pre‑deploy scan + staging |
| Open redirect / insecure redirects | ✅ SAST, ✅ DAST | Semgrep (`routes/redirect.ts`) + runtime test | PR checks + staging |

(додаткові деталі й PoC — у `lab6.md`)

---

## 2) Практична симуляція: інтеграція IAST (Task 2) 💡
Вибір: інтегрувати **IAST‑агент** у тестове середовище Juice Shop.

Кроки / середовище:
- Інструмент: Contrast Assess / Seeker / Veracode IAST (приклад). Агент встановлюється поруч із node.js-програмою в тестовому контейнері.
- Де запускати: інтеграційні тести в CI (GitHub Actions) або окрема stage‑середа зі штатними E2E тестами (Cypress/Playwright).
- Які тести: повні API‑інтеграційні тести + фази функціонального сканування (login, search, reviews, file serve).

Очікувані результати / приклад виявлення:
- IAST проводить taint‑tracking: запит → параметр `q` у `/rest/products/search` помічено як tainted → детектує SQLi у `models.sequelize.query(...)` → повертає стек‑трейс, HTTP-запит і фрагмент уразливого коду.
- Аналогічно IAST вкаже на stored XSS у механізмі зберігання відгуків і на hardcoded секрети при інструментальній перевірці конфігурації.

Практична цінність:
- Менше false‑positives, бо IAST працює із runtime‑контекстом; дозволяє пріоритезувати вразливості за експлуатованістю.

---

## 3) Вибір інструментів за типом застосунку (Task 3) 🔧

A) SPA (Angular фронтенд)
- Рекомендовані тести: SAST (JS/TS), DAST (runtime), SCA (залежності), E2E‑security checks.
- Інструменти: Semgrep / ESLint (SAST), OWASP ZAP або Burp (DAST), Snyk/Dependabot (SCA), Cypress + security checks (E2E).
- Інтеграція в pipeline:
  1. PR → Semgrep + ESLint (block on high severity).  
  2. CI build → SCA (PR alerts).  
  3. Nightly staging → DAST (ZAP baseline) + E2E security scenarios.

B) REST API (Node/Express backend)
- Рекомендовані тести: SAST, IAST (integration), DAST (API fuzzing), SCA, runtime logging/monitoring.
- Інструменти: Semgrep (SAST), Contrast (IAST), OWASP ZAP / Postman + Fuzz (DAST), Snyk (SCA).
- Інтеграція в pipeline:
  1. Pre‑merge SAST (Semgrep).  
  2. CI integration: run unit + integration tests with IAST agent attached.  
  3. Pre‑release/staging: automated DAST scan against deployed staging.  
  4. Post‑deploy: RASP / WAF + monitoring for runtime anomalies.

---

## Докази / артефакти (де шукати) 📂
- Semgrep (SAST) JSON‑звіт: `results_semgrep.json` (в робочій папці).  
- Ручні DAST PoC та опис — додані в `lab6.md` (stored XSS, SQLi auth bypass, directory listing, insecure headers).  
- Docker/Запуск Juice Shop: локально на `http://localhost:3000`.

---

## Чек‑лист для здачі (відповідно до критеріїв оцінювання) ✅
- [x] SAST: Semgrep запущено, `results_semgrep.json` — є (мінімум 3 вразливості).  
- [x] DAST: ZAP не вдалося запустити тут, але виконано ручні PoC (мінімум 5 runtime знахідок документовано в `lab6.md`).  
- [x] Порівняльна таблиця SAST vs DAST — є (у `lab6.md` та тут).  
- [x] Завдання 1 — таблиця з прикладами вразливостей — виконано.  
- [x] Завдання 2 — IAST‑сценарій — описано.  
- [x] Завдання 3 — вибір інструментів і pipeline — описано.  
- [x] Висновок (2–3 речення) — є нижче.

---

## Висновок (2–3 речення) ✨
SAST (Semgrep) дає швидкий зворотний зв'язок на рівні коду — ефективний для пошуку hardcoded секретів і pattern‑based issues. DAST підтверджує експлуатованість у runtime (XSS, auth bypass, misconfigurations); IAST додає точності, бо поєднує контекст коду й виконання. Рекомендовано комбінувати всі підходи у CI/CD: SAST → IAST (integration) → DAST (staging) + runtime‑monitoring.

---

Якщо хочеш — згенерую з цього `report.md` або PDF та прикріплю його до архіву для LMS. Хочеш, щоб я підготував готовий Google‑Doc/ZIP для здачі? 📤
