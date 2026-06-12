# Performance Guidelines

Tài liệu này gom các nguyên tắc tối ưu hiệu năng cho Python/FastAPI trong template này.

## Nguyên tắc cốt lõi

- Profile trước khi tối ưu
- Tập trung vào hot path, không tối ưu chỗ hiếm khi chạy
- Giữ code rõ ràng trước, tối ưu sau
- Tối ưu theo dữ liệu thật, không theo cảm giác

## Khi nghi ngờ chậm

Ưu tiên kiểm tra theo thứ tự:

1. CPU profiling nếu nghi ngờ compute nặng
2. Memory profiling nếu nghi ngờ cấp phát hoặc leak
3. Line profiling nếu cần biết dòng nào đắt
4. Call graph nếu cần thấy luồng gọi phức tạp

## Cách tối ưu trong Python

- Ưu tiên built-in và standard library vì đã được tối ưu ở mức C
- Dùng `dict` cho tra cứu nhanh và `set` cho membership check
- Tránh tạo object hoặc copy dữ liệu trong loop nếu không cần
- Dùng generator khi xử lý dữ liệu lớn
- Cache computation đắt nhưng ổn định bằng `lru_cache` hoặc cache layer phù hợp
- Batch I/O để giảm số lần gọi hệ thống
- Chọn async cho I/O-bound flow và tránh blocking trong request path

## Cách tối ưu trong FastAPI

- Giữ handler mỏng, chuyển business logic ra service
- Không làm work nặng ở import-time
- Dùng `lifespan` cho init/cleanup
- Tránh dựng dependency hoặc settings nhiều lần nếu có thể cache hợp lý
- Chỉ bật tính năng nặng như debug/docs/reference khi thực sự cần trong môi trường đó

## Database và I/O

- Dùng connection pooling nếu có database
- Giảm round trip tới database bằng query hợp lý
- Chỉ select đúng field cần dùng
- Tránh N+1 query
- Tối ưu serialization nếu response lớn

## Khi cần benchmark

Gợi ý:

- Dùng `timeit` cho timing nhỏ
- Dùng `cProfile` cho CPU bottleneck
- Dùng tool memory profiling khi nghi ngờ memory growth
- Dùng production-like data khi benchmark

## Không nên làm

- Tối ưu khi chưa đo
- Thêm cache vô tội vạ
- Hy sinh readability cho micro-optimization chưa chứng minh được lợi ích
- Tạo nhiều bản sao dữ liệu không cần thiết
- Đưa logic nặng vào import-time hoặc request handler
