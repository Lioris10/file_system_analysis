# Model Version Review

Review date: 2026-07-15.

The YAML examples were updated after checking current public provider documentation. Because model catalogs change frequently, these examples should be rechecked before production deployment.

## Sources Checked

- OpenAI API model documentation: `https://platform.openai.com/docs/models` / `https://developers.openai.com/api/docs/models`.
- Google Gemini API model documentation: `https://ai.google.dev/gemini-api/docs/models`.
- Anthropic Claude model overview: `https://docs.anthropic.com/en/docs/about-claude/models/overview`.
- Amazon Bedrock supported models and model lifecycle documentation: `https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html` and `https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html`.

## YAML Model Examples Selected

| Provider | YAML example key | Model ID |
|---|---|---|
| OpenAI | `openai_gpt_5_6_sol` | `gpt-5.6-sol` |
| OpenAI | `openai_gpt_5_6_terra` | `gpt-5.6-terra` |
| Azure OpenAI | `azure_openai_deployment` | `my-gpt-5-6-deployment` |
| Google Gemini | `gemini_3_5_flash` | `gemini-3.5-flash` |
| Google Gemini | `gemini_3_1_pro_preview` | `gemini-3.1-pro-preview` |
| Anthropic | `anthropic_sonnet` | `claude-sonnet-5` |
| AWS Bedrock | `aws_bedrock_claude` | `anthropic.claude-sonnet-5` |
| AWS Bedrock | `aws_bedrock_claude_haiku` | `anthropic.claude-haiku-4-5-20251001-v1:0` |
| AWS Bedrock | `aws_bedrock_llama` | `meta.llama4-maverick-17b-instruct-v1:0` |
| Ollama | `local_ollama` | `llama3.1` |

## Important Caveats

- Azure OpenAI uses deployment names. The YAML example therefore uses `my-gpt-5-6-deployment` as a placeholder rather than assuming the public OpenAI model ID is the Azure deployment name.
- AWS Bedrock model availability is account-specific and region-specific. A model ID in YAML may still require enabling model access in the AWS console.
- Preview models, such as Gemini preview models, may change more frequently than stable model IDs.
- Local Ollama model names depend on models pulled into the local Ollama runtime.
