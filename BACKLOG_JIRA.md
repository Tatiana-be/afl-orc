# AFL Orchestrator: Бэклог задач для Jira/Linear

**Дата создания**: 2026-03-31  
**Версия**: 1.0  
**На основе ТЗ**: AFL_Orchestrator_TZ_ADD.md v1.0

---

## Структура эпиков

| Epic ID | Название | Фаза | Спринтов |
|---------|----------|------|----------|
| EPIC-001 | Parser Module | MVP | 2 |
| EPIC-002 | Workflow Engine | MVP | 3 |
| EPIC-003 | Budget Tracker | MVP | 2 |
| EPIC-004 | Agent Executor | MVP | 3 |
| EPIC-005 | Context Manager | Alpha | 3 |
| EPIC-006 | Guardrail Engine | MVP/Alpha | 3 |
| EPIC-007 | Storage Layer | MVP | 2 |
| EPIC-008 | REST API | MVP | 2 |
| EPIC-009 | LLM Integrations | MVP | 2 |
| EPIC-010 | Git Integration | Alpha | 2 |
| EPIC-011 | Issue Tracker Integration | Alpha | 2 |
| EPIC-012 | Security & Sandbox | Alpha | 2 |
| EPIC-013 | Monitoring & Observability | Beta | 2 |
| EPIC-014 | Deployment & CI/CD | MVP | 2 |

---

## EPIC-001: Parser Module

**Описание**: Парсинг и валидация AFL-конфигураций  
**Срок**: Недели 1-2  
**Ответственный**: Core Team  
**DoD**: Раздел 5.1.5 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **PARSER-001** | Настройка проекта Python 3.11+ с pydantic | Task | 3 | 🔴 High | — |
| **PARSER-002** | Реализация схемы AFLConfig (Pydantic models) | Story | 8 | 🔴 High | PARSER-001 |
| **PARSER-003** | YAML парсинг с поддержкой anchors/aliases | Story | 5 | 🔴 High | PARSER-002 |
| **PARSER-004** | JSON парсинг (альтернативный формат) | Task | 3 | 🟡 Medium | PARSER-002 |
| **PARSER-005** | Валидация ссылок (agent/artifact/guardrail) | Story | 5 | 🔴 High | PARSER-002 |
| **PARSER-006** | Проверка циклов в графе зависимостей workflow | Story | 8 | 🔴 High | PARSER-002 |
| **PARSER-007** | Детализация ошибок (строка/колонка) | Task | 5 | 🟡 Medium | PARSER-003 |
| **PARSER-008** | Версионирование схемы AFL (migration support) | Story | 5 | 🟡 Medium | PARSER-002 |
| **PARSER-009** | Юнит-тесты парсера (покрытие ≥90%) | Test | 8 | 🔴 High | PARSER-003-008 |
| **PARSER-010** | Документация API парсера | Doc | 2 | 🟢 Low | PARSER-009 |

---

## EPIC-002: Workflow Engine

**Описание**: Управление жизненным циклом workflow, машина состояний  
**Срок**: Недели 2-4  
**Ответственный**: Core Team  
**DoD**: Раздел 5.2.5 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **WF-001** | Проектирование машины состояний (7 состояний) | Story | 5 | 🔴 High | — |
| **WF-002** | Реализация State Machine (transitions) | Story | 8 | 🔴 High | WF-001 |
| **WF-003** | Запуск workflow из AFLConfig | Story | 5 | 🔴 High | WF-002, PARSER-009 |
| **WF-004** | Приостановка/возобновление workflow | Story | 5 | 🔴 High | WF-002 |
| **WF-005** | Сериализация состояния в БД | Story | 5 | 🔴 High | WF-002, STORAGE-001 |
| **WF-006** | Параллельное выполнение независимых шагов | Story | 8 | 🟡 Medium | WF-002 |
| **WF-007** | Синхронизация через барьеры (wait for all) | Story | 5 | 🟡 Medium | WF-006 |
| **WF-008** | Retry логика с exponential backoff | Story | 5 | 🔴 High | WF-002 |
| **WF-009** | Обработка ошибок шагов (continue/skip/fail) | Story | 5 | 🔴 High | WF-008 |
| **WF-010** | Восстановление после сбоя (recovery) | Story | 8 | 🔴 High | WF-005 |
| **WF-011** | Юнит-тесты машины состояний | Test | 8 | 🔴 High | WF-002-010 |
| **WF-012** | Интеграционные тесты workflow | Test | 8 | 🔴 High | WF-011 |
| **WF-013** | Chaos-тесты (сбои БД/сети) | Test | 5 | 🟡 Medium | WF-012 |

