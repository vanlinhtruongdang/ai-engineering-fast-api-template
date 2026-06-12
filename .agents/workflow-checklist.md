# Working Checklist

Checklist ngắn cho dev/agent khi làm việc trong template này.

## Trước khi code

- Đọc đúng file cần sửa
- Xác định ranh giới thay đổi
- Ưu tiên sửa nguyên nhân gốc
- Nếu liên quan FastAPI, kiểm tra đúng convention trước

## Khi code

- Giữ thay đổi nhỏ và rõ ràng
- Viết code theo `ruff` và `ty`
- Dùng tên phản ánh đúng chức năng
- Không thêm placeholder hay alias nếu không cần
- Nếu chạm tới code có khả năng nặng, hỏi trước: đây có phải hot path không, và đã profile chưa?
- Tránh tạo copy dữ liệu hoặc loop nặng nếu có thể thay bằng built-in, generator, hoặc cache

## Sau khi code

- Chạy `ruff format`
- Chạy `ruff check`
- Chạy `ty check`
- Chạy `pytest`
- Nếu có thay đổi liên quan hiệu năng, ghi lại cách đo hoặc lý do tối ưu trong note/PR
- Kiểm tra `git status`
- Viết commit message theo conventional commit nếu cần commit

## Khi làm với Docker

- Ưu tiên official base images
- Không bake secrets hay env runtime vào image
- Giữ compose/dev/prod rõ ràng
- Tránh `container_name` nếu không có yêu cầu đặc biệt
