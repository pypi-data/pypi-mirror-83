# Multiplexer
---
Multiplexer is an encryption library.

## Installation

```bash
pip install multiplexer
```

## Usage

```python
from multiplexer import Plex, generate, load

book = load() or generate("michel", save=True)

p = Plex(book)

cypher = p.encode('My secret message')
print(cypher)

secret_message = p.decode(cypher)
print(secret_message)

# Human readable
cypher = p.h_encode('My secret message')
print(cypher)

secret_message = p.h_decode(cypher)
print(secret_message)
```

## Logging

```python
import logging

logger = logging.getLogger('multiplexer')
logger.setLevel(logging.INFO)
```