"""Modification of the Sphinx HTML5 translator with better handling of permalinks.

Instead of "permalink to this headline",
this returns "Copy link to section: *sectionname*".
Clicking on the permalink anchor will copy the link to the clipboard.
This is implemented in JavaScript.

:copyright: Copyright Kai Welke.
:license: MIT, see LICENSE for details.
"""
from typing import Any, Dict

from docutils import nodes
from docutils.nodes import Element, Text
from sphinx.application import Sphinx
from sphinx.locale import _
from sphinx.util import logging
from sphinx.writers.html5 import HTML5Translator

from . import __version__

logger = logging.getLogger(__name__)

# icons are from Material Design icon set
ICONS = {
    # https://material.io/resources/icons/?icon=content_copy
    "copy": (
        "<svg xmlns='http://www.w3.org/2000/xvg' viewBox='0 0 24 24' "
        "fill=currentColor aria-hidden='true'>"
        "<path d='M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 "
        "4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 "
        "0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z' /></svg>"
    ),
    # https://material.io/resources/icons/?icon=link
    "headerlink": (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'pointer-events="none" viewBox="0 0 24 24">'
        '<path d="M3.9 12c0-1.71 1.39-3.1 '
        "3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 "
        "5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 "
        "13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 "
        "3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 "
        '5-5s-2.24-5-5-5z"/></svg>'
    ),
    # https://material.io/resources/icons/?icon=open_in_new
    "external_link": (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 24 24" class="external-link-icon" aria-hidden="true">'
        '<path d="M19 19H5V5h7V3H5a2 2 0 00-2 2v14a2 2 0 '
        "002 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 "
        '3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z"/></svg>'
    ),
}

COPY_BUTTON = (
    "<button class='copy tooltipped tooltipped-nw' aria-label='Copy this code'>"
    + ICONS["copy"]
    + "</button>\n"
)


class AwesomeHTMLTranslator(HTML5Translator):
    """Override a few methods to improve the usability.

    By default, Sphinx permalinks have generic titles,
    such as: "Permalink to this section".
    In the sphinx awesome theme, clicking on a permalink
    copies the link to the clipboard. Therefore,
    the link title attributes are updated to be more
    specific.
    """

    def depart_title(self, node: Element) -> None:
        """Change the permalinks for headlines.

        - for headlines: "Copy link to section: <section title>"
        - for tables: "Copy link to this table"
        - for admonitions: "Copy link to this <type>"

        Admonitions don't have an ID by default.
        The AdmonitionID post-transform adds
        IDs to admonitions.
        """
        close_tag = self.context[-1]
        if (
            self.permalink_text
            and self.builder.add_permalinks
            and node.parent.hasattr("ids")
            and node.parent["ids"]
        ):
            # add permalink anchor
            if close_tag.startswith("</h"):
                self.add_permalink_ref(
                    node.parent, _(f"Copy link to section: {node.astext()}.")
                )
            elif isinstance(node.parent, nodes.table):
                self.body.append("</span>")
                self.add_permalink_ref(node.parent, _("Copy link to this table."))
            elif isinstance(node.parent, nodes.Admonition):
                admon_type = type(node.parent).__name__
                self.add_permalink_ref(
                    node.parent, _(f"Copy link to this {admon_type}.")
                )
        elif isinstance(node.parent, nodes.table):
            self.body.append("</span>")

        self.body.append(self.context.pop())
        if self.in_document_title:  # type: ignore
            self.title = self.body[self.in_document_title : -1]  # type: ignore
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]

    def add_permalink_ref(self, node: Element, title: str) -> None:
        """Add an icon instead of the ¶ symbol.

        Note that user-defined permalink characters specified via
        `html_add_permalinks` are ignored.

        Since clicking the permalink icon copies the link to the clipboard,
        this should be a button element, but there is some magic with the
        resolution of `href` attributes happening in Sphinx.
        """
        if node["ids"] and self.builder.add_permalinks and self.permalink_text:
            headerlink = (
                '<a role="button" class="headerlink tooltipped tooltipped-ne" '
                'href="#{}" aria-label="{}">'.format(node["ids"][0], title)
            )
            headerlink += ICONS["headerlink"] + "</a>"
            self.body.append(headerlink)

    def visit_caption(self, node: Element) -> None:
        """Use semantic elements."""
        if isinstance(node.parent, nodes.figure):
            self.body.append("<figcaption>")
            self.add_fignumber(node.parent)
            self.body.append(self.starttag(node, "span", "", CLASS="caption-text"))
        elif isinstance(node.parent, nodes.container) and node.parent.get(
            "literal_block"
        ):
            self.body.append(self.starttag(node, "span", ""))
            self.body.append(self.starttag(node, "span", "", CLASS="caption-text"))
        else:
            self.body.append(self.starttag(node, "p", "", CLASS="caption"))

    def depart_caption(self, node: Element) -> None:
        """Change the permalinks for captions.

        - for code blocks: Copy link to this code block
        - for images: Copy link to this image
        - for table of contents: Copy link to this table of contents.
        """
        self.body.append("</span>")

        # append permalink if available
        if isinstance(node.parent, nodes.container) and node.parent.get(
            "literal_block"
        ):
            self.add_permalink_ref(node.parent, _("Copy link to this code block."))
            self.body.append("</span>")
        if isinstance(node.parent, nodes.figure):
            self.add_permalink_ref(node.parent, _("Copy link to this image."))
        elif node.parent.get("toctree"):
            self.add_permalink_ref(
                node.parent.parent, _("Copy link to this table of contents.")
            )

        if isinstance(node.parent, nodes.container) and node.parent.get(
            "literal_block"
        ):
            self.body.append(COPY_BUTTON)
            self.body.append("</div>\n")
        elif isinstance(node.parent, nodes.figure):
            self.body.append("</figcaption>\n")
        else:
            self.body.append("</p>\n")

    def depart_desc_signature(self, node: Element) -> None:
        """Change permalinks for code definitions.

        Functions, methods, command line options, etc.
        "Copy link to this definition"
        """
        if not node.get("is_multiline"):
            self.add_permalink_ref(node, _("Copy link to this definition."))
        self.body.append("</dt>\n")

    def depart_desc_signature_line(self, node: Element) -> None:
        """Change permalinks for code definitions."""
        if node.get("add_permalink"):
            self.add_permalink_ref(node.parent, _("Copy link to this definition."))
        self.body.append("<br />")

    def visit_section(self, node: Element) -> None:
        """Use semantic <section> elements."""
        self.section_level += 1
        self.body.append(self.starttag(node, "section"))

    def depart_section(self, node: Element) -> None:
        """Use semantic <section> elements."""
        self.section_level -= 1
        self.body.append("</section>\n")

    def visit_figure(self, node: Element) -> None:
        """Use semantic <figure> elements."""
        attributes = {}
        if node.get("width"):
            attributes["style"] = f"width:{node['width']}"
        if node.get("align"):
            attributes["class"] = f"align-{node['align']}"
        self.body.append(self.starttag(node, "figure", **attributes))

    def depart_figure(self, node: Element) -> None:
        """Use semantic <figure> elements."""
        self.body.append("</figure>\n")

    def visit_literal_block(self, node: Element) -> None:
        """Don't wrap highlighted blocks any further."""
        if node.rawsource != node.astext():
            # most probably a parsed-literal block -- don't highlight
            return super().visit_literal_block(node)

        lang = node.get("language", "default")
        linenos = node.get("linenos", False)
        highlight_args = node.get("highlight_args", {})
        highlight_args["force"] = node.get("force", False)
        if lang is self.builder.config.highlight_language:
            # only pass highlighter options for original language
            opts = self.builder.config.highlight_options
        else:
            opts = {}

        if linenos and self.builder.config.html_codeblock_linenos_style:
            linenos = "inline"

        highlighted = self.highlighter.highlight_block(
            node.rawsource,
            lang,
            opts=opts,
            linenos=linenos,
            location=node,
            **highlight_args,
        )

        # if the node is not child of a container.literal_block node
        if not (
            isinstance(node.parent, nodes.container)
            and node.parent.get("literal_block")
        ):

            self.body.append(self.starttag(node, "div", CLASS="highlight"))

            code_header = "<div class='code-header'>\n"
            code_header += (
                f"<span class='code-lang'>{lang.replace('default', 'python')}</span>\n"
            )
            code_header += COPY_BUTTON
            code_header += "</div>\n"
            self.body.append(code_header)

        # wrap the highlighted string in a div
        self.body.append(highlighted)

        if not (
            isinstance(node.parent, nodes.container)
            and node.parent.get("literal_block")
        ):
            self.body.append("</div>\n")
        raise nodes.SkipNode

    def visit_literal(self, node: Element) -> None:
        """Simplify inline code elements."""
        if "kbd" in node["classes"]:
            self.body.append(self.starttag(node, "kbd"))
        else:
            self.body.append(self.starttag(node, "code"))

        self.protect_literal_text += 1

    def depart_literal(self, node: Element) -> None:
        """Simplify inline code elements."""
        if "kbd" in node["classes"]:
            self.body.append("</kbd>")
        else:
            self.body.append("</code>")

    def visit_Text(self, node: Text) -> None:
        """Simplify inline code elements."""
        text = node.astext()
        encoded = self.encode(text)

        if self.protect_literal_text:
            for token in self.words_and_spaces.findall(encoded):
                if token.strip() or token in " \n":  # noqa: S105
                    self.body.append(token)
                else:
                    self.body.append("&#160;" * (len(token) - 1) + " ")
        else:
            if self.in_mailto and self.settings.cloak_email_addresses:
                encoded = self.cloak_email(encoded)
            self.body.append(encoded)

    def visit_container(self, node: Element) -> None:
        """Overide for code blocks with captions."""
        self.body.append(self.starttag(node, "div", CLASS="highlight"))
        if node.get("literal_block"):
            lang = node.get("language")
            code_header = "<div class='code-header'>\n"
            code_header += (
                f"<span class='code-lang'>{lang.replace('default', 'python')}</span>\n"
            )
            self.body.append(code_header)

    def depart_reference(self, node: Element) -> None:
        """Add external link icon."""
        if "refuri" in node and not node.get("internal"):
            self.body.append(ICONS["external_link"])
        super().depart_reference(node)


def setup(app: "Sphinx") -> Dict[str, Any]:
    """Use the AwesomeHTMLTranslator for the html and dirhtml builders.

    This function makes this available as extension.
    """
    app.set_translator("html", AwesomeHTMLTranslator)
    app.set_translator("dirhtml", AwesomeHTMLTranslator)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
