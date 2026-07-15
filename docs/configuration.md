# Configuration Specification

All runtime behavior that can vary between environments must be controlled by YAML. This includes the LLM provider, model name, credential source, summary length, supported extensions, file-size limits, date format, and UI direction.

## Python Version

The project targets Python 3.12 or newer.

## LLM Configuration

The active provider is configured with `llm.provider`. The active model is configured with `llm.model_name`. Credentials should be read from environment variables by using provider-specific `api_key_env` settings.

Example OpenAI configuration:

```yaml
llm:
  provider: "openai"
  model_name: "gpt-4o-mini"
  api_key_env: "OPENAI_API_KEY"
```

Example Gemini configuration:

```yaml
llm:
  provider: "gemini"
  model_name: "gemini-1.5-pro"
  api_key_env: "GOOGLE_API_KEY"
```

Example Anthropic configuration:

```yaml
llm:
  provider: "anthropic"
  model_name: "claude-3-5-sonnet-latest"
  api_key_env: "ANTHROPIC_API_KEY"
```

## Generic Model Factory Contract

The planned `ModelFactory` must:

1. Read `llm.provider`.
2. Locate the provider definition under `llm.providers`.
3. Resolve the provider class, for example `langchain_openai.ChatOpenAI`.
4. Read the configured API key environment variable.
5. Instantiate the model with `model_name`, temperature, timeout, and retry settings.
6. Return a LangChain-compatible chat model.

No application service or graph node may hard-code a specific model provider.

## Summary Configuration

```yaml
summarization:
  output_max_chars: 2000
  preserve_source_language: true
```

The default summary length is 2,000 characters. The prompt must instruct the model to summarize in the original source language and not translate the document.
