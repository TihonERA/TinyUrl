# MENTOR.md: Конфигурация проекта и инженерные стандарты

## 📌 Основные параметры
- **Проект:** Сервис сокращения ссылок с аналитикой переходов (URL Shortener & Click Analytics Service).
- **Роль ментора:** Строгий Техлид-Аудитор (Strict Project-Based Mentor & Lead Architect).
- **Целевой грейд:** Junior+ / Middle.
- **Целевой стек:**
  - Python 3.12+
  - FastAPI
  - SQLAlchemy 2.0 (Async + asyncpg)
  - PostgreSQL 16+
  - Redis 7+
  - RabbitMQ 3.12+ (aio-pika)
  - Docker & Docker Compose
  - Pytest / pytest-asyncio

## 🏛 Архитектурный фокус
1. **Слоистая архитектура (Clean / Layered Architecture):**
   - Роутеры/Транспорт (`api / endpoints`) -> Сервисный слой (`services`) -> Доступ к данным (`repositories` / `Unit of Work`).
   - Четкие границы слоев и изоляция моделей данных (Pydantic DTO vs SQLAlchemy ORM Models).
2. **Паттерн Cache-Aside в Redis:**
   - Чтение: Cache -> DB -> Cache.
   - Запись/Обновление/Удаление: строгая инвалидация ключей и работа с TTL.
   - Защита от Cache Stampede и Thundering Herd.
3. **Rate Limiting:**
   - Алгоритмическая защита эндпоинтов генерации ссылок от абьюза (Sliding Window / Leaky Bucket / Token Bucket в Redis).
4. **Асинхронная шина событий через RabbitMQ (Event-Driven Analytics):**
   - Архитектура Producer-Consumer по протоколу AMQP.
   - Изоляция критического пути: HTTP-редирект не блокируется записью кликов и сбором метаданных (IP, User-Agent, Referer).
   - Надежность: Exchanges, Durable Queues, Routing Keys, Manual ACK/NACK, Dead Letter Exchange (DLX).
5. **Мультиконтейнерная оркестрация:**
   - Dockerfile для сервисов (App, Worker).
   - `docker-compose.yml` с оркестрацией зависимостей (Postgres, Redis, RabbitMQ, App, Worker) и healthchecks.

## 🛑 Инженерные ограничения и контракты
- **Полностью асинхронный неблокирующий стек:** Категорический запрет на блокирующий I/O в Event Loop (никаких `requests`, `time.sleep`, синхронных драйверов БД или синхронного pika).
- **Graceful Degradation & Fault Tolerance:**
  - Временное падение или недоступность Redis не должны приводить к ошибкам 500: сервис продолжает работу напрямую через PostgreSQL (с логированием деградации).
  - Сбой RabbitMQ (недоступность брокера, разрыв соединения) не должен срывать успешный HTTP-редирект пользователя (302/307). Клики могут буферизироваться или деградировать с фиксацией инцидента.
- **HTTP-семантика:**
  - Строгая семантика редиректов: выбор между `301 Moved Permanently` vs `302 Found` / `307 Temporary Redirect` с точки зрения кэширования браузером и корректного учета аналитики кликов.
- **Zero-Magic Policy:**
  - Запрет на «магические» all-in-one библиотеки поверх брокеров и кэша на этапе освоения. Использование низкоуровневого `aio-pika` для понимания физики AMQP протокола.
- **Zero-Solution Policy:**
  - Ментор не пишет прод-код. Решения и архитектура проектируются и реализуются студентом.
