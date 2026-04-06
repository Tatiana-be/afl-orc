# AFL Orchestrator: Бэклог задач для Jira/Linear

**Дата создания**: 2026-03-31 **Дата обновления**: 2026-04-02 **Версия**: 4.0
**На основе ТЗ**: AFL_Orchestrator_TZ_ADD.md v1.0 **Статус**: ✅ Актуализирован
после PoC + Infrastructure Audit + Infra Fixes

---

## Прогресс проекта

| Метрика                    | Значение |
| -------------------------- | -------- |
| **Всего задач**            | 240      |
| **Выполнено**              | 42 (18%) |
| **В работе**               | 0        |
| **Осталось**               | 198      |
| **Story Points всего**     | ~1310    |
| **Story Points выполнено** | ~230     |
| **Прогресс**               | 17.6%    |

---

## Структура эпиков

| Epic ID  | Название                   | Фаза   | Статус         | Задач | Выполнено |
| -------- | -------------------------- | ------ | -------------- | ----- | --------- |
| EPIC-001 | Parser Module              | MVP    | ✅ Complete    | 10    | 10        |
| EPIC-002 | Workflow Engine            | MVP    | 🟡 In Progress | 13    | 3         |
| EPIC-003 | Budget Tracker             | MVP    | 🔴 Not Started | 12    | 0         |
| EPIC-004 | Agent Executor             | MVP    | 🔴 Not Started | 15    | 0         |
| EPIC-005 | Context Manager            | MVP ✅ | 🔴 Not Started | 16    | 0         |
| EPIC-006 | Guardrail Engine           | MVP ✅ | 🔴 Not Started | 18    | 0         |
| EPIC-007 | Storage Layer              | MVP    | 🟡 In Progress | 16    | 2         |
| EPIC-008 | REST API                   | MVP    | 🟡 In Progress | 14    | 1         |
| EPIC-009 | LLM Integrations           | MVP    | 🔴 Not Started | 13    | 0         |
| EPIC-010 | Git Integration            | Alpha  | 🔴 Not Started | 13    | 0         |
| EPIC-011 | Issue Tracker Integration  | Alpha  | 🔴 Not Started | 14    | 0         |
| EPIC-012 | Security & Sandbox         | MVP ✅ | 🟡 In Progress | 14    | 1         |
| EPIC-013 | Monitoring & Observability | MVP ⬆️ | 🟡 In Progress | 22    | 8         |
| EPIC-014 | Deployment & CI/CD         | MVP    | 🟡 In Progress | 16    | 8         |
| EPIC-015 | Proof-of-Concept           | MVP    | ✅ Complete    | 8     | 8         |
| EPIC-016 | Documentation              | MVP    | 🟡 In Progress | 13    | 6         |
| EPIC-017 | Repository Setup           | MVP    | ✅ Complete    | 13    | 13        |
| EPIC-018 | Infrastructure Hardening   | MVP ⭐ | ✅ Complete    | 13    | 13        |

> **Изменения v4.0**: EPIC-018 завершён (13/13). EPIC-013 расширен — 8 задач
> выполнено (JSON логи, Prometheus метрики, Grafana, алерты). EPIC-014 расширен
> — 8 задач выполнено (Python 3.12, GHCR push, staging/prod deploy, OWASP ZAP).
> EPIC-012 — 1 задача выполнена (DAST).

---

## EPIC-001: Parser Module

**Описание**: Парсинг и валидация AFL-конфигураций **Срок**: Недели 1-2
**Ответственный**: Core Team **DoD**: Раздел 5.1.5 ТЗ **Прогресс**: 10/10 задач
(100%) ✅

### Задачи

| ID             | Задача                                        | Тип   | SP  | Приоритет | Статус  | Зависимости    |
| -------------- | --------------------------------------------- | ----- | --- | --------- | ------- | -------------- |
| **PARSER-001** | Настройка проекта Python 3.12+ с pydantic     | Task  | 3   | 🔴 High   | ✅ Done | —              |
| **PARSER-002** | Реализация схемы AFLConfig (Pydantic models)  | Story | 8   | 🔴 High   | ✅ Done | PARSER-001     |
| **PARSER-003** | YAML парсинг с поддержкой anchors/aliases     | Story | 5   | 🔴 High   | ✅ Done | PARSER-002     |
| **PARSER-004** | JSON парсинг (альтернативный формат)          | Task  | 3   | 🟡 Medium | ✅ Done | PARSER-002     |
| **PARSER-005** | Валидация ссылок (agent/artifact/guardrail)   | Story | 5   | 🔴 High   | ✅ Done | PARSER-002     |
| **PARSER-006** | Проверка циклов в графе зависимостей workflow | Story | 8   | 🔴 High   | ✅ Done | PARSER-002     |
| **PARSER-007** | Детализация ошибок (строка/колонка)           | Task  | 5   | 🟡 Medium | ✅ Done | PARSER-003     |
| **PARSER-008** | Версионирование схемы AFL (migration support) | Story | 5   | 🟡 Medium | ✅ Done | PARSER-002     |
| **PARSER-009** | Юнит-тесты парсера (покрытие ≥90%)            | Test  | 8   | 🔴 High   | ✅ Done | PARSER-003-008 |
| **PARSER-010** | Документация API парсера                      | Doc   | 2   | 🟢 Low    | ✅ Done | PARSER-009     |

---

## EPIC-002: Workflow Engine

**Описание**: Управление жизненным циклом workflow, машина состояний **Срок**:
Недели 2-4 **Ответственный**: Core Team **DoD**: Раздел 5.2.5 ТЗ **Прогресс**:
3/13 задач (23%)

### Задачи

| ID         | Задача                                        | Тип   | SP  | Приоритет | Статус  | Зависимости         |
| ---------- | --------------------------------------------- | ----- | --- | --------- | ------- | ------------------- |
| **WF-001** | Проектирование машины состояний (7 состояний) | Story | 5   | 🔴 High   | ✅ Done | —                   |
| **WF-002** | Реализация State Machine (transitions)        | Story | 8   | 🔴 High   | ✅ Done | WF-001              |
| **WF-003** | Запуск workflow из AFLConfig                  | Story | 5   | 🔴 High   | 🔴 Todo | WF-002, PARSER-009  |
| **WF-004** | Приостановка/возобновление workflow           | Story | 5   | 🔴 High   | 🔴 Todo | WF-002              |
| **WF-005** | Сериализация состояния в БД                   | Story | 5   | 🔴 High   | 🔴 Todo | WF-002, STORAGE-001 |
| **WF-006** | Параллельное выполнение независимых шагов     | Story | 8   | 🟡 Medium | 🔴 Todo | WF-002              |
| **WF-007** | Синхронизация через барьеры (wait for all)    | Story | 5   | 🟡 Medium | 🔴 Todo | WF-006              |
| **WF-008** | Retry логика с exponential backoff            | Story | 5   | 🔴 High   | 🔴 Todo | WF-002              |
| **WF-009** | Обработка ошибок шагов (continue/skip/fail)   | Story | 5   | 🔴 High   | 🔴 Todo | WF-008              |
| **WF-010** | Восстановление после сбоя (recovery)          | Story | 8   | 🔴 High   | 🔴 Todo | WF-005              |
| **WF-011** | Юнит-тесты машины состояний                   | Test  | 8   | 🔴 High   | ✅ Done | WF-002-010          |
| **WF-012** | Интеграционные тесты workflow                 | Test  | 8   | 🔴 High   | 🔴 Todo | WF-011              |
| **WF-013** | Chaos-тесты (сбои БД/сети)                    | Test  | 5   | 🟡 Medium | 🔴 Todo | WF-012              |

