# DocDump

#### Grant Holtes 2020
### A package to extract text from common document types

DocDump aims to allow for raw text data and document metadata to be easily extracted from a 
range of commonly used document types, such as Word, PDF, PowerPoint, Excel, txt. 

DocDump extracts all text as a single string, and does not preserve text structure. This makes
it a useful tool in a natural language processing or search pipeline.

DocDump does not perform any preprocessing or normalisation.

## Usage

```python
from docdump import doc_reader

document = doc_reader("sampleFile.docx")

text_dump = document.text
metadata = document.metadata
filetype = document.filetype
absolute_path = document.path
```
 
## Installation:

Use pip to install the package and its dependancies.

```bash
pip install docdump
```