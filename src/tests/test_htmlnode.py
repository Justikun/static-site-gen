import unittest

from src.HTMLNode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode("p", "This is a node with props", props={"href": "https://example.com"})
        self.assertEqual(node.props, {"href": "https://example.com"})

    def test_props2_to_html(self):
        node = HTMLNode("p",
                        "This is a node with props",
                        props={
                            "href": "https://example.com",
                            "target": "_blank"},
                        )
        self.assertEqual(node.props, {"href": "https://example.com", "target": "_blank"})

    def test_defaults_are_empty(self):
        node = HTMLNode()
        assert node.tag is None
        assert node.value is None
        assert node.children == []
        assert node.props == {}


class TestLeafNodeHTML(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_to_html_no_val(self):
        with self.assertRaises(ValueError):
            LeafNode("body", None).to_html()

    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()