# IP Guard RAG Retrieval Worker

FAISS-based Retrieval-Augmented Generation (RAG) worker that finds similar character images using semantic visual search.

## Overview

This worker enables visual similarity search for IP detection. It's used by the IP Guard pipeline to:

1. Encode query images with an OpenCLIP vision encoder
2. Search FAISS index of reference character images
3. Return ranked results with similarity scores and metadata

**Key Features:**
- **Semantic search** - Find visually similar characters, not exact matches
- **OpenCLIP vision encoder** - Uses the OpenCLIP model configured in `worker/retrieval/build.py`
- **FAISS indexing** - Fast approximate nearest neighbor search
- **Batch processing** - Encode and search multiple images efficiently
- **Similarity filtering** - Filter results by minimum similarity threshold

## API Usage

### Request Format

```python
from colligo.models.ip_guard.worker.retrieval.types import IPGuardRAGRequest

# Basic retrieval
request = IPGuardRAGRequest(
    images=[
        "https://example.com/image.jpg",  # URL
        PublicBinary(...),                # From storage
        tensor,                           # In-memory tensor
    ],
    retrieval_k=3,              # Top-k results per image
    similarity_threshold=0.75,  # Min similarity score (0-1)
)

# With embeddings returned
request = IPGuardRAGRequest(
    images=["https://example.com/image.jpg"],
    retrieval_k=5,
    similarity_threshold=0.7,
    return_embeddings=True,  # Return base64-encoded embeddings
)
```

### Response Format

```python
from colligo.models.ip_guard.worker.retrieval.types import (
    IPGuardRAGResponse,
    RAGReference,
    ReferenceImage,
    IPGuardRAGMetadata,
)

response = IPGuardRAGResponse(
    references=[
        [  # References for first image
            RAGReference(
                similarity=0.95,  # Cosine similarity (0-1)
                reference=ReferenceImage(
                    idx=42,
                    uid="char_123",
                    data_url="data:image/jpeg;base64,...",
                    width=1024,
                    height=1024,
                    source_query="mickey mouse disney",
                    source_location="internal_reference_dataset",
                    automod_label="blocked",
                ),
            ),
            RAGReference(
                similarity=0.87,
                reference=ReferenceImage(...),
            ),
        ],
        [  # References for second image
            RAGReference(
                similarity=0.92,
                reference=ReferenceImage(...),
            ),
        ],
    ],
    metadata=IPGuardRAGMetadata(
        encoder="facebook/dinov2-base",
        encode_time_seconds=0.123,
        search_time_seconds=0.045,
        num_retrievals=3,  # Total across all images
    ),
    embeddings=None,  # Only if return_embeddings=True
)
```

## Configuration

### Worker Config (Deployment-time)

Set in `build.py`:

```python
from colligo.models.ip_guard.worker.retrieval.types import (
    IPGuardRAGConfig,
    IPGuardRAGEncoder,
)

worker_config = IPGuardRAGConfig(
    encoder=IPGuardRAGEncoder.DINOV2_BASE,
    torch_compile_mode="max-autotune",  # Torch compilation mode
)
```

### Request-time Parameters

Set in `IPGuardRAGRequest`:

```python
request = IPGuardRAGRequest(
    images=[...],
    retrieval_k=3,              # Top-k results per query image
    similarity_threshold=0.75,  # Min similarity to keep (0-1)
    return_embeddings=False,    # Whether to return embeddings
)
```

## Features

### 1. Vision Encoders

**Normalized embeddings:**
- All embeddings L2-normalized
- Cosine similarity via inner product
- Similarity range: [-1, +1] for cosine similarity

### 2. FAISS Index

**Index type:** `IndexFlatIP` (Inner Product, exhaustive search)
- **Pros:** Exact search, no approximation error, simple
- **Cons:** Linear time complexity O(n), slower for large indices

**Future:** Consider quantization or IVF for larger indices (>1M vectors)

**Currently CPU-based:**
```python
# GPU support disabled due to FAISS compatibility issues with H100
# See IPGuardRAG.py:52-58
self.index = faiss.read_index(str(source_dir / "index.faiss"))
```

### 3. Similarity Filtering

**Threshold filtering:**
```python
similarity_threshold=0.75  # Only keep references with similarity ≥ 0.75
```

**Common thresholds:**
- **0.85+** - Very similar (same character, different pose)
- **0.75-0.85** - Similar (same character family, related characters)
- **0.65-0.75** - Somewhat similar (same franchise, similar style)
- **<0.65** - Weak similarity (may be noise)

**Trade-offs:**
- **Higher threshold** → Fewer results, higher precision, may miss true positives
- **Lower threshold** → More results, higher recall, more false positives

### 4. Reference Metadata

