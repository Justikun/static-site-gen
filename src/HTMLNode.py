class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        :param tag: (str) The type of the node.
                e.g., html, div, p, h1
        :param value: (str) The value of the node.
                e.g., Text in a paragraph
        :param children: (list) The children of the node.
                e.g., List of HTMLNode
        :param props: (dict) The attributes of the node.
                e.g., <a> tag might have {"href": "https://example.com"}
        """
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        final_string = ""
        for key, value in self.props.items():
            final_string += f"{key}=\"{self.props[key]}\" "
        return final_string


