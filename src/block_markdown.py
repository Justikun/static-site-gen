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
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    markdown_to_block(md)




if __name__ == "__main__":
    main()

