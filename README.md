# Розв'язок лабораторної: Практична криптографія

## Коротко
Цей файл — готове рішення завдання з `lab.md`. Наведено: мінімум три помилки в кожному з трьох YAML‑файлів, пояснення чому це небезпечно, рекомендації щодо виправлення та приклад безпечної конфігурації (YAML) з коментарями.

---

## Таблиця 1 — Помилки в конфігураціях
| Файл | Помилка | Чому це помилка | Як виправити |
|---|---|---|---|
| `crypto_config_we.yaml` | `jwt.algorithm: none` / `verify_signature: false` | Токени не підписуються — можна підробити токен (втрата цілісності/автентифікації) | Використовувати підпис (RS256/PS256 або HS256 з надійним секретом). Вимагати `exp`, `aud`, `iss`. |
| `crypto_config_we.yaml` | `passwords.hash_function: sha1` | SHA‑1 — занадто швидкий й вразливий до брутфорсу | Використовувати Argon2id або bcrypt з унікальним salt і адекватними cost‑параметрами. |
| `crypto_config_we.yaml` | `encryption.algorithm: AES-CBC` + `iv_strategy: fixed_iv` | Фіксований IV робить шифрування вразливим (повторюваність, padding oracle) | Використовувати AEAD (AES‑GCM) з унікальним випадковим nonce; ключі в Vault/KMS. |
| `crypto_config_le.yaml` | `jwt.shared_secret: "hardcoded-secret"` | Хардкод секрету у конфігурації — витік, неможлива ротація | Зберігати секрети у Vault/KMS; використовувати `secretKeyRef`/env + ротацію. |
| `crypto_config_le.yaml` | `passwords.salt: fixed_salt` | Однаковий salt для всіх паролів — уразливість до rainbow tables | Генерувати випадковий salt для кожного паролю (зберігати разом із хешем). |
| `crypto_config_le.yaml` | `encryption.algorithm: DES` / `key_storage: hardcoded` | DES застарілий; ключі в коді — критична помилка | Перейти на AES‑GCM 256 і зберігати ключі у Vault/KMS; додати key rotation. |
| `crypto_config_mi.yaml` | `passwords` params занизькі (`time_cost:1`, `memory_cost:1024`) | Argon2 з низькими параметрами неефективний проти атак | Підібрати адекватні параметри (наприклад, time_cost ≥3, memory_cost_kb ≥65536). |
| `crypto_config_mi.yaml` | `encryption.iv_strategy: fixed_iv` | Фіксований IV навіть для AEAD (або повторюваний nonce) призводить до компрометації | Використовувати унікальний рандомний nonce/IV для кожного шифрування. |
| `crypto_config_mi.yaml` | (JWT) відсутні перевірки `aud`/`iss`/`exp` | Відсутність валідації claims → replay/forgery ризики | Вимагати `exp_required: true`, перевірки `aud` та `iss`, короткі TTL.

---

## Таблиця 2 — Власна безпечна конфігурація (YAML)
```yaml
jwt:
  algorithm: RS256
  key_source: vault_or_jwks       # ключі беруться з Vault або JWKS
  verify_signature: true
  claims:
    exp_required: true
    aud_check: true
    iss_check: true
    leeway_seconds: 60

passwords:
  algorithm: argon2id
  time_cost: 3
  memory_cost_kb: 65536
  parallelism: 4
  salt_length_bytes: 16
  pepper: env:APP_PEPPER          # optional, from Vault/KMS

encryption:
  algorithm: AES-GCM
  key_length: 256
  nonce_strategy: random_unique_per_message
  key_storage: vault_kms
  aad: application-specific-metadata
  key_rotation_interval_days: 90
```

### Короткі пояснення вибору
- RS256 + JWKS/Vault дозволяє керувати ключами й ротацією без перезапуску сервісів.
- Argon2id з налаштованими параметрами забезпечує стійкість паролів до сучасних атак.
- AES‑GCM — AEAD режим для одночасної конфіденційності і цілісності; ніколи не використовувати фіксований IV.
- Секрети та ключі зберігайте у Vault/KMS, не хардкодьте у конфігурації/коді.

---

## Як перевірити (коротко)
- JWT: тестувати підроблені токени, перевірити `exp`, `aud`, `iss` у unit/integration тестах.
- Паролі: перевірити хеш/верифікацію з Argon2 (різні salts, pepper відсутній у записі).
- Шифрування: перевірити унікальність nonce для повторних операцій; додати тести на AAD.

---

## Де покласти результати
- Додати `crypto_config_secure.yaml` у папку `fix/`.
- Додати приклади unit‑тестів у `test/` (JWT validation, password hash checks, nonce reuse test).

---

Якщо потрібно, можу автоматично створити `fix/crypto_config_secure.yaml` та додати unit‑тести — скажи `Fix`; або закомітити і відкрити PR — скажи `PR`.