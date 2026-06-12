# Python & FastAPI Conventions

Tài liệu này quy định chuẩn code cho toàn bộ template.

## 1. Python style

- Dùng Python 3.12+
- Ưu tiên code rõ ràng, ngắn gọn, dễ đọc
- Viết type hints cho public functions và data structures
- Dùng `from __future__ import annotations` nếu dự án cần
- Ưu tiên built-in functions và standard library trước khi thêm dependency mới
- Tránh tối ưu sớm nếu chưa profile
- Ưu tiên cấu trúc dữ liệu đúng mục đích: `dict` cho lookup, `set` cho membership
- Hạn chế tạo bản sao dữ liệu không cần thiết
- Dùng cache như `lru_cache` cho computation đắt tiền nhưng ổn định

## 2. Ruff rules

Mọi thay đổi Python phải pass `ruff`:

- Chạy `ruff format` cho format
- Chạy `ruff check` cho lint
- Không để import thừa
- Không để biến, hàm, hoặc file rác không dùng
- Giữ code theo line length và import order của project

## 3. Ty rules

Mọi thay đổi Python phải pass `ty`:

- Không bỏ qua lỗi unresolved import
- Không bỏ qua lỗi type chỉ vì “chạy được”
- Giữ type của function rõ ràng
- Dùng `dict[str, ...]`, `list[...]`, `Optional[...]` hoặc `| None` nhất quán

## 4. FastAPI convention

- App entry point nằm ở `app/main.py`
- App factory nằm ở `app/api/app.py`
- Route versioned nằm ở `app/api/v1/router.py`
- Route modules nằm ở `app/api/v1/endpoints/`
- `app/core/` dành cho config, logging, security, infra helpers
- `app/services/` dành cho business logic
- `app/schemas/` dành cho request/response schema
- Dependency dùng `Depends()` và tách khỏi handler khi hợp lý
- Route handler nên mỏng, không nhét nghiệp vụ vào handler
- Ưu tiên async cho các flow I/O hoặc kiến trúc cần mở rộng
- Dùng `lifespan` cho init/cleanup thay vì side effect import-time

## 5. Naming

- Router cấp version nên dùng tên `api_router`
- Route module nên đặt theo chức năng, ví dụ `health.py`, `info.py`
- Hàm handler nên đặt theo action, ví dụ `read_system_info`
- Schema nên đặt theo mục đích, ví dụ `HealthResponse`
- Tránh tên mơ hồ như `service_root`, `main_route`, nếu nó không phản ánh đúng ý nghĩa

## 6. Validation checklist

Trước khi hoàn tất công việc, tối thiểu phải kiểm tra:

- `uv run ruff format`
- `uv run ruff check`
- `uv run ty check`
- `uv run pytest`

## 7. Khi thêm feature mới

- Tạo schema trước nếu API contract thay đổi
- Tách logic vào service thay vì để ở route
- Chỉ thêm repository/model khi thật sự có data access layer
- Thêm test tương ứng theo cùng nhánh thư mục
- Nếu feature có khả năng nặng, đo trước bằng benchmark hoặc profiling nhỏ thay vì đoán