---

## EPIC-003: Budget Tracker

**Описание**: Учёт токенов, лимиты, уведомления  
**Срок**: Недели 2-3  
**Ответственный**: Core Team  
**DoD**: Раздел 5.5.5 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **BUDGET-001** | Модель данных CostRecord | Task | 3 | 🔴 High | — |
| **BUDGET-002** | Учёт токенов по провайдерам/моделям | Story | 5 | 🔴 High | BUDGET-001 |
| **BUDGET-003** | Иерархические лимиты (project/workflow/step/agent) | Story | 8 | 🔴 High | BUDGET-002 |
| **BUDGET-004** | Soft limits (предупреждение при 80%) | Story | 3 | 🔴 High | BUDGET-003 |
| **BUDGET-005** | Hard limits (блокировка при превышении) | Story | 5 | 🔴 High | BUDGET-003 |
| **BUDGET-006** | Email уведомления о лимитах | Story | 5 | 🟡 Medium | BUDGET-004 |
| **BUDGET-007** | Slack уведомления | Story | 3 | 🟢 Low | BUDGET-004 |
| **BUDGET-008** | Webhook уведомления | Story | 5 | 🟡 Medium | BUDGET-004 |
| **BUDGET-009** | Прогнозирование расхода (на основе истории) | Story | 8 | 🟡 Medium | BUDGET-002 |
| **BUDGET-010** | Grafana дашборд затрат | Task | 5 | 🟡 Medium | BUDGET-002 |
| **BUDGET-011** | Юнит-тесты (покрытие ≥85%) | Test | 5 | 🔴 High | BUDGET-002-009 |
| **BUDGET-012** | Интеграционные тесты с OpenAI API | Test | 5 | 🔴 High | BUDGET-011 |

---

## EPIC-004: Agent Executor

**Описание**: Выполнение агентов, управление инструментами  
**Срок**: Недели 1-3  
**Ответственный**: AI Team  
**DoD**: Раздел 5.6.5 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **AGENT-001** | IAgent интерфейс (Protocol) | Task | 3 | 🔴 High | — |
| **AGENT-002** | ITool интерфейс | Task | 3 | 🔴 High | AGENT-001 |
| **AGENT-003** | Реестр инструментов (decorator-based) | Story | 5 | 🔴 High | AGENT-002 |
| **AGENT-004** | Базовый LLM-агент (LLM-based) | Story | 8 | 🔴 High | AGENT-001, LLM-001 |
| **AGENT-005** | Таймауты выполнения агента | Story | 3 | 🔴 High | AGENT-004 |
| **AGENT-006** | Circuit breaker для нестабильных провайдеров | Story | 5 | 🔴 High | AGENT-004 |
| **AGENT-007** | Fallback стратегии (другая модель) | Story | 5 | 🔴 High | AGENT-006 |
| **AGENT-008** | Логирование промптов/ответов | Task | 3 | 🔴 High | AGENT-004 |
| **AGENT-009** | Логирование tool calls | Task | 3 | 🔴 High | AGENT-003 |
| **AGENT-010** | Инструмент: HTTP Request | Story | 5 | 🟡 Medium | AGENT-003 |
| **AGENT-011** | Инструмент: File Read/Write | Story | 3 | 🟡 Medium | AGENT-003 |
| **AGENT-012** | Инструмент: Shell Command (sandboxed) | Story | 8 | 🟡 Medium | AGENT-003, SANDBOX-001 |
| **AGENT-013** | Инструмент: Database Query | Story | 5 | 🟢 Low | AGENT-003 |
| **AGENT-014** | Юнит-тесты агентов (покрытие ≥85%) | Test | 8 | 🔴 High | AGENT-004-013 |
| **AGENT-015** | Бенчмарки времени запуска | Test | 3 | 🟡 Medium | AGENT-014 |

