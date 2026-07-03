# Install & Update

## 各平台安装

**macOS/Linux**
```bash
curl -fsSL https://opencode.ai/install | bash
```

**Windows (Scoop)**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install opencode
```

**验证安装**
```bash
opencode --version
```

## 网络代理配置

```bash
# macOS/Linux
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# Windows PowerShell
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
```

## API Key 配置

方式一：`opencode auth login`（交互式）
方式二：环境变量（自动检测）
- `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `DEEPSEEK_API_KEY` / `ZHIPUAI_API_KEY` 等
- 支持 75+ 模型提供商

凭证存储位置：`~/.local/share/opencode/auth.json`

## 自动更新

```bash
opencode update
```