**Stored in `reference.parquet`:**
```python
ReferenceImage(
    idx=42,                          # Index in FAISS
    uid="char_123",                  # Unique identifier
    data_url="data:image/jpeg;...",  # Base64-encoded image
    character="Mickey Mouse",        # Character name
    franchise="Disney",              # Franchise/IP owner
    category="animation",            # Category
    automoderation_status="blocked", # Auto-moderation flag
    source="internal",               # Data source
    width=512,                       # Image width in pixels
    height=512,                      # Image height in pixels
)
```

**Metadata alignment:**
- Index order matches parquet row order
- Fast lookup by index (pandas DataFrame index)
- Supports filtering by metadata fields (future)

### 5. Batch Processing

**Processes multiple images in parallel:**
```python
request = IPGuardRAGRequest(
    images=[image1, image2, ..., imageN],
    retrieval_k=3,
)
# Returns: [[ref1, ref2, ref3], [ref4, ref5, ref6], ...]
```

**Benefits:**
- Encoder batching for efficiency
- Parallel FAISS searches
- Single network round-trip

### 6. Embedding Export

**Optional embedding return:**
```python
request = IPGuardRAGRequest(
    images=[...],
    return_embeddings=True,
)

response = IPGuardRAGResponse(
    references=[...],
    embeddings=[
        "base64_encoded_float32_array_1",
        "base64_encoded_float32_array_2",
    ],
)
```

**Use cases:**
- Caching embeddings for repeated queries
- Building custom similarity metrics
- Analyzing embedding space

**Format:** Base64-encoded float32 numpy arrays

## Index Management

### Creating a FAISS Index

**Requirements:**
1. Directory of reference images
2. CSV with metadata (character, franchise, etc.)
3. Selected encoder model

**Steps:**

1. **Encode reference images:**
```python
from colligo.models.ip_guard.helpers.encoder import RAGEncoder

encoder = RAGEncoder.create(
    encoder_name="facebook/dinov2-base",
    device="cuda",
)
encoder.load_model()

embeddings = []
for image_path in reference_images:
    image = Image.open(image_path)
    embedding = encoder.encode([image])
    embeddings.append(embedding)

embeddings = np.vstack(embeddings)
```

2. **Build FAISS index:**
```python
import faiss

# Create index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatIP(embedding_dim)

# Add embeddings
index.add(embeddings)

# Save index
faiss.write_index(index, "index.faiss")
```

3. **Create metadata file:**
```python
import pandas as pd

metadata = pd.DataFrame([
    {
        "idx": 0,
        "uid": "char_001",
        "data_url": "data:image/jpeg;base64,...",
        "character": "Mickey Mouse",
        "franchise": "Disney",
        "category": "animation",
        "automoderation_status": "blocked",
        "source": "internal",
    },
    # ... more rows
])

metadata.to_parquet("reference.parquet", index=False)
```

4. **Create encoder name file:**
```bash
echo "facebook/dinov2-base" > ENCODER_NAME
```

5. **Package and upload:**
```bash
tar -czf characters_v1.tar.gz index.faiss reference.parquet ENCODER_NAME
./m deps.upload_artifact characters_v1.tar.gz ip_guard/index/dinov2-base
```

### Updating the Index

**When to update:**
- Adding new reference characters
- Improving reference image quality
- Changing encoder model
- Updating metadata

**Process:**
1. Rebuild index with new data
2. Upload to S3 with new version
3. Update `build.py` with new S3 source
4. Redeploy worker

**Important:** Index must match configured encoder. Worker validates on startup:
```python
def validate_encoder(self, encoder: IPGuardRAGEncoder) -> None:
    index_encoder = (self.source_dir / "ENCODER_NAME").read_text().strip()
    runtime_assert(
        index_encoder == encoder.value,
        f"Index encoder mismatch: '{index_encoder}' != '{encoder.value}'"
    )
```

## Testing

```bash
# All retrieval tests
pytest models/colligo/models/ip_guard/tests/test_retrieve.py

# Encoder tests
pytest models/colligo/models/ip_guard/tests/test_encoder.py

# With debug output
pytest models/colligo/models/ip_guard/tests/test_retrieve.py -v -s
```

## Known Limitations

1. **CPU-based FAISS:**
   - GPU support disabled due to H100 compatibility issues
   - Linear search time O(n) - slower for large indices
   - Consider quantization for >100K vectors

2. **Encoder selection:**
   - Must match index encoder
   - Changing encoder requires rebuilding index
   - No automatic encoder detection

3. **Similarity interpretation:**
   - Scores depend on encoder and reference distribution
   - May require threshold tuning per use case
   - No absolute similarity scale

4. **Reference image quality:**
   - Quality affects retrieval accuracy
   - Variety important for coverage
   - Bias towards training distribution

## Related Documentation

- [Pipeline Worker](../pipeline/README.md) - Main IP Guard pipeline
- [Detection Worker](../detection/README.md) - Object detection for IP regions
- [Configuration Guide](../../aidoc/configuration.md) - Encoder and index configuration