---

## EPIC-005: Context Manager

**Описание**: Управление контекстом, сжатие, долгосрочная память  
**Срок**: Недели 3-5 (Alpha)  
**Ответственный**: AI Team  
**DoD**: Раздел 5.3.5 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **CTX-001** | Модель данных ConversationTurn | Task | 3 | 🔴 High | — |
| **CTX-002** | Механизм передачи контекста между агентами | Story | 5 | 🔴 High | CTX-001 |
| **CTX-003** | Лимиты токенов на контекст | Story | 3 | 🔴 High | CTX-002 |
| **CTX-004** | Стратегия: Sliding Window | Story | 5 | 🔴 High | CTX-003 |
| **CTX-005** | Стратегия: LLM Summarization | Story | 13 | 🔴 High | CTX-003, LLM-001 |
| **CTX-006** | Стратегия: Key Information Extraction | Story | 8 | 🟡 Medium | CTX-003 |
| **CTX-007** | Hybrid стратегия (комбинация) | Story | 8 | 🟡 Medium | CTX-004-006 |
| **CTX-008** | Динамическое сжатие при 80% лимита | Story | 5 | 🔴 High | CTX-003, CTX-007 |
| **CTX-009** | Фильтрация конфиденциальной информации | Story | 5 | 🔴 High | CTX-002 |
| **CTX-010** | Аннотация источника контекста | Task | 3 | 🟡 Medium | CTX-002 |
| **CTX-011** | Интеграция ChromaDB (векторная память) | Story | 8 | 🟡 Medium | CTX-001 |
| **CTX-012** | Семантический поиск в памяти | Story | 8 | 🟡 Medium | CTX-011 |
| **CTX-013** | Индексирование ключевых решений | Story | 5 | 🟢 Low | CTX-011 |
| **CTX-014** | Валидация качества сжатия (BLEU/ROUGE) | Test | 8 | 🔴 High | CTX-005-007 |
| **CTX-015** | Бенчмарки производительности | Test | 5 | 🔴 High | CTX-014 |
| **CTX-016** | Security-тесты фильтрации секретов | Test | 5 | 🔴 High | CTX-009 |

---

## EPIC-006: Guardrail Engine

**Описание**: Проверка безопасности и качества выводов  
**Срок**: Недели 4-6 (MVP/Alpha)  
**Ответственный**: Security Team  
**DoD**: Раздел 5.4.7 ТЗ

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **GR-001** | BaseGuardrail абстрактный класс | Task | 3 | 🔴 High | — |
| **GR-002** | GuardrailAction enum (block/modify/flag/rollback) | Task | 2 | 🔴 High | GR-001 |
| **GR-003** | Guardrail Registry | Story | 5 | 🔴 High | GR-001 |
| **GR-004** | Validator Pipeline (Chain of Responsibility) | Story | 8 | 🔴 High | GR-003 |
| **GR-005** | Result Aggregator | Story | 5 | 🔴 High | GR-004 |
| **GR-006** | Action Executor | Story | 5 | 🔴 High | GR-004 |
| **GR-007** | Гардрейл: File Extension Check | Story | 5 | 🔴 High | GR-001 |
| **GR-008** | Гардрейл: Token Limit Check | Story | 5 | 🔴 High | GR-001, BUDGET-002 |
| **GR-009** | Гардрейл: Regex Pattern Check | Story | 3 | 🔴 High | GR-001 |
| **GR-010** | Гардрейл: LLM-as-a-Judge | Story | 13 | 🔴 High | GR-001, LLM-001 |
| **GR-011** | Гардрейл: Python Function (custom) | Story | 5 | 🟡 Medium | GR-001 |
| **GR-012** | Обработка нарушений (violation handler) | Story | 5 | 🔴 High | GR-006 |
| **GR-013** | Кэширование результатов проверок | Story | 5 | 🟡 Medium | GR-004 |
| **GR-014** | Датасет для валидации (1000 примеров) | Task | 8 | 🔴 High | — |
| **GR-015** | Валидация FP rate <5% | Test | 5 | 🔴 High | GR-014 |
| **GR-016** | Валидация FN rate <1% | Test | 5 | 🔴 High | GR-014 |
| **GR-017** | Бенчмарки производительности (<100 мс) | Test | 5 | 🔴 High | GR-007-013 |
| **GR-018** | Юнит-тесты (покрытие ≥90%) | Test | 8 | 🔴 High | GR-007-013 |

