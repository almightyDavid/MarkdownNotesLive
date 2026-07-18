from models import db, Tag

def parse_tags(tag_string):
    names = [t.strip().lower() for t in tag_string.split(",") if t.strip()]
    tags = []

    for name in set(names):
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)

    return tags