---

## EPIC-003: Budget Tracker

**Описание**: Учёт токенов, лимиты, уведомления **Срок**: Недели 2-3
**Ответственный**: Core Team **DoD**: Раздел 5.5.5 ТЗ **Прогресс**: 0/12 задач
(0%)

### Задачи

| ID             | Задача                                             | Тип   | SP  | Приоритет | Статус  | Зависимости    |
| -------------- | -------------------------------------------------- | ----- | --- | --------- | ------- | -------------- |
| **BUDGET-001** | Модель данных CostRecord                           | Task  | 3   | 🔴 High   | 🔴 Todo | —              |
| **BUDGET-002** | Учёт токенов по провайдерам/моделям                | Story | 5   | 🔴 High   | 🔴 Todo | BUDGET-001     |
| **BUDGET-003** | Иерархические лимиты (project/workflow/step/agent) | Story | 8   | 🔴 High   | 🔴 Todo | BUDGET-002     |
| **BUDGET-004** | Soft limits (предупреждение при 80%)               | Story | 3   | 🔴 High   | 🔴 Todo | BUDGET-003     |
| **BUDGET-005** | Hard limits (блокировка при превышении)            | Story | 5   | 🔴 High   | 🔴 Todo | BUDGET-003     |
| **BUDGET-006** | Email уведомления о лимитах                        | Story | 5   | 🟡 Medium | 🔴 Todo | BUDGET-004     |
| **BUDGET-007** | Slack уведомления                                  | Story | 3   | 🟢 Low    | 🔴 Todo | BUDGET-004     |
| **BUDGET-008** | Webhook уведомления                                | Story | 5   | 🟡 Medium | 🔴 Todo | BUDGET-004     |
| **BUDGET-009** | Прогнозирование расхода (на основе истории)        | Story | 8   | 🟡 Medium | 🔴 Todo | BUDGET-002     |
| **BUDGET-010** | Grafana дашборд затрат                             | Task  | 5   | 🟡 Medium | 🔴 Todo | BUDGET-002     |
| **BUDGET-011** | Юнит-тесты (покрытие ≥85%)                         | Test  | 5   | 🔴 High   | 🔴 Todo | BUDGET-002-009 |
| **BUDGET-012** | Интеграционные тесты с OpenAI API                  | Test  | 5   | 🔴 High   | 🔴 Todo | BUDGET-011     |

---

## EPIC-004: Agent Executor

**Описание**: Выполнение агентов, управление инструментами **Срок**: Недели 1-3
**Ответственный**: AI Team **DoD**: Раздел 5.6.5 ТЗ **Прогресс**: 0/15 задач
(0%)

### Задачи

| ID            | Задача                                       | Тип   | SP  | Приоритет | Статус  | Зависимости            |
| ------------- | -------------------------------------------- | ----- | --- | --------- | ------- | ---------------------- |
| **AGENT-001** | IAgent интерфейс (Protocol)                  | Task  | 3   | 🔴 High   | 🔴 Todo | —                      |
| **AGENT-002** | ITool интерфейс                              | Task  | 3   | 🔴 High   | 🔴 Todo | AGENT-001              |
| **AGENT-003** | Реестр инструментов (decorator-based)        | Story | 5   | 🔴 High   | 🔴 Todo | AGENT-002              |
| **AGENT-004** | Базовый LLM-агент (LLM-based)                | Story | 8   | 🔴 High   | 🔴 Todo | AGENT-001, LLM-001     |
| **AGENT-005** | Таймауты выполнения агента                   | Story | 3   | 🔴 High   | 🔴 Todo | AGENT-004              |
| **AGENT-006** | Circuit breaker для нестабильных провайдеров | Story | 5   | 🔴 High   | 🔴 Todo | AGENT-004              |
| **AGENT-007** | Fallback стратегии (другая модель)           | Story | 5   | 🔴 High   | 🔴 Todo | AGENT-006              |
| **AGENT-008** | Логирование промптов/ответов                 | Task  | 3   | 🔴 High   | 🔴 Todo | AGENT-004              |
| **AGENT-009** | Логирование tool calls                       | Task  | 3   | 🔴 High   | 🔴 Todo | AGENT-003              |
| **AGENT-010** | Инструмент: HTTP Request                     | Story | 5   | 🟡 Medium | 🔴 Todo | AGENT-003              |
| **AGENT-011** | Инструмент: File Read/Write                  | Story | 3   | 🟡 Medium | 🔴 Todo | AGENT-003              |
| **AGENT-012** | Инструмент: Shell Command (sandboxed)        | Story | 8   | 🟡 Medium | 🔴 Todo | AGENT-003, SANDBOX-001 |
| **AGENT-013** | Инструмент: Database Query                   | Story | 5   | 🟢 Low    | 🔴 Todo | AGENT-003              |
| **AGENT-014** | Юнит-тесты агентов (покрытие ≥85%)           | Test  | 8   | 🔴 High   | 🔴 Todo | AGENT-004-013          |
| **AGENT-015** | Бенчмарки времени запуска                    | Test  | 3   | 🟡 Medium | 🔴 Todo | AGENT-014              |

---

## EPIC-005: Context Manager ⬆️ Перенесён из Alpha в MVP

**Описание**: Управление контекстом, сжатие, долгосрочная память **Срок**:
Недели 3-5 **Ответственный**: AI Team **DoD**: Раздел 5.3.5 ТЗ **Прогресс**:
0/16 задач (0%)

> **PoC 2 подтвердил**: Hybrid стратегия обеспечивает 0% потерь при достаточном
> лимите, Summarization — 2.4% потерь.

### Задачи

