from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of nodes based on a delimiter, creating new nodes with specified text

    :param old_nodes: List of nodes to split.
    :type old_nodes: list[TextNode]

    :param delimiter: The delimiter used to split the text
    :type delimiter: str

    :param text_type: The type assigned to the list of nodes
    :type text_type: TextType

    :return: A new list of nodes with text split into respective sections and types.
        Original nodes without text-based content are directly appended to the result.
    :type: list
    :raises ValueError: If the markdown-like formatted section in any node's text
        is not properly closed (i.e., if the number of splits by the delimiter is even).
    """
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


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
