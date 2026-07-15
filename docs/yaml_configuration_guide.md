# YAML Configuration Guide

This guide explains how to configure `config/config.example.yaml` for the file_system_analysis application.

## 1. Basic Rule

The application is designed so runtime choices are made through YAML. The code should read this file at startup and should not hard-code the LLM provider, model name, API key, scan behavior, summary length, or UI direction.

## 2. `app` Section

```yaml
app:
  name: "file_system_analysis"
  runtime_python: "3.12+"
  platform: "windows"
  language: "en"
  rtl_enabled: true
  theme: "light"
```

| Key | Meaning |
|---|---|
| `name` | Display/application name. |
| `runtime_python` | Human-readable runtime requirement. Actual Poetry enforcement is in `pyproject.toml`. |
| `platform` | Target operating system. |
| `language` | Default UI language. |
| `rtl_enabled` | Enables right-to-left layout support for Hebrew. |
| `theme` | Planned UI theme name. |

## 3. `ui` Section

```yaml
ui:
  default_layout_direction: "rtl"
  table_page_size: 200
  show_full_path: false
  date_time_format: "%Y-%m-%d %H:%M:%S"
```

| Key | Meaning |
|---|---|
| `default_layout_direction` | Use `rtl` for Hebrew-friendly layout or `ltr` for English-only layout. |
| `table_page_size` | Number of rows to load/display per page or batch. |
| `show_full_path` | If `true`, the UI can display full file paths; if `false`, it should show file names. |
| `date_time_format` | Format used for created/modified timestamps. |

## 4. `scanner` Section

```yaml
scanner:
  recursive_default: false
  max_file_size_mb: 50
  supported_extensions:
    - ".txt"
    - ".md"
    - ".pdf"
```

| Key | Meaning |
|---|---|
| `recursive_default` | Default value for scanning subdirectories. The UI can still let the user override it. |
| `max_file_size_mb` | Prevents reading very large files into memory. |
| `supported_extensions` | File types the application should list and attempt to read. |

## 5. `llm` Section

The top-level fields under `llm` select the active provider and model:

```yaml
llm:
  provider: "openai"
  model_name: "gpt-5.6-terra"
  api_key_env: "OPENAI_API_KEY"
  temperature: 0.2
  timeout_seconds: 60
  max_retries: 2
```

| Key | Meaning |
|---|---|
| `provider` | Active provider key. It must match one key under `llm.providers`. |
| `model_name` | Active model/deployment ID. |
| `api_key_env` | Environment variable that contains the provider API key. Not used by every provider. |
| `temperature` | Lower values produce more deterministic summaries. `0.2` is recommended for summarization. |
| `timeout_seconds` | Request timeout for LLM calls. |
| `max_retries` | Retry count for transient provider/API failures. |

## 6. Provider Blocks

Provider blocks define how the planned `ModelFactory` should create a LangChain chat model.

### OpenAI

```yaml
llm:
  provider: "openai"
  model_name: "gpt-5.6-terra"
  api_key_env: "OPENAI_API_KEY"
```

Required environment variable:

```powershell
$env:OPENAI_API_KEY="sk-..."
```

### Azure OpenAI

```yaml
llm:
  provider: "azure_openai"
  model_name: "my-gpt-5-6-deployment"
  api_key_env: "AZURE_OPENAI_API_KEY"
  endpoint_env: "AZURE_OPENAI_ENDPOINT"
```

Required environment variables:

```powershell
$env:AZURE_OPENAI_API_KEY="..."
$env:AZURE_OPENAI_ENDPOINT="https://<resource-name>.openai.azure.com/"
```

Important: for Azure OpenAI, `model_name` is usually the Azure deployment name, not necessarily the public model ID.

### Google Gemini

```yaml
llm:
  provider: "gemini"
  model_name: "gemini-3.5-flash"
  api_key_env: "GOOGLE_API_KEY"
```

Required environment variable:

```powershell
$env:GOOGLE_API_KEY="..."
```

### Anthropic

```yaml
llm:
  provider: "anthropic"
  model_name: "claude-sonnet-5"
  api_key_env: "ANTHROPIC_API_KEY"
```

Required environment variable:

```powershell
$env:ANTHROPIC_API_KEY="..."
```

### AWS Bedrock

```yaml
llm:
  provider: "bedrock"
  model_name: "anthropic.claude-sonnet-5"
  region_name_env: "AWS_REGION"
  profile_name_env: "AWS_PROFILE"
```

Recommended environment variables when using an AWS profile:

```powershell
$env:AWS_PROFILE="my-bedrock-profile"
$env:AWS_REGION="us-east-1"
```

Alternative environment variables when using direct temporary or long-lived AWS credentials:

```powershell
$env:AWS_ACCESS_KEY_ID="..."
$env:AWS_SECRET_ACCESS_KEY="..."
$env:AWS_SESSION_TOKEN="..."  # only if using temporary credentials
$env:AWS_REGION="us-east-1"
```

Important Bedrock notes:

- The AWS account must have model access enabled for the selected Bedrock model.
- Bedrock model availability depends on AWS Region.
- Some Bedrock model IDs may require cross-region inference profile prefixes in certain accounts or Regions.

### Ollama

```yaml
llm:
  provider: "ollama"
  model_name: "llama3.1"
  base_url: "http://localhost:11434"
```

Ollama is useful for local/offline development when the required model is available locally.

## 7. How to Switch Models

To switch from OpenAI to Gemini, edit only this part:

```yaml
llm:
  provider: "gemini"
  model_name: "gemini-3.5-flash"
  api_key_env: "GOOGLE_API_KEY"
```

To switch from Gemini to AWS Bedrock Claude, edit only this part:

```yaml
llm:
  provider: "bedrock"
  model_name: "anthropic.claude-sonnet-5"
  region_name_env: "AWS_REGION"
  profile_name_env: "AWS_PROFILE"
```

The implementation should then load the matching provider block from `llm.providers`.

## 8. `summarization` Section

```yaml
summarization:
  output_max_chars: 2000
  preserve_source_language: true
  chunk_size_chars: 12000
  chunk_overlap_chars: 500
```

| Key | Meaning |
|---|---|
| `output_max_chars` | Maximum target summary length. Default is 2,000 characters. |
| `preserve_source_language` | If `true`, the prompt instructs the model to summarize in the original document language. |
| `chunk_size_chars` | Approximate chunk size for large documents. |
| `chunk_overlap_chars` | Overlap between chunks to preserve context. |

## 9. Recommended First Configuration

For initial development, use a cost-balanced hosted model:

```yaml
llm:
  provider: "openai"
  model_name: "gpt-5.6-terra"
  api_key_env: "OPENAI_API_KEY"
```

For AWS-only environments, use Bedrock:

```yaml
llm:
  provider: "bedrock"
  model_name: "anthropic.claude-sonnet-5"
  region_name_env: "AWS_REGION"
  profile_name_env: "AWS_PROFILE"
```