| ID          | Задача                                     | Тип   | SP  | Приоритет | Статус  | Зависимости      |
| ----------- | ------------------------------------------ | ----- | --- | --------- | ------- | ---------------- |
| **CTX-001** | Модель данных ConversationTurn             | Task  | 3   | 🔴 High   | 🔴 Todo | —                |
| **CTX-002** | Механизм передачи контекста между агентами | Story | 5   | 🔴 High   | 🔴 Todo | CTX-001          |
| **CTX-003** | Лимиты токенов на контекст                 | Story | 3   | 🔴 High   | 🔴 Todo | CTX-002          |
| **CTX-004** | Стратегия: Sliding Window                  | Story | 5   | 🔴 High   | 🔴 Todo | CTX-003          |
| **CTX-005** | Стратегия: LLM Summarization               | Story | 13  | 🔴 High   | 🔴 Todo | CTX-003, LLM-001 |
| **CTX-006** | Стратегия: Key Information Extraction      | Story | 8   | 🟡 Medium | 🔴 Todo | CTX-003          |
| **CTX-007** | Hybrid стратегия (комбинация)              | Story | 8   | 🔴 High   | 🔴 Todo | CTX-004-006      |
| **CTX-008** | Динамическое сжатие при 80% лимита         | Story | 5   | 🔴 High   | 🔴 Todo | CTX-003, CTX-007 |
| **CTX-009** | Фильтрация конфиденциальной информации     | Story | 5   | 🔴 High   | 🔴 Todo | CTX-002          |
| **CTX-010** | Аннотация источника контекста              | Task  | 3   | 🟡 Medium | 🔴 Todo | CTX-002          |
| **CTX-011** | Интеграция ChromaDB (векторная память)     | Story | 8   | 🟡 Medium | 🔴 Todo | CTX-001          |
| **CTX-012** | Семантический поиск в памяти               | Story | 8   | 🟡 Medium | 🔴 Todo | CTX-011          |
| **CTX-013** | Индексирование ключевых решений            | Story | 5   | 🟢 Low    | 🔴 Todo | CTX-011          |
| **CTX-014** | Валидация качества сжатия (BLEU/ROUGE)     | Test  | 8   | 🔴 High   | 🔴 Todo | CTX-005-007      |
| **CTX-015** | Бенчмарки производительности               | Test  | 5   | 🔴 High   | 🔴 Todo | CTX-014          |
| **CTX-016** | Security-тесты фильтрации секретов         | Test  | 5   | 🔴 High   | 🔴 Todo | CTX-009          |

---

## EPIC-006: Guardrail Engine ⬆️ Перенесён из Alpha в MVP

**Описание**: Проверка безопасности и качества выводов **Срок**: Недели 4-6
**Ответственный**: Security Team **DoD**: Раздел 5.4.7 ТЗ **Прогресс**: 0/18
задач (0%)

> **PoC 3 подтвердил**: Комбинированная цепочка — FP 0.00%, FN 0.00%. Все цели
> достигнуты.

### Задачи

| ID         | Задача                                            | Тип   | SP  | Приоритет | Статус  | Зависимости        |
| ---------- | ------------------------------------------------- | ----- | --- | --------- | ------- | ------------------ |
| **GR-001** | BaseGuardrail абстрактный класс                   | Task  | 3   | 🔴 High   | 🔴 Todo | —                  |
| **GR-002** | GuardrailAction enum (block/modify/flag/rollback) | Task  | 2   | 🔴 High   | 🔴 Todo | GR-001             |
| **GR-003** | Guardrail Registry                                | Story | 5   | 🔴 High   | 🔴 Todo | GR-001             |
| **GR-004** | Validator Pipeline (Chain of Responsibility)      | Story | 8   | 🔴 High   | 🔴 Todo | GR-003             |
| **GR-005** | Result Aggregator                                 | Story | 5   | 🔴 High   | 🔴 Todo | GR-004             |
| **GR-006** | Action Executor                                   | Story | 5   | 🔴 High   | 🔴 Todo | GR-004             |
| **GR-007** | Гардрейл: File Extension Check                    | Story | 5   | 🔴 High   | 🔴 Todo | GR-001             |
| **GR-008** | Гардрейл: Token Limit Check                       | Story | 5   | 🔴 High   | 🔴 Todo | GR-001, BUDGET-002 |
| **GR-009** | Гардрейл: Regex Pattern Check                     | Story | 3   | 🔴 High   | 🔴 Todo | GR-001             |
| **GR-010** | Гардрейл: LLM-as-a-Judge                          | Story | 13  | 🔴 High   | 🔴 Todo | GR-001, LLM-001    |
| **GR-011** | Гардрейл: Python Function (custom)                | Story | 5   | 🟡 Medium | 🔴 Todo | GR-001             |
| **GR-012** | Обработка нарушений (violation handler)           | Story | 5   | 🔴 High   | 🔴 Todo | GR-006             |
| **GR-013** | Кэширование результатов проверок                  | Story | 5   | 🟡 Medium | 🔴 Todo | GR-004             |
| **GR-014** | Датасет для валидации (1000 примеров)             | Task  | 8   | 🔴 High   | 🔴 Todo | —                  |
| **GR-015** | Валидация FP rate <5%                             | Test  | 5   | 🔴 High   | 🔴 Todo | GR-014             |
| **GR-016** | Валидация FN rate <1%                             | Test  | 5   | 🔴 High   | 🔴 Todo | GR-014             |
| **GR-017** | Бенчмарки производительности (<100 мс)            | Test  | 5   | 🔴 High   | 🔴 Todo | GR-007-013         |
| **GR-018** | Юнит-тесты (покрытие ≥90%)                        | Test  | 8   | 🔴 High   | 🔴 Todo | GR-007-013         |

---

## EPIC-007: Storage Layer

**Описание**: База данных, кэш, хранилище артефактов **Срок**: Недели 1-2
**Ответственный**: Core Team **Прогресс**: 2/16 задач (13%)

### Задачи

| ID              | Задача                            | Тип   | SP  | Приоритет | Статус  | Зависимости     |
| --------------- | --------------------------------- | ----- | --- | --------- | ------- | --------------- |
| **STORAGE-001** | Настройка PostgreSQL + SQLAlchemy | Task  | 5   | 🔴 High   | ✅ Done | —               |
| **STORAGE-002** | Миграции БД (Alembic)             | Task  | 5   | 🔴 High   | ✅ Done | STORAGE-001     |
| **STORAGE-003** | Модель: Project                   | Task  | 2   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-004** | Модель: Workflow                  | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-005** | Модель: WorkflowExecution         | Task  | 5   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-006** | Модель: AgentExecution            | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-007** | Модель: TaskExecution             | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-008** | Модель: ArtifactVersion           | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-009** | Модель: GuardrailCheck            | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-010** | Модель: CostRecord                | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-011** | Модель: AuditLog                  | Task  | 3   | 🔴 High   | 🔴 Todo | STORAGE-002     |
| **STORAGE-012** | Индексы для производительности    | Task  | 5   | 🔴 High   | 🔴 Todo | STORAGE-003-011 |
| **STORAGE-013** | Настройка Redis (кэш)             | Task  | 5   | 🔴 High   | 🔴 Todo | —               |
| **STORAGE-014** | Настройка MinIO/S3 (артефакты)    | Task  | 5   | 🔴 High   | 🔴 Todo | —               |
| **STORAGE-015** | Repository Pattern (абстракция)   | Story | 5   | 🔴 High   | 🔴 Todo | STORAGE-003-011 |
| **STORAGE-016** | Юнит-тесты репозиториев           | Test  | 8   | 🔴 High   | 🔴 Todo | STORAGE-015     |