---

## EPIC-007: Storage Layer

**Описание**: База данных, кэш, хранилище артефактов  
**Срок**: Недели 1-2  
**Ответственный**: Core Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **STORAGE-001** | Настройка PostgreSQL + SQLAlchemy | Task | 5 | 🔴 High | — |
| **STORAGE-002** | Миграции БД (Alembic) | Task | 5 | 🔴 High | STORAGE-001 |
| **STORAGE-003** | Модель: Project | Task | 2 | 🔴 High | STORAGE-002 |
| **STORAGE-004** | Модель: Workflow | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-005** | Модель: WorkflowExecution | Task | 5 | 🔴 High | STORAGE-002 |
| **STORAGE-006** | Модель: AgentExecution | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-007** | Модель: TaskExecution | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-008** | Модель: ArtifactVersion | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-009** | Модель: GuardrailCheck | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-010** | Модель: CostRecord | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-011** | Модель: AuditLog | Task | 3 | 🔴 High | STORAGE-002 |
| **STORAGE-012** | Индексы для производительности | Task | 5 | 🔴 High | STORAGE-003-011 |
| **STORAGE-013** | Настройка Redis (кэш) | Task | 5 | 🔴 High | — |
| **STORAGE-014** | Настройка MinIO/S3 (артефакты) | Task | 5 | 🔴 High | — |
| **STORAGE-015** | Repository Pattern (абстракция) | Story | 5 | 🔴 High | STORAGE-003-011 |
| **STORAGE-016** | Юнит-тесты репозиториев | Test | 8 | 🔴 High | STORAGE-015 |

---

## EPIC-008: REST API

**Описание**: Внешнее API для интеграции  
**Срок**: Недели 2-3  
**Ответственный**: Core Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **API-001** | Настройка FastAPI проекта | Task | 3 | 🔴 High | — |
| **API-002** | Модель: WorkflowCreateRequest | Task | 2 | 🔴 High | API-001 |
| **API-003** | Модель: WorkflowStatusResponse | Task | 2 | 🔴 High | API-001 |
| **API-004** | Endpoint: POST /api/v1/workflows | Story | 5 | 🔴 High | API-002, WF-003 |
| **API-005** | Endpoint: GET /api/v1/workflows/{id} | Story | 3 | 🔴 High | API-003, WF-003 |
| **API-006** | Endpoint: POST /api/v1/workflows/{id}/pause | Story | 3 | 🔴 High | WF-004 |
| **API-007** | Endpoint: POST /api/v1/workflows/{id}/resume | Story | 3 | 🔴 High | WF-004 |
| **API-008** | Endpoint: GET /api/v1/workflows/{id}/artifacts | Story | 5 | 🟡 Medium | STORAGE-008 |
| **API-009** | Endpoint: GET /api/v1/metrics/budget | Story | 5 | 🟡 Medium | BUDGET-002 |
| **API-010** | WebSocket для real-time уведомлений | Story | 8 | 🟡 Medium | API-005 |
| **API-011** | Аутентификация API (API keys) | Story | 5 | 🔴 High | API-001 |
| **API-012** | Rate limiting | Story | 5 | 🟡 Medium | API-011 |
| **API-013** | OpenAPI документация (/docs) | Task | 2 | 🟢 Low | API-004-010 |
| **API-014** | Интеграционные тесты API | Test | 8 | 🔴 High | API-004-012 |

---

## EPIC-009: LLM Integrations

