# ARCHIVE — report.md

> **Застарілий:** весь звіт і таблиця вразливостей перенесені в `README.md`. Будь ласка, дивіться `README.md` для повної інформації.
Шаблон та запущений локально контейнер OWASP Juice Shop мають кілька архітектурних дефектів, які ускладнюють автоматизоване тестування та контроль (хардкод‑секрети, публічний доступ до логів, відкритий OpenAPI, старі залежності). Нижче — перелік виявлених проблем, їхній вплив і рекомендації.

---

### 🔴 Виявлені проблеми (мінімум 5)
1. Хардкод secret у коді (`cookieParser('kekse')`) — PoLP/секрет‑менеджмент. Рішення: Vault CSI / secretKeyRef.
2. Directory listing та публічні логи (`/ftp`, `/support/logs`) — Information Disclosure. Рішення: прибрати serve-index, захистити RBAC.
3. Відкритий CORS і вимкнені XSS фільтри — Surface increase. Рішення: whitelist origin, CSP/helmet.
4. Старі/вразливі залежності (`jsonwebtoken@0.4.0`, `js-yaml@3.x`) — SCA risk. Рішення: SBOM + SCA, оновлення пакетів.
5. Публічний `/api-docs` — DAST‑сигнал (корисно для тестів), але треба контролювати у проді.

---

## ✅ Чеклист сигналів
| Сигнал / Контроль               | Є / Немає |
|---------------------------------|-----------|
| OpenAPI / `response_model`      | ✅        |
| SBOM / package script           | ✅        |
| CI перевірки (Trivy, Semgrep)   | ❌        |
| Secrets через Vault / CSI       | ❌        |
| Image pinning / digest          | ✅        |

---

## Інструменти

| Інструмент | Призначення | Примітки |
|---|---|---|
| Postman | Надсилання запитів до API | Ручне тестування / сценарії |
| jwt.io | Перевірка / декодування JWT | Не зберігати секрети в сторонніх сервісах |
| Браузер | Перегляд веб‑інтерфейсу | Функціональна перевірка, DAST‑огляд |
| Notepad / Word / Google Docs | Оформлення звіту | Підготовка deliverables для LMS / репо |

---

## Пріоритетні кроки (рекомендації)
1. Міграція секретів у Vault CSI / Kubernetes Secret (критично).
2. Закрити або захистити `/ftp`, `/support/logs` (високий пріоритет).
3. Додати SBOM/SCA у CI (syft, trivy/grype) і оновити залежності.
4. Обмежити CORS / увімкнути CSP та helmet XSS‑фільтр.
5. Обмежити доступ до `/api-docs` у продакшн.

---

## Файли з прикладами виправлень (fix/)
- `fix/` — приклади конфігурацій і код‑фрагментів для виправлення хардкод‑секретів, CI та probes.

---

_Звіт підготовлено відповідно до `task.md` — мінімум 5 проблем, опис порушених принципів та практичні пропозиції виправлення._

---

## 🔒 Vulnerabilities (liste provided — require SBOM/SCA verification)
Нижче — CVE, які ти навів; у колонці **Status** вказано, чи підтверджено на основі `package.json` / runtime, або потребує підтвердження через SBOM/SCA (Trivy/Grype).

| CVE | Severity | Пакет | Версія | Status | Recommendation |
|---|---:|---|---:|---|---|
| CVE-2023-37903 | 9.8 | vm2 | 3.9.17 | Needs SBOM (not top-level) | If present (transitive) → upgrade/remove vm2; avoid running untrusted code in sandboxed vm2 instance |
| CVE-2023-32314 | 9.8 | vm2 | 3.9.17 | Needs SBOM (not top-level) | Same as above — patch or remove dependency |
| CVE-2026-22709 | 9.8 | vm2 | 3.9.17 | Needs SBOM (not top-level) | Same as above |
| CVE-2023-37466 | 9.8 | vm2 | 3.9.17 | Needs SBOM (not top-level) | Same as above |
| CVE-2021-44906 | 9.8 | minimist | 0.2.4 | Needs SBOM (not top-level) | If found → update minimist to patched version or remove transitive dependency |
| CVE-2025-55130 | 9.1 | node (runtime) | 22.21.1 | Confirmed (container runtime) | Upgrade Node to patched release or apply runtime mitigation; validate compatibility |
| CVE-2019-10744 | 9.1 | lodash | 2.4.2 | Needs SBOM (not top-level) | Update lodash to safe version or remove vulnerable transitive dep |
| CVE-2023-46233 | 9.1 | crypto-js | 3.3.0 | Needs SBOM (not top-level) | Replace / update crypto-js to patched release |
| CVE-2015-9235 | N/A | jsonwebtoken | 0.1.0+ | Confirmed (package.json shows `jsonwebtoken@0.4.0`) | Upgrade `jsonwebtoken` to a patched major or migrate to modern JWT library (e.g., `jose`) and revalidate auth flows |
| GHSA-5mrr-rgp6-x4gr | N/A | marsdb | 0.6.11 | Confirmed (top-level dep) | Check advisory details; update/remove marsdb or apply mitigations |

> Note: many packages above may be **transitive** (not listed in top-level `package.json`). A full SBOM and SCA scan (syft → trivy/grype) is required to confirm presence and exact version ranges.

### How to verify locally (commands)
```bash
# generate SBOM for image
syft bkimminich/juice-shop:latest -o cyclonedx-json > sbom-image.json

# scan image for vulnerabilities
trivy image --format json --output trivy-image.json bkimminich/juice-shop:latest
# or
grype bkimminich/juice-shop:latest -o json > grype-image.json

# scan source (package.json)
npm run sbom    # generates bom.json / bom.xml
npm audit fix --package-lock-only
```

---