---

## EPIC-008: REST API

**Описание**: Внешнее API для интеграции **Срок**: Недели 2-3 **Ответственный**:
Core Team **Прогресс**: 1/14 задач (7%)

### Задачи

| ID          | Задача                                         | Тип   | SP  | Приоритет | Статус  | Зависимости     |
| ----------- | ---------------------------------------------- | ----- | --- | --------- | ------- | --------------- |
| **API-001** | Настройка FastAPI проекта                      | Task  | 3   | 🔴 High   | ✅ Done | —               |
| **API-002** | Модель: WorkflowCreateRequest                  | Task  | 2   | 🔴 High   | 🔴 Todo | API-001         |
| **API-003** | Модель: WorkflowStatusResponse                 | Task  | 2   | 🔴 High   | 🔴 Todo | API-001         |
| **API-004** | Endpoint: POST /api/v1/workflows               | Story | 5   | 🔴 High   | 🔴 Todo | API-002, WF-003 |
| **API-005** | Endpoint: GET /api/v1/workflows/{id}           | Story | 3   | 🔴 High   | 🔴 Todo | API-003, WF-003 |
| **API-006** | Endpoint: POST /api/v1/workflows/{id}/pause    | Story | 3   | 🔴 High   | 🔴 Todo | WF-004          |
| **API-007** | Endpoint: POST /api/v1/workflows/{id}/resume   | Story | 3   | 🔴 High   | 🔴 Todo | WF-004          |
| **API-008** | Endpoint: GET /api/v1/workflows/{id}/artifacts | Story | 5   | 🟡 Medium | 🔴 Todo | STORAGE-008     |
| **API-009** | Endpoint: GET /api/v1/metrics/budget           | Story | 5   | 🟡 Medium | 🔴 Todo | BUDGET-002      |
| **API-010** | WebSocket для real-time уведомлений            | Story | 8   | 🟡 Medium | 🔴 Todo | API-005         |
| **API-011** | Аутентификация API (API keys)                  | Story | 5   | 🔴 High   | 🔴 Todo | API-001         |
| **API-012** | Rate limiting                                  | Story | 5   | 🟡 Medium | 🔴 Todo | API-011         |
| **API-013** | OpenAPI документация (/docs)                   | Task  | 2   | 🟢 Low    | 🔴 Todo | API-004-010     |
| **API-014** | Интеграционные тесты API                       | Test  | 8   | 🔴 High   | 🔴 Todo | API-004-012     |

---

## EPIC-009: LLM Integrations

**Описание**: Интеграция с LLM-провайдерами **Срок**: Недели 1-2
**Ответственный**: AI Team **Прогресс**: 0/13 задач (0%)

### Задачи

| ID          | Задача                             | Тип   | SP  | Приоритет | Статус  | Зависимости      |
| ----------- | ---------------------------------- | ----- | --- | --------- | ------- | ---------------- |
| **LLM-001** | Настройка litellm абстракции       | Task  | 5   | 🔴 High   | 🔴 Todo | —                |
| **LLM-002** | Интеграция OpenAI (GPT-4, GPT-3.5) | Story | 8   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-003** | Интеграция Anthropic (Claude 3)    | Story | 8   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-004** | Fallback стратегии (модели)        | Story | 5   | 🔴 High   | 🔴 Todo | LLM-002, LLM-003 |
| **LLM-005** | Circuit breaker для LLM            | Story | 5   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-006** | Обработка timeout ошибок           | Story | 3   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-007** | Обработка rate limit ошибок        | Story | 5   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-008** | Обработка auth ошибок              | Story | 3   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-009** | Подсчёт токенов (tiktoken)         | Task  | 3   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-010** | Кэширование ответов (diskcache)    | Story | 5   | 🟡 Medium | 🔴 Todo | LLM-001          |
| **LLM-011** | Retry логика (exponential backoff) | Story | 5   | 🔴 High   | 🔴 Todo | LLM-001          |
| **LLM-012** | Юнит-тесты с моками                | Test  | 8   | 🔴 High   | 🔴 Todo | LLM-002-011      |
| **LLM-013** | Интеграционные тесты (sandbox)     | Test  | 8   | 🔴 High   | 🔴 Todo | LLM-012          |

---

## EPIC-010: Git Integration

**Описание**: Интеграция с системами контроля версий **Срок**: Недели 4-5
(Alpha) **Ответственный**: Core Team **Прогресс**: 0/13 задач (0%)

### Задачи

| ID          | Задача                           | Тип   | SP  | Приоритет | Статус  | Зависимости      |
| ----------- | -------------------------------- | ----- | --- | --------- | ------- | ---------------- |
| **GIT-001** | Настройка gitpython              | Task  | 2   | 🔴 High   | 🔴 Todo | —                |
| **GIT-002** | GitIntegrationManager класс      | Task  | 5   | 🔴 High   | 🔴 Todo | GIT-001          |
| **GIT-003** | Метод: clone_repository          | Story | 8   | 🔴 High   | 🔴 Todo | GIT-002          |
| **GIT-004** | Метод: get_file_content          | Story | 5   | 🔴 High   | 🔴 Todo | GIT-002          |
| **GIT-005** | Метод: get_diff                  | Story | 5   | 🟡 Medium | 🔴 Todo | GIT-002          |
| **GIT-006** | Метод: commit_and_push           | Story | 8   | 🟡 Medium | 🔴 Todo | GIT-002          |
| **GIT-007** | SSH аутентификация               | Story | 5   | 🔴 High   | 🔴 Todo | GIT-002          |
| **GIT-008** | HTTPS аутентификация (tokens)    | Story | 5   | 🔴 High   | 🔴 Todo | GIT-002          |
| **GIT-009** | Обработка ошибок аутентификации  | Story | 3   | 🔴 High   | 🔴 Todo | GIT-007, GIT-008 |
| **GIT-010** | Retry логика для Git операций    | Story | 5   | 🔴 High   | 🔴 Todo | GIT-002          |
| **GIT-011** | Очистка временных директорий     | Task  | 3   | 🟡 Medium | 🔴 Todo | GIT-003          |
| **GIT-012** | Юнит-тесты с моками              | Test  | 8   | 🔴 High   | 🔴 Todo | GIT-003-010      |
| **GIT-013** | Интеграционные тесты (test repo) | Test  | 8   | 🔴 High   | 🔴 Todo | GIT-012          |

