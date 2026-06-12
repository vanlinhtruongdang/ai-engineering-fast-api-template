# FastAPI Template

Template FastAPI dùng làm nền cho các backend service về sau. Cấu trúc này ưu tiên:

- Bám convention của FastAPI
- Giữ layout rõ ràng, dễ mở rộng
- Tách config, API, service, schema, test thành các lớp riêng
- Dùng layout canonical với `app/` ở root
- Giữ sẵn một số package placeholder cho các pattern mở rộng về sau

## Layout

```text
app/
├── __init__.py              # App package marker
├── main.py                  # Entry point khởi động app
├── api/
│   ├── app.py               # App factory
│   ├── dependencies.py      # Shared dependencies
│   └── v1/
│       ├── router.py        # Version router
│       └── endpoints/       # FastAPI convention cho route modules
├── core/                    # Config, logging, nền tảng hệ thống
├── schemas/                 # Pydantic schemas
├── services/                # Business logic
├── repositories/            # Repository placeholder
├── models/                  # ORM placeholder
├── db/                      # DB helper placeholder
├── utils/                   # Utility placeholder
├── common/                  # Shared/common placeholder
├── pipelines/               # Pipeline placeholder
└── agents/                  # Agent placeholder
```

## Conventions

- `app/api/v1/endpoints/`: nơi đặt module route theo convention phổ biến của FastAPI
- `app/api/v1/router.py`: gom các endpoints theo version
- `app/core/`: giữ các cấu hình, logging, security, database helpers
- `app/services/`: chứa business logic, không để route xử lý trực tiếp
- `app/schemas/`: chứa Pydantic models cho request/response

## Development

- Cài dependency: `uv sync`
- Chạy app: `uv run python -m app.main`
- Chạy test: `uv run pytest`

## Template Notes

- Cấu trúc hiện tại ưu tiên tính rõ ràng và khả năng mở rộng hơn là tối giản số lượng thư mục.
- Các package placeholder trong `app/` được giữ lại có chủ đích để template cover nhiều pattern khác nhau.

## Tài liệu chi tiết

- Xem thêm: [docs/fastapi-template-architecture.md](/home/linhtdv/fpt-work/coding-template/fast-api/docs/fastapi-template-architecture.md)
