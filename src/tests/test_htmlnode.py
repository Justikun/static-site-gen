import unittest

from src.HTMLNode import HTMLNode

class test_htmlnode(unittest.TestCase):

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