---

## EPIC-011: Issue Tracker Integration

**Описание**: Интеграция с Jira, GitHub Issues **Срок**: Недели 5-6 (Alpha)
**Ответственный**: Core Team **Прогресс**: 0/14 задач (0%)

### Задачи

| ID              | Задача                            | Тип   | SP  | Приоритет | Статус  | Зависимости              |
| --------------- | --------------------------------- | ----- | --- | --------- | ------- | ------------------------ |
| **TRACKER-001** | BaseIssueTracker абстракция       | Task  | 3   | 🔴 High   | 🔴 Todo | —                        |
| **TRACKER-002** | Модель: Issue                     | Task  | 3   | 🔴 High   | 🔴 Todo | TRACKER-001              |
| **TRACKER-003** | IssueTrackerFactory               | Task  | 3   | 🔴 High   | 🔴 Todo | TRACKER-001              |
| **TRACKER-004** | JiraTracker: подключение          | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-001              |
| **TRACKER-005** | JiraTracker: create_issue         | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-004              |
| **TRACKER-006** | JiraTracker: add_comment          | Story | 3   | 🔴 High   | 🔴 Todo | TRACKER-004              |
| **TRACKER-007** | JiraTracker: search_issues        | Story | 5   | 🟡 Medium | 🔴 Todo | TRACKER-004              |
| **TRACKER-008** | GitHubIssuesTracker: подключение  | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-001              |
| **TRACKER-009** | GitHubIssuesTracker: create_issue | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-008              |
| **TRACKER-010** | GitHubIssuesTracker: add_comment  | Story | 3   | 🔴 High   | 🔴 Todo | TRACKER-008              |
| **TRACKER-011** | Обработка rate limit              | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-004, TRACKER-008 |
| **TRACKER-012** | Retry логика                      | Story | 5   | 🔴 High   | 🔴 Todo | TRACKER-001              |
| **TRACKER-013** | Юнит-тесты с моками               | Test  | 8   | 🔴 High   | 🔴 Todo | TRACKER-004-012          |
| **TRACKER-014** | Интеграционные тесты (sandbox)    | Test  | 8   | 🔴 High   | 🔴 Todo | TRACKER-013              |

---

## EPIC-012: Security & Sandbox ⬆️ Перенесён из Alpha в MVP

**Описание**: Изоляция выполнения, безопасность **Срок**: Недели 4-5
**Ответственный**: Security Team **Прогресс**: 0/14 задач (0%)

> **PoC 6 подтвердил**: 6/6 escape attempts blocked, 0 false positives.

### Задачи

| ID              | Задача                                   | Тип   | SP  | Приоритет | Статус  | Зависимости     |
| --------------- | ---------------------------------------- | ----- | --- | --------- | ------- | --------------- |
| **SANDBOX-001** | Docker sandbox базовая конфигурация      | Story | 8   | 🔴 High   | 🔴 Todo | —               |
| **SANDBOX-002** | Изоляция файловой системы                | Story | 5   | 🔴 High   | 🔴 Todo | SANDBOX-001     |
| **SANDBOX-003** | Изоляция сети                            | Story | 5   | 🔴 High   | 🔴 Todo | SANDBOX-001     |
| **SANDBOX-004** | Лимиты ресурсов (CPU, RAM)               | Story | 5   | 🔴 High   | 🔴 Todo | SANDBOX-001     |
| **SANDBOX-005** | Таймаут выполнения контейнера            | Story | 3   | 🔴 High   | 🔴 Todo | SANDBOX-001     |
| **SANDBOX-006** | Шифрование секретов в БД                 | Story | 5   | 🔴 High   | 🔴 Todo | STORAGE-001     |
| **SANDBOX-007** | Интеграция HashiCorp Vault (опционально) | Story | 8   | 🟡 Medium | 🔴 Todo | SANDBOX-006     |
| **SANDBOX-008** | Ротация API ключей                       | Story | 5   | 🟡 Medium | 🔴 Todo | SANDBOX-006     |
| **SANDBOX-009** | Тесты на escape-попытки                  | Test  | 13  | 🔴 High   | 🔴 Todo | SANDBOX-001-005 |
| **SANDBOX-010** | Security audit кода                      | Task  | 8   | 🔴 High   | 🔴 Todo | SANDBOX-006-008 |
| **SANDBOX-011** | OWASP ZAP сканирование                   | Test  | 5   | 🔴 High   | ✅ Done | API-014         |
| **SEC-012**     | Branch protection rules (GitHub)         | Task  | 3   | 🔴 High   | 🔴 Todo | —               |
| **SEC-013**     | DAST сканирование (OWASP ZAP в CI)       | Task  | 5   | 🟡 Medium | ✅ Done | SANDBOX-011     |
| **SEC-014**     | Secrets rotation policy                  | Task  | 5   | 🟡 Medium | 🔴 Todo | SANDBOX-008     |

---

## EPIC-013: Monitoring & Observability ⬆️ Перенесён из Beta в MVP

**Описание**: Логирование, метрики, алертинг, трейсинг **Срок**: Недели 3-6
**Ответственный**: Platform Team **Прогресс**: 0/22 задач (0%)

> **Аудит выявил**: 5/7 компонентов observability не настроены. Критично для
> production.

### Задачи

