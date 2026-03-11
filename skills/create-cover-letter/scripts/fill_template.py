"""
Fill a Word .dotx template by replacing {{PLACEHOLDER}} tokens in the XML.

Word splits placeholder text across multiple XML <w:r> (run) elements, so we
work at the paragraph level: concatenate all <w:t> text in a <w:p>, find
placeholders in the concatenated text, then map replacement text back into
the XML runs.

Usage:
    python fill_template.py <template.dotx> <output.docx> <json_replacements>

    json_replacements is a JSON string: {"DATE": "3/6/2026", "JOB TITLE": "...", ...}
"""

import sys
import json
import re
import zipfile
import shutil
import os
import tempfile
from xml.etree import ElementTree as ET


NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

for prefix, uri in NSMAP.items():
    ET.register_namespace(prefix, uri)


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def replace_in_paragraph_xml(para_xml, replacements):
    """
    Given raw XML for a single <w:p> element, find {{KEY...}} placeholders
    in the concatenated text, replace them, and rebuild the XML.

    Strategy:
    1. Extract all <w:t> elements and their text, building a text-to-run map
    2. Concatenate all text to find placeholders
    3. Replace placeholder text in the concatenation
    4. Redistribute the new text back into the <w:t> elements
    """
    # Find all <w:t...>TEXT</w:t> in this paragraph with their positions
    t_pattern = re.compile(r'(<w:t[^>]*>)(.*?)(</w:t>)', re.DOTALL)
    t_matches = list(t_pattern.finditer(para_xml))

    if not t_matches:
        return para_xml

    # Build concatenated text and track which chars map to which match
    concat = ""
    char_to_match = []  # For each char in concat, which match index it belongs to
    for i, m in enumerate(t_matches):
        text = m.group(2)
        for ch in text:
            char_to_match.append(i)
        concat += text

    # Find all {{...}} placeholders in the concatenated text
    placeholder_re = re.compile(r'\{\{.*?\}\}')
    ph_matches = list(placeholder_re.finditer(concat))

    if not ph_matches:
        return para_xml

    # Check each placeholder against our replacements
    new_concat = concat
    offset = 0
    for ph in ph_matches:
        ph_text = ph.group(0)  # e.g. "{{DATE}}" or "{{COMPANY NAME}}"
        ph_inner = ph_text[2:-2].strip()  # e.g. "DATE" or "COMPANY NAME"

        # Match against replacement keys — the placeholder inner text starts with the key
        for key, value in replacements.items():
            if ph_inner.upper().startswith(key.upper()):
                start = ph.start() + offset
                end = ph.end() + offset
                new_concat = new_concat[:start] + value + new_concat[end:]
                offset += len(value) - (ph.end() - ph.start())
                break

    if new_concat == concat:
        return para_xml

    # Now redistribute new_concat back into the <w:t> elements
    # Strategy: put all text in the first <w:t>, empty the rest
    # But we need to handle text OUTSIDE placeholders that should stay in their runs

    # Simpler: since the paragraph contains a placeholder, replace all <w:t> content
    # Put the full new text in the first <w:t> and empty the rest
    new_para = para_xml
    # Process in reverse order to preserve positions
    for i, m in enumerate(reversed(t_matches)):
        idx = len(t_matches) - 1 - i
        if idx == 0:
            # First <w:t>: put all the new concatenated text here
            new_t = '<w:t xml:space="preserve">' + escape_xml(new_concat) + '</w:t>'
        else:
            # Subsequent <w:t>: empty them
            new_t = m.group(1) + m.group(3)
        new_para = new_para[:m.start()] + new_t + new_para[m.end():]

    return new_para


def fill_template(template_path, output_path, replacements):
    """Open a .dotx template, replace placeholders, save as .docx."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_zip = os.path.join(tmpdir, 'template.zip')
        shutil.copy2(template_path, tmp_zip)

        files = {}
        with zipfile.ZipFile(tmp_zip, 'r') as zin:
            for item in zin.namelist():
                files[item] = zin.read(item)

        # Process document.xml
        doc_xml = files['word/document.xml'].decode('utf-8')

        # Split into paragraphs and process each one
        # Find all <w:p ...>...</w:p> elements
        para_pattern = re.compile(r'(<w:p[ >].*?</w:p>)', re.DOTALL)
        parts = para_pattern.split(doc_xml)

        new_parts = []
        for part in parts:
            if part.startswith('<w:p'):
                part = replace_in_paragraph_xml(part, replacements)
            new_parts.append(part)

        doc_xml = ''.join(new_parts)
        files['word/document.xml'] = doc_xml.encode('utf-8')

        # Fix content type from template to document
        if '[Content_Types].xml' in files:
            ct = files['[Content_Types].xml'].decode('utf-8')
            ct = ct.replace(
                'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
            )
            files['[Content_Types].xml'] = ct.encode('utf-8')

        # Write the new .docx
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for name, data in files.items():
                zout.writestr(name, data)

    print(f"Created: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python fill_template.py <template.dotx> <output.docx> '<json>'")
        sys.exit(1)

    template = sys.argv[1]
    output = sys.argv[2]
    replacements = json.loads(sys.argv[3])

    fill_template(template, output, replacements)