**Описание**: Интеграция с LLM-провайдерами  
**Срок**: Недели 1-2  
**Ответственный**: AI Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **LLM-001** | Настройка litellm абстракции | Task | 5 | 🔴 High | — |
| **LLM-002** | Интеграция OpenAI (GPT-4, GPT-3.5) | Story | 8 | 🔴 High | LLM-001 |
| **LLM-003** | Интеграция Anthropic (Claude 3) | Story | 8 | 🔴 High | LLM-001 |
| **LLM-004** | Fallback стратегии (модели) | Story | 5 | 🔴 High | LLM-002, LLM-003 |
| **LLM-005** | Circuit breaker для LLM | Story | 5 | 🔴 High | LLM-001 |
| **LLM-006** | Обработка timeout ошибок | Story | 3 | 🔴 High | LLM-001 |
| **LLM-007** | Обработка rate limit ошибок | Story | 5 | 🔴 High | LLM-001 |
| **LLM-008** | Обработка auth ошибок | Story | 3 | 🔴 High | LLM-001 |
| **LLM-009** | Подсчёт токенов (tiktoken) | Task | 3 | 🔴 High | LLM-001 |
| **LLM-010** | Кэширование ответов (diskcache) | Story | 5 | 🟡 Medium | LLM-001 |
| **LLM-011** |retry логика (exponential backoff) | Story | 5 | 🔴 High | LLM-001 |
| **LLM-012** | Юнит-тесты с моками | Test | 8 | 🔴 High | LLM-002-011 |
| **LLM-013** | Интеграционные тесты (sandbox) | Test | 8 | 🔴 High | LLM-012 |

---

## EPIC-010: Git Integration

**Описание**: Интеграция с системами контроля версий  
**Срок**: Недели 4-5 (Alpha)  
**Ответственный**: Core Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **GIT-001** | Настройка gitpython | Task | 2 | 🔴 High | — |
| **GIT-002** | GitIntegrationManager класс | Task | 5 | 🔴 High | GIT-001 |
| **GIT-003** | Метод: clone_repository | Story | 8 | 🔴 High | GIT-002 |
| **GIT-004** | Метод: get_file_content | Story | 5 | 🔴 High | GIT-002 |
| **GIT-005** | Метод: get_diff | Story | 5 | 🟡 Medium | GIT-002 |
| **GIT-006** | Метод: commit_and_push | Story | 8 | 🟡 Medium | GIT-002 |
| **GIT-007** | SSH аутентификация | Story | 5 | 🔴 High | GIT-002 |
| **GIT-008** | HTTPS аутентификация (tokens) | Story | 5 | 🔴 High | GIT-002 |
| **GIT-009** | Обработка ошибок аутентификации | Story | 3 | 🔴 High | GIT-007, GIT-008 |
| **GIT-010** | retry логика для Git операций | Story | 5 | 🔴 High | GIT-002 |
| **GIT-011** | Очистка временных директорий | Task | 3 | 🟡 Medium | GIT-003 |
| **GIT-012** | Юнит-тесты с моками | Test | 8 | 🔴 High | GIT-003-010 |
| **GIT-013** | Интеграционные тесты (test repo) | Test | 8 | 🔴 High | GIT-012 |

---

## EPIC-011: Issue Tracker Integration

**Описание**: Интеграция с Jira, GitHub Issues  
**Срок**: Недели 5-6 (Alpha)  
**Ответственный**: Core Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **TRACKER-001** | BaseIssueTracker абстракция | Task | 3 | 🔴 High | — |
| **TRACKER-002** | Модель: Issue | Task | 3 | 🔴 High | TRACKER-001 |
| **TRACKER-003** | IssueTrackerFactory | Task | 3 | 🔴 High | TRACKER-001 |
| **TRACKER-004** | JiraTracker: подключение | Story | 5 | 🔴 High | TRACKER-001 |
| **TRACKER-005** | JiraTracker: create_issue | Story | 5 | 🔴 High | TRACKER-004 |
| **TRACKER-006** | JiraTracker: add_comment | Story | 3 | 🔴 High | TRACKER-004 |
| **TRACKER-007** | JiraTracker: search_issues | Story | 5 | 🟡 Medium | TRACKER-004 |
| **TRACKER-008** | GitHubIssuesTracker: подключение | Story | 5 | 🔴 High | TRACKER-001 |
| **TRACKER-009** | GitHubIssuesTracker: create_issue | Story | 5 | 🔴 High | TRACKER-008 |
| **TRACKER-010** | GitHubIssuesTracker: add_comment | Story | 3 | 🔴 High | TRACKER-008 |
| **TRACKER-011** | Обработка rate limit | Story | 5 | 🔴 High | TRACKER-004, TRACKER-008 |
| **TRACKER-012** | retry логика | Story | 5 | 🔴 High | TRACKER-001 |
| **TRACKER-013** | Юнит-тесты с моками | Test | 8 | 🔴 High | TRACKER-004-012 |
| **TRACKER-014** | Интеграционные тесты (sandbox) | Test | 8 | 🔴 High | TRACKER-013 |

