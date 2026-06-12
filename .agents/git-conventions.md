# Git Conventions

Tài liệu này quy định chuẩn git cho project.

## 1. Branch naming

Khuyến nghị:

- `feat/<short-desc>`
- `fix/<short-desc>`
- `refactor/<short-desc>`
- `docs/<short-desc>`
- `chore/<short-desc>`

Ví dụ:

- `feat/fastapi-template-layout`
- `fix/docker-base-image`
- `docs/internal-agent-guides`

## 2. Commit message

Dùng conventional commit.

Format:

- `<type>(<scope>): <summary>`

Types thường dùng:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`
- `build`

Ví dụ:

- `feat(api): add system info endpoint`
- `fix(docker): remove baked env files from image`
- `docs(agents): add internal coding guidelines`
- `refactor(core): move logging init into lifespan`

## 3. Commit rules

- Mỗi commit nên có một mục đích rõ ràng
- Tránh gộp quá nhiều ý khác nhau trong cùng một commit
- Không commit file cache, bytecode, hoặc artifact build
- Không commit thay đổi không liên quan đến task hiện tại
- Nếu cần sửa nhiều lớp, ưu tiên chia thành nhiều commit logic

## 4. Working rules

- Kiểm tra `git status` trước khi kết thúc
- Đọc diff trước khi commit
- Không dùng `git reset --hard`
- Không dùng `git checkout --` để xóa thay đổi của người khác
- Chỉ rewrite history khi user yêu cầu rõ ràng

## 5. Suggested scopes

Một số scope gợi ý cho repo này:

- `api`
- `core`
- `docker`
- `tests`
- `docs`
- `agents`
- `build`

## 6. Good examples

- `feat(api): add health endpoint`
- `refactor(core): defer logging initialization`
- `test(api): cover system info response`
- `docs(agents): define coding workflow`
