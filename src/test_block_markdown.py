import unittest

from markdown_conversion import markdown_to_block, block_to_block_type, BlockType

class TestMDToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        text = "This is a normal paragraph"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading1(self):
        text = "# heading 1"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading2(self):
        text = "## heading 1"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading6(self):
        text = "###### heading 6"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_ordered(self):
        text = "1. item tems item\n2. asdl"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_unordered(self):
        text = "- unordered. - unordered 2"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