| ID          | Задача                                     | Тип   | SP  | Приоритет | Статус  | Зависимости         |
| ----------- | ------------------------------------------ | ----- | --- | --------- | ------- | ------------------- |
| **MON-001** | Структурированное логирование (JSON)       | Task  | 5   | 🔴 High   | ✅ Done | —                   |
| **MON-002** | Уровни логирования (DEBUG/INFO/WARN/ERROR) | Task  | 3   | 🔴 High   | ✅ Done | MON-001             |
| **MON-003** | Интеграция Prometheus                      | Story | 8   | 🔴 High   | ✅ Done | MON-001             |
| **MON-004** | Метрика: workflow_execution_time           | Task  | 3   | 🔴 High   | ✅ Done | MON-003             |
| **MON-005** | Метрика: agent_execution_success_rate      | Task  | 3   | 🔴 High   | ✅ Done | MON-003             |
| **MON-006** | Метрика: token_usage_per_minute            | Task  | 3   | 🔴 High   | ✅ Done | MON-003, BUDGET-002 |
| **MON-007** | Метрика: guardrail_violations_total        | Task  | 3   | 🔴 High   | ✅ Done | MON-003, GR-012     |
| **MON-008** | Метрика: integration_request_duration      | Task  | 3   | 🔴 High   | ✅ Done | MON-003             |
| **MON-009** | Метрика: queue_length                      | Task  | 3   | 🔴 High   | ✅ Done | MON-003             |
| **MON-010** | Метрика: error_rate                        | Task  | 3   | 🔴 High   | ✅ Done | MON-003             |
| **MON-011** | Настройка Grafana                          | Task  | 5   | 🔴 High   | ✅ Done | MON-003             |
| **MON-012** | Дашборд: Обзор системы                     | Task  | 5   | 🔴 High   | ✅ Done | MON-011             |
| **MON-013** | Дашборд: Бюджет и затраты                  | Task  | 5   | 🟡 Medium | 🔴 Todo | MON-011             |
| **MON-014** | Дашборд: Производительность агентов        | Task  | 5   | 🟡 Medium | 🔴 Todo | MON-011             |
| **MON-015** | OpenTelemetry инициализация                | Story | 8   | 🟡 Medium | 🔴 Todo | MON-001             |
| **MON-016** | Distributed tracing для workflow           | Story | 8   | 🟡 Medium | 🔴 Todo | MON-015             |
| **MON-017** | Алерт: Бюджет превышен на 90%              | Story | 3   | 🔴 High   | ✅ Done | MON-011, BUDGET-004 |
| **MON-018** | Алерт: Error rate >5%                      | Story | 3   | 🔴 High   | ✅ Done | MON-011             |
| **MON-019** | Алерт: SLA breach                          | Story | 3   | 🔴 High   | ✅ Done | MON-011             |
| **MON-020** | Алерт: Workflow failed                     | Story | 3   | 🔴 High   | ✅ Done | MON-011             |
| **MON-021** | Интеграция Slack для алертов               | Story | 5   | 🔴 High   | ✅ Done | MON-017-020         |
| **MON-022** | Интеграция ELK Stack (опционально)         | Story | 8   | 🟢 Low    | 🔴 Todo | MON-001             |

---

## EPIC-014: Deployment & CI/CD

**Описание**: Развёртывание, контейнеризация, пайплайны **Срок**: Недели 2-3
**Ответственный**: Platform Team **Прогресс**: 3/16 задач (19%)

### Задачи

| ID             | Задача                                 | Тип   | SP  | Приоритет | Статус  | Зависимости            |
| -------------- | -------------------------------------- | ----- | --- | --------- | ------- | ---------------------- |
| **DEPLOY-001** | Dockerfile для оркестратора            | Task  | 5   | 🔴 High   | ✅ Done | —                      |
| **DEPLOY-002** | docker-compose.yml (локально)          | Task  | 5   | 🔴 High   | ✅ Done | DEPLOY-001             |
| **DEPLOY-003** | GitHub Actions: CI пайплайн            | Story | 8   | 🔴 High   | ✅ Done | DEPLOY-001             |
| **DEPLOY-004** | GitHub Actions: тесты                  | Task  | 5   | 🔴 High   | ✅ Done | DEPLOY-003             |
| **DEPLOY-005** | GitHub Actions: build Docker image     | Task  | 3   | 🔴 High   | ✅ Done | DEPLOY-003             |
| **DEPLOY-006** | GitHub Actions: push to registry       | Task  | 3   | 🔴 High   | ✅ Done | DEPLOY-005             |
| **DEPLOY-007** | Обновить Python до 3.12 в CI/CD        | Task  | 2   | 🔴 High   | ✅ Done | DEPLOY-003             |
| **DEPLOY-008** | Docker registry push (GHCR)            | Task  | 5   | 🔴 High   | ✅ Done | DEPLOY-005             |
| **DEPLOY-009** | Staging deploy команды                 | Story | 8   | 🔴 High   | ✅ Done | DEPLOY-002             |
| **DEPLOY-010** | Production deploy команды              | Story | 8   | 🔴 High   | ✅ Done | DEPLOY-002             |
| **DEPLOY-011** | Kubernetes manifests (опционально)     | Story | 8   | 🟡 Medium | 🔴 Todo | DEPLOY-001             |
| **DEPLOY-012** | Helm chart (опционально)               | Story | 8   | 🟡 Medium | 🔴 Todo | DEPLOY-011             |
| **DEPLOY-013** | Настройка окружений (dev/staging/prod) | Task  | 5   | 🔴 High   | 🔴 Todo | DEPLOY-002             |
| **DEPLOY-014** | Секреты в CI/CD                        | Task  | 5   | 🔴 High   | 🔴 Todo | DEPLOY-003             |
| **DEPLOY-015** | Blue-green deployment                  | Story | 8   | 🟡 Medium | 🔴 Todo | DEPLOY-010             |
| **DEPLOY-016** | Документация развёртывания             | Doc   | 5   | 🟡 Medium | 🔴 Todo | DEPLOY-002, DEPLOY-011 |

---

## EPIC-015: Proof-of-Concept

**Описание**: Валидация ключевых рисков через эксперименты **Срок**: Недели 1-2
**Ответственный**: Core Team + AI Team **Прогресс**: 8/8 задач (100%) ✅

> **Все 8 PoC прошли успешно за 16 секунд.** Архитектура валидирована.

### Задачи

| ID          | Задача                                         | Тип | SP  | Приоритет | Статус  | Результат                 |
| ----------- | ---------------------------------------------- | --- | --- | --------- | ------- | ------------------------- |
| **POC-001** | LLM Integration — fallback, circuit breaker    | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED                 |
| **POC-002** | Context Manager — 3 стратегии сжатия           | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED                 |
| **POC-003** | Guardrail Engine — FP/FN на 1000 samples       | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (FP 0%, FN 0%)  |
| **POC-004** | Budget Tracking — точность учёта               | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (100% accuracy) |
| **POC-005** | Workflow Recovery — восстановление после сбоев | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (recovery <5s)  |
| **POC-006** | Sandbox Security — escape detection            | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (6/6 blocked)   |
| **POC-007** | Database Scaling — 100K workflows              | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (p95 0.47ms)    |
| **POC-008** | Concurrent Workflows — 100 параллельных        | PoC | 5   | 🔴 High   | ✅ Done | ✅ PASSED (100% success)  |

---

## EPIC-016: Documentation

**Описание**: Техническая документация проекта **Срок**: Недели 1-4
**Ответственный**: Core Team **Прогресс**: 5/13 задач (38%)

### Задачи

