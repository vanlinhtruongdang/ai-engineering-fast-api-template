# Internal Agent Guide

Tài liệu này dành cho dev và agent làm việc trong template FastAPI này.

## Mục tiêu

- Code phải theo chuẩn `ruff`
- Type-check phải theo `ty`
- API phải bám FastAPI convention
- Git phải theo git convention thống nhất

## Tài liệu liên quan

- [Python & FastAPI conventions](./python-fastapi-conventions.md)
- [Git conventions](./git-conventions.md)
- [Performance guidelines](./performance-guidelines.md)
- [Working checklist](./workflow-checklist.md)

## Nguyên tắc chung

- Ưu tiên sửa đúng root cause thay vì vá tạm
- Giữ thay đổi nhỏ, rõ ràng, dễ review
- Không tạo thêm file hay thư mục nếu chưa có lý do rõ ràng
- Luôn kiểm tra lại bằng công cụ phù hợp trước khi kết thúc
