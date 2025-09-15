from textnode import TextNode, TextType
from HTMLNode import HTMLNode, LeafNode

def main():
    node = TextNode("Hello", TextType.LINK,"https://example.com")
    htmlNode = HTMLNode("p", "paragraph text value", props={"href": "https://example.com"})


main()