---

## EPIC-012: Security & Sandbox

**Описание**: Изоляция выполнения, безопасность  
**Срок**: Недели 4-5 (Alpha)  
**Ответственный**: Security Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **SANDBOX-001** | Docker sandbox базовая конфигурация | Story | 8 | 🔴 High | — |
| **SANDBOX-002** | Изоляция файловой системы | Story | 5 | 🔴 High | SANDBOX-001 |
| **SANDBOX-003** | Изоляция сети | Story | 5 | 🔴 High | SANDBOX-001 |
| **SANDBOX-004** | Лимиты ресурсов (CPU, RAM) | Story | 5 | 🔴 High | SANDBOX-001 |
| **SANDBOX-005** | Таймаут выполнения контейнера | Story | 3 | 🔴 High | SANDBOX-001 |
| **SANDBOX-006** | Шифрование секретов в БД | Story | 5 | 🔴 High | STORAGE-001 |
| **SANDBOX-007** | Интеграция HashiCorp Vault (опционально) | Story | 8 | 🟡 Medium | SANDBOX-006 |
| **SANDBOX-008** | Ротация API ключей | Story | 5 | 🟡 Medium | SANDBOX-006 |
| **SANDBOX-009** | Тесты на escape-попытки | Test | 13 | 🔴 High | SANDBOX-001-005 |
| **SANDBOX-010** | Security audit кода | Task | 8 | 🔴 High | SANDBOX-006-008 |
| **SANDBOX-011** | OWASP ZAP сканирование | Test | 5 | 🔴 High | API-014 |

---

## EPIC-013: Monitoring & Observability

**Описание**: Логирование, метрики, алертинг  
**Срок**: Недели 7-10 (Beta)  
**Ответственный**: Platform Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **MON-001** | Структурированное логирование (JSON) | Task | 5 | 🔴 High | — |
| **MON-002** | Интеграция Prometheus | Story | 8 | 🔴 High | MON-001 |
| **MON-003** | Метрика: workflow_execution_time | Task | 3 | 🔴 High | MON-002 |
| **MON-004** | Метрика: agent_execution_success_rate | Task | 3 | 🔴 High | MON-002 |
| **MON-005** | Метрика: token_usage_per_minute | Task | 3 | 🔴 High | MON-002, BUDGET-002 |
| **MON-006** | Метрика: guardrail_violations_total | Task | 3 | 🔴 High | MON-002, GR-012 |
| **MON-007** | Метрика: integration_request_duration | Task | 3 | 🔴 High | MON-002 |
| **MON-008** | Настройка Grafana | Task | 5 | 🔴 High | MON-002 |
| **MON-009** | Дашборд: Обзор системы | Task | 5 | 🔴 High | MON-008 |
| **MON-010** | Дашборд: Бюджет и затраты | Task | 5 | 🟡 Medium | MON-008 |
| **MON-011** | Дашборд: Производительность агентов | Task | 5 | 🟡 Medium | MON-008 |
| **MON-012** | Алерт: Бюджет превышен на 90% | Story | 3 | 🔴 High | MON-008, BUDGET-004 |
| **MON-013** | Алерт: Error rate >5% | Story | 3 | 🔴 High | MON-008 |
| **MON-014** | Алерт: SLA breach | Story | 3 | 🔴 High | MON-008 |
| **MON-015** | Интеграция ELK Stack (опционально) | Story | 8 | 🟢 Low | MON-001 |

---

## EPIC-014: Deployment & CI/CD

**Описание**: Развёртывание, контейнеризация, пайплайны  
**Срок**: Недели 2-3  
**Ответственный**: Platform Team

### Задачи

| ID | Задача | Тип | Story Points | Приоритет | Зависимости |
|----|--------|-----|--------------|-----------|-------------|
| **DEPLOY-001** | Dockerfile для оркестратора | Task | 5 | 🔴 High | — |
| **DEPLOY-002** | docker-compose.yml (локально) | Task | 5 | 🔴 High | DEPLOY-001 |
| **DEPLOY-003** | GitHub Actions: CI пайплайн | Story | 8 | 🔴 High | DEPLOY-001 |
| **DEPLOY-004** | GitHub Actions: тесты | Task | 5 | 🔴 High | DEPLOY-003 |
| **DEPLOY-005** | GitHub Actions: build Docker image | Task | 3 | 🔴 High | DEPLOY-003 |
| **DEPLOY-006** | GitHub Actions: push to registry | Task | 3 | 🔴 High | DEPLOY-005 |
| **DEPLOY-007** | Kubernetes manifests (опционально) | Story | 8 | 🟡 Medium | DEPLOY-001 |
| **DEPLOY-008** | Helm chart (опционально) | Story | 8 | 🟡 Medium | DEPLOY-007 |
| **DEPLOY-009** | Настройка окружений (dev/staging/prod) | Task | 5 | 🔴 High | DEPLOY-002 |
| **DEPLOY-010** | Секреты в CI/CD | Task | 5 | 🔴 High | DEPLOY-003 |
| **DEPLOY-011** | Документация развёртывания | Doc | 5 | 🟡 Medium | DEPLOY-002, DEPLOY-007 |

---

## Сводка по спринтам

### Спринт 1 (Недели 1-2): MVP Foundation
- **EPIC-001**: Parser Module (PARSER-001-010)
- **EPIC-007**: Storage Layer (STORAGE-001-016)
- **EPIC-009**: LLM Integrations (LLM-001-013)
- **EPIC-014**: Deployment & CI/CD (DEPLOY-001-006)

**Всего SP**: ~120

### Спринт 2 (Недели 2-3): Core Engine
- **EPIC-002**: Workflow Engine (WF-001-013)
- **EPIC-003**: Budget Tracker (BUDGET-001-012)
- **EPIC-008**: REST API (API-001-014)

**Всего SP**: ~100

### Спринт 3 (Недели 3-4): Agent Execution
- **EPIC-004**: Agent Executor (AGENT-001-015)
- **EPIC-006**: Guardrail Engine (GR-001-018, MVP часть)

**Всего SP**: ~110

### Спринт 4 (Недели 4-5): Alpha Features
- **EPIC-005**: Context Manager (CTX-001-016)
- **EPIC-010**: Git Integration (GIT-001-013)
- **EPIC-012**: Security & Sandbox (SANDBOX-001-011)

**Всего SP**: ~120

### Спринт 5 (Недели 5-6): Integrations
- **EPIC-011**: Issue Tracker Integration (TRACKER-001-014)
- **EPIC-006**: Guardrail Engine (оставшиеся задачи)

**Всего SP**: ~80

### Спринт 6-7 (Недели 7-10): Beta & Monitoring
- **EPIC-013**: Monitoring & Observability (MON-001-015)
- Стабилизация, багфиксы, нагрузочное тестирование

**Всего SP**: ~80

---

## Приложения

### A. Импорт в Jira

```csv
Summary,Issue Type,Priority,Story Points,Epic Link,Labels
"Настройка проекта Python 3.11+ с pydantic",Task,High,3,EPIC-001,parser;mvp
"Реализация схемы AFLConfig (Pydantic models)",Story,High,8,EPIC-001,parser;mvp
...
```

### B. Импорт в Linear

```json
[
  {
    "title": "Настройка проекта Python 3.11+ с pydantic",
    "type": "task",
    "priority": "high",
    "estimate": 3,
    "teamId": "core-team",
    "labelIds": ["parser", "mvp"]
  },
  ...
]
```

### C. Матрица ответственности

| Команда | Эпики |
|---------|-------|
| **Core Team** | EPIC-001, EPIC-002, EPIC-003, EPIC-007, EPIC-008, EPIC-010, EPIC-011, EPIC-014 |
| **AI Team** | EPIC-004, EPIC-005, EPIC-009 |
| **Security Team** | EPIC-006, EPIC-012 |
| **Platform Team** | EPIC-013, EPIC-014 |

---

*Документ сгенерирован на основе ТЗ AFL_Orchestrator_TZ_ADD.md v1.0*
