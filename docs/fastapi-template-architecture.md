# FastAPI Template Architecture

Tài liệu này giải thích layout của template và lý do nó được tổ chức như hiện tại.

## Mục tiêu thiết kế

Template này ưu tiên 4 mục tiêu cùng lúc:

- Bám sát convention phổ biến của FastAPI
- Giữ cấu trúc đủ rộng để dùng lại cho nhiều pattern khác nhau
- Tách rõ trách nhiệm giữa API, core, services, schemas và tests
- Dễ đọc với người mới clone repo lần đầu
- Có sẵn các package placeholder để mở rộng theo nhiều hướng khác nhau

## Cấu trúc thư mục

```text
app/
├── __init__.py
├── main.py
├── api/
│   ├── app.py
│   ├── dependencies.py
│   └── v1/
│       ├── router.py
│       └── endpoints/
├── core/
├── schemas/
├── services/
├── repositories/
├── models/
├── db/
├── utils/
├── common/
├── pipelines/
└── agents/
tests/
└── api/
    └── v1/
        └── endpoints/
```

## Ý nghĩa từng lớp

### `app/main.py`

Entry point của ứng dụng. File này tạo app, cấu hình logging, rồi khởi chạy Uvicorn khi chạy local.

### `app/api/`

Chứa mọi thứ liên quan đến HTTP layer:

- `app.py`: app factory
- `dependencies.py`: dependency dùng chung
- `v1/router.py`: gom router theo version
- `v1/endpoints/`: mỗi module route theo một nhóm chức năng

### `app/core/`

Nơi để các cấu hình nền tảng:

- settings
- logging
- security
- database helpers

### `app/schemas/`

Chứa Pydantic models cho request/response. Layer này giúp API contract rõ ràng và dễ test.

### `app/services/`

Chứa business logic. Route nên mỏng, không xử lý nghiệp vụ trực tiếp ở đây.

### `app/repositories/`

Placeholder cho lớp truy cập dữ liệu khi project cần database thật.

### `app/models/`

Placeholder cho ORM models.

### `app/db/`

Placeholder cho các helper hoặc pattern liên quan database.

### `app/utils/`

Placeholder cho helper dùng chung.

### `app/common/`

Placeholder cho các thành phần shared giữa nhiều feature.

### `app/pipelines/`

Placeholder cho flow xử lý nhiều bước, ví dụ ETL hoặc workflow pipeline.

### `app/agents/`

Placeholder cho agent-related patterns về sau.

## FastAPI conventions đang được áp dụng

- App factory nằm ở `app/api/app.py`
- Versioned router nằm ở `app/api/v1/router.py`
- Route modules nằm ở `app/api/v1/endpoints/`
- `health` endpoint riêng, `system/info` endpoint riêng
- Dependency được tách khỏi route
- Service layer được tách khỏi HTTP layer
- Các package placeholder được giữ sẵn để mở rộng khi project cần thêm pattern mới

## Khi thêm feature mới

Khuyến nghị đi theo flow này:

1. Tạo schema trong `app/schemas/`
2. Viết logic trong `app/services/`
3. Tạo route trong `app/api/v1/endpoints/`
4. Thêm test mirror theo `tests/api/v1/endpoints/`