| ID          | Задача                     | Тип | SP  | Приоритет | Статус  | Файл                         |
| ----------- | -------------------------- | --- | --- | --------- | ------- | ---------------------------- |
| **DOC-001** | Техническое Задание        | Doc | 8   | 🔴 High   | ✅ Done | `AFL_Orchestrator_TZ_ADD.md` |
| **DOC-002** | Архитектура системы        | Doc | 8   | 🔴 High   | ✅ Done | `ARCHITECTURE_DESIGN.md`     |
| **DOC-003** | API Спецификация (часть 1) | Doc | 5   | 🔴 High   | ✅ Done | `API_SPECIFICATION_P1.md`    |
| **DOC-004** | API Спецификация (часть 2) | Doc | 5   | 🔴 High   | ✅ Done | `API_SPECIFICATION_P2.md`    |
| **DOC-005** | Схема БД (части 1-3)       | Doc | 8   | 🔴 High   | ✅ Done | `DATABASE_SCHEMA_P1-3.md`    |
| **DOC-006** | Git Flow документация      | Doc | 3   | 🟡 Medium | ✅ Done | `GIT_FLOW.md`                |
| **DOC-007** | Настройка репозитория      | Doc | 3   | 🟡 Medium | ✅ Done | `REPO_SETUP.md`              |
| **DOC-008** | PoC Результаты             | Doc | 5   | 🔴 High   | ✅ Done | `POC_RESULTS.md`             |
| **DOC-009** | README проекта             | Doc | 3   | 🟡 Medium | ✅ Done | `README.md`                  |
| **DOC-010** | Бэклог задач               | Doc | 3   | 🟡 Medium | ✅ Done | `BACKLOG_JIRA.md`            |
| **DOC-011** | Инфраструктура аудит       | Doc | 3   | 🟡 Medium | ✅ Done | `INFRASTRUCTURE_AUDIT.md`    |
| **DOC-012** | API документация (OpenAPI) | Doc | 5   | 🟡 Medium | 🔴 Todo | `/docs` endpoint             |
| **DOC-013** | Руководство разработчика   | Doc | 5   | 🟡 Medium | 🔴 Todo | `CONTRIBUTING.md`            |

---

## EPIC-017: Repository Setup

**Описание**: Настройка репозитория, CI/CD, линтеры **Срок**: Недели 1-2
**Ответственный**: Platform Team **Прогресс**: 13/13 задач (100%) ✅

### Задачи

| ID           | Задача                             | Тип   | SP  | Приоритет | Статус  | Файл                               |
| ------------ | ---------------------------------- | ----- | --- | --------- | ------- | ---------------------------------- |
| **REPO-001** | .gitignore для Python              | Task  | 1   | 🔴 High   | ✅ Done | `.gitignore`                       |
| **REPO-002** | Pre-commit hooks конфигурация      | Task  | 3   | 🔴 High   | ✅ Done | `.pre-commit-config.yaml`          |
| **REPO-003** | pyproject.toml (ruff, black, mypy) | Task  | 3   | 🔴 High   | ✅ Done | `pyproject.toml`                   |
| **REPO-004** | SQLFluff конфигурация              | Task  | 2   | 🟡 Medium | ✅ Done | `.sqlfluff`                        |
| **REPO-005** | GitHub Issues шаблоны              | Task  | 2   | 🟡 Medium | ✅ Done | `.github/ISSUE_TEMPLATE/`          |
| **REPO-006** | PR шаблон                          | Task  | 2   | 🟡 Medium | ✅ Done | `.github/PULL_REQUEST_TEMPLATE.md` |
| **REPO-007** | GitHub Actions CI/CD               | Story | 5   | 🔴 High   | ✅ Done | `.github/workflows/ci-cd.yml`      |
| **REPO-008** | Скрипт настройки окружения         | Task  | 3   | 🔴 High   | ✅ Done | `scripts/setup-git.sh`             |
| **REPO-009** | requirements.txt                   | Task  | 2   | 🔴 High   | ✅ Done | `requirements.txt`                 |
| **REPO-010** | requirements-dev.txt               | Task  | 2   | 🔴 High   | ✅ Done | `requirements-dev.txt`             |
| **REPO-011** | .env.example                       | Task  | 1   | 🔴 High   | ✅ Done | `.env.example`                     |
| **REPO-012** | Makefile с командами               | Task  | 3   | 🟡 Medium | ✅ Done | `Makefile`                         |
| **REPO-013** | Структура проекта                  | Task  | 3   | 🔴 High   | ✅ Done | `src/orchestrator/`                |

---

## EPIC-018: Infrastructure Hardening ⭐ Новый

**Описание**: Устранение проблем из Infrastructure Audit **Срок**: Недели 2-4
**Ответственный**: Platform Team + Security Team **Прогресс**: 0/13 задач (0%)

> **Аудит выявил 7 критических проблем**: нет Prometheus, Grafana,
> OpenTelemetry, алертинга, DAST, Vault, seed-данных.

### Задачи

| ID            | Задача                               | Тип   | SP  | Приоритет | Статус  | Зависимости |
| ------------- | ------------------------------------ | ----- | --- | --------- | ------- | ----------- |
| **INFRA-001** | Prometheus сервер (docker-compose)   | Task  | 5   | 🔴 High   | ✅ Done | DEPLOY-002  |
| **INFRA-002** | Grafana сервер (docker-compose)      | Task  | 5   | 🔴 High   | ✅ Done | INFRA-001   |
| **INFRA-003** | Seed-данные для разработки           | Task  | 3   | 🟡 Medium | ✅ Done | STORAGE-002 |
| **INFRA-004** | Seed AFL конфиги                     | Task  | 3   | 🟡 Medium | ✅ Done | INFRA-003   |
| **INFRA-005** | Makefile target: `make seed`         | Task  | 2   | 🟡 Medium | ✅ Done | INFRA-003   |
| **INFRA-006** | JSON форматтер для логов             | Task  | 5   | 🔴 High   | ✅ Done | MON-001     |
| **INFRA-007** | Health check endpoint                | Task  | 3   | 🔴 High   | ✅ Done | API-001     |
| **INFRA-008** | Readiness probe                      | Task  | 3   | 🔴 High   | ✅ Done | INFRA-007   |
| **INFRA-009** | Liveness probe                       | Task  | 3   | 🔴 High   | ✅ Done | INFRA-007   |
| **INFRA-010** | Docker healthcheck для всех сервисов | Task  | 3   | 🔴 High   | ✅ Done | DEPLOY-002  |
| **INFRA-011** | Rate limiting middleware             | Story | 5   | 🔴 High   | ✅ Done | API-012     |
| **INFRA-012** | Request ID middleware                | Task  | 3   | 🟡 Medium | ✅ Done | API-001     |
| **INFRA-013** | CORS настройка                       | Task  | 3   | 🔴 High   | ✅ Done | API-001     |

