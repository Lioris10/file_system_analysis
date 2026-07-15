# LangGraph Workflow Specification

## State

The planned graph state should include:

```python
class FileProcessingState(TypedDict):
    file_path: str
    metadata: dict | None
    content: str | None
    chunks: list[str]
    partial_summaries: list[str]
    summary: str | None
    error: str | None
```

## Nodes

- `read_metadata_node`
- `read_content_node`
- `clean_text_node`
- `split_content_node`
- `summarize_node`
- `combine_summaries_node`
- `finalize_node`
- `error_node`

## Normal Flow

```text
START
  -> read_metadata
  -> read_content
  -> clean_text
  -> split_content
  -> summarize
  -> combine_summaries
  -> finalize
  -> END
```

## Error Flow

Any node that cannot process the current file should set `error` and route to `error_node`. A failed file must not stop the processing of other files.

## LangChain Integration

The `summarize_node` must call a provider-neutral summarization service that receives a LangChain chat model created by the YAML-driven model factory.
