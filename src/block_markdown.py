from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    """
    :param markdown_block: string
    :return: BlockType
    """

    # single line block
    print(block)
    if block[:2] == '# ':
        return BlockType.HEADING
    if block[:3] == '## ':
        return BlockType.HEADING
    if block[:4] == '### ':
        return BlockType.HEADING
    if block[:5] == '#### ':
        return BlockType.HEADING
    if block[:6] == '##### ':
        return BlockType.HEADING
    if block[:7] == '###### ':
        return BlockType.HEADING
    if block[:3] and block[len(block)-3:] == '```':
        return BlockType.CODE

    # multiline line block
    if block[:2] == "- ":
        blocks = block.split("\n")
        for block in blocks:
            if block[:2] == "- ":
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[:2] == "> ":
        blocks = block.split("\n")
        for block in blocks:
            if block[:2] == "> ":
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    pattern = r"\d+\.\s.*"
    match = re.search(pattern, block)
    if match:
        blocks = block.split("\n")
        for block in blocks:
            re.search(pattern, block)
            if match:
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH



def markdown_to_block(markdown):
    """
    :param markdown: string representing an entire markdown segment
    :return: a list of 'block' string([string])
    """
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == '':
            continue
        block = block.strip(" ")
        block = block.strip("\n")
        new_blocks.append(block)
    return new_blocks


def main():
    md = """
#This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

    blocks = markdown_to_block(md)

    text = "2. this is heading text"
    print(block_to_block_type(text))

if __name__ == "__main__":
    main()