---

## Сводка по спринтам (обновлённая v4.0)

### Спринт 1 (Недели 1-2): MVP Foundation 🟡 В работе

| Эпик             | Задач | Выполнено | Осталось SP |
| ---------------- | ----- | --------- | ----------- |
| EPIC-001 Parser  | 10    | 10        | 0 ✅        |
| EPIC-007 Storage | 16    | 2         | ~55         |
| EPIC-009 LLM     | 13    | 0         | ~65         |
| EPIC-014 Deploy  | 16    | 8         | ~30         |
| EPIC-015 PoC     | 8     | 8         | 0 ✅        |
| EPIC-016 Docs    | 13    | 6         | ~15         |
| EPIC-017 Repo    | 13    | 13        | 0 ✅        |
| EPIC-018 Infra   | 13    | 13        | 0 ✅        |

**Всего SP**: ~267 → **Выполнено**: ~204 SP (76%) → **Осталось**: ~181 SP

### Спринт 2 (Недели 2-3): Core Engine 🔴 Не начат

| Эпик                | Задач | Выполнено | Осталось SP |
| ------------------- | ----- | --------- | ----------- |
| EPIC-002 Workflow   | 13    | 3         | ~60         |
| EPIC-003 Budget     | 12    | 0         | ~55         |
| EPIC-008 REST API   | 14    | 1         | ~50         |
| EPIC-013 Monitoring | 22    | 8         | ~40         |

**Всего SP**: ~205 → **Выполнено**: ~40 SP (20%)

### Спринт 3 (Недели 3-4): Agent Execution 🔴 Не начат

| Эпик               | Задач | Выполнено | Осталось SP |
| ------------------ | ----- | --------- | ----------- |
| EPIC-004 Agent     | 15    | 0         | ~75         |
| EPIC-006 Guardrail | 18    | 0         | ~95         |

**Всего SP**: ~170

### Спринт 4 (Недели 4-5): MVP Security & Context 🔴 Не начат

| Эпик                | Задач | Выполнено | Осталось SP |
| ------------------- | ----- | --------- | ----------- |
| EPIC-005 Context    | 16    | 0         | ~90         |
| EPIC-012 Sandbox    | 14    | 0         | ~75         |
| EPIC-013 Monitoring | 22    | 0         | ~95         |

**Всего SP**: ~260

### Спринт 5 (Недели 5-6): Alpha Integrations 🔴 Не начат

| Эпик             | Задач | Выполнено | Осталось SP |
| ---------------- | ----- | --------- | ----------- |
| EPIC-010 Git     | 13    | 0         | ~65         |
| EPIC-011 Tracker | 14    | 0         | ~65         |

**Всего SP**: ~130

### Спринт 6-7 (Недели 7-10): Beta & Stabilization 🔴 Не начат

| Эпик                     | Задач | Выполнено | Осталось SP |
| ------------------------ | ----- | --------- | ----------- |
| Стабилизация             | —     | 0         | ~15         |
| Нагрузочное тестирование | —     | 0         | ~15         |

**Всего SP**: ~30

---

## Изменения v3.0 → v4.0

| Изменение             | Описание                                                                                | Статус          |
| --------------------- | --------------------------------------------------------------------------------------- | --------------- |
| **EPIC-018 завершён** | 13/13 задач ✅                                                                          | ✅ Завершён     |
| **EPIC-017 завершён** | 13/13 задач ✅                                                                          | ✅ Завершён     |
| **EPIC-015 завершён** | 8/8 задач ✅                                                                            | ✅ Завершён     |
| **EPIC-013 в работе** | 8/22 задач — JSON логи, Prometheus, Grafana, алерты                                     | 🟡 В работе     |
| **EPIC-014 в работе** | 8/16 задач — Python 3.12, GHCR, staging/prod deploy, OWASP ZAP                          | 🟡 В работе     |
| **EPIC-012 в работе** | 1/14 задач — DAST сканирование                                                          | 🟡 В работе     |
| **EPIC-016 в работе** | 6/13 задач — PoC результаты, аудит                                                      | 🟡 В работе     |
| **EPIC-001 завершён** | 10/10 задач ✅ — YAML/JSON, anchors, валидация, циклы, line/column, миграции, тесты 98% | ✅ Завершён     |
| **EPIC-007 в работе** | 2/16 задач — PostgreSQL + Alembic готовы                                                | 🟡 В работе     |
| **EPIC-002 в работе** | 3/13 задач — State Machine готова                                                       | 🟡 В работе     |
| **EPIC-008 в работе** | 1/14 задач — FastAPI настроен                                                           | 🟡 В работе     |
| **Pre-commit fixes**  | 8 проблем исправлены — ruff, mypy, black, isort, detect-secrets                         | ✅ Завершён     |
| **Всего выполнено**   | 50/240 задач (20.8%)                                                                    | +8 задач с v3.0 |
| **Story Points**      | ~262/~1310 (20%)                                                                        | +162 SP         |

---

## Приложения

### A. Импорт в Jira

```csv
Summary,Issue Type,Priority,Story Points,Epic Link,Status,Labels
"Настройка проекта Python 3.12+ с pydantic",Task,High,3,EPIC-001,Done,parser;mvp
"Prometheus сервер (docker-compose)",Task,High,5,EPIC-018,Todo,infra;mvp
"Grafana сервер (docker-compose)",Task,High,5,EPIC-018,Todo,infra;mvp
"Seed-данные для разработки",Task,Medium,3,EPIC-018,Todo,infra;dev
...
```

### B. Импорт в Linear

```json
[
  {
    "title": "Prometheus сервер (docker-compose)",
    "type": "task",
    "priority": "high",
    "estimate": 5,
    "teamId": "platform-team",
    "labelIds": ["infra", "mvp"],
    "state": "backlog"
  },
  ...
]
```

### C. Матрица ответственности

| Команда           | Эпики                                       | Задач | Выполнено | Прогресс |
| ----------------- | ------------------------------------------- | ----- | --------- | -------- |
| **Core Team**     | EPIC-001, 002, 003, 007, 008, 010, 011, 016 | 100   | 16        | 16%      |
| **AI Team**       | EPIC-004, 005, 009                          | 44    | 0         | 0%       |
| **Security Team** | EPIC-006, 012                               | 32    | 1         | 3%       |
| **Platform Team** | EPIC-013, 014, 017, 018                     | 64    | 35        | 55%      |

---

_Документ обновлён на основе ТЗ AFL_Orchestrator_TZ_ADD.md v1.0, результатов PoC
и Infrastructure Audit (2026-04-02)_
