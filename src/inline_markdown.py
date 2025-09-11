from src.textnode import TextNode, TextType
from src.HTMLNode import LeafNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        matches = list(
            re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", old_node.text)
        )
        last_index = 0

        if not matches:
            # No links found -> keep text as is
            new_nodes.append(old_node)
            continue

        for match in matches:
            # Preceding plain text
            if match.start() > last_index:
                plain_text = text[last_index:match.start()]
                if plain_text:
                    new_nodes.append(TextNode(plain_text, TextType.TEXT))

            # Link
            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, TextType.IMAGE, url))

            last_index = match.end()

        # Trailing plain text
        if last_index < len(text):
            trailing_text = text[last_index:]
            if trailing_text:
                new_nodes.append(TextNode(trailing_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        matches = list(
            re.finditer(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
        )
        last_index = 0

        if not matches:
            # No links found -> keep text as is
            new_nodes.append(old_node)
            continue

        for match in matches:
            # Preceding plain text
            if match.start() > last_index:
                plain_text = text[last_index:match.start()]
                if plain_text:
                    new_nodes.append(TextNode(plain_text, TextType.TEXT))

            # Link
            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            last_index = match.end()

        # Trailing plain text
        if last_index < len(text):
            trailing_text = text[last_index:]
            if trailing_text:
                new_nodes.append(TextNode(trailing_text, TextType.TEXT))
    return new_nodes



def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes