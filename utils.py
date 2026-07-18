import markdown
import bleach

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS | {
        "p", "pre", "code", "h1", "h2", "h3",
        "ul", "ol", "li", "strong", "em", "blockquote"
}

def render_markdown(text):
        html = markdown.markdown(
                text,
                extensions=["fenced_code", "codehilite"]
        )
        return bleach.clean(html, tags=ALLOWED_TAGS)