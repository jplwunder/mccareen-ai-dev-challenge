from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

source = "https://arxiv.org/pdf/2408.09869"  # PDF path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(
    result.document.export_to_markdown()
)  # output: "### Docling Technical Report[...]"


def convert_document_to_markdown(source: str) -> str:
    """
    Convert a document from a given source to Markdown format.

    Args:
        source (str): The path or URL of the document to convert.

    Returns:
        str: The converted document in Markdown format.
    """
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_markdown()
