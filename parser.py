from flask import request
from sqlalchemy import or_
from models import *

def parse_search_query(q):
    q = q.strip()

    if q.startswith("/t "):
        raw = q[3:]
        values = []
        
        for v in raw.split(","):
                cleaned = v.strip()
                if cleaned:
                        values.append(cleaned.lower())
        return ("tag", values)

    elif q.startswith("/c "):
        return ("content", q[3:])
    elif q.startswith("/n "):
        return ("title", q[3:])
    else:
        return ("all", q)

def apply_tag_filter(query, tags):
        return query.join(Note.tags).filter(
                Tag.name.in_(tags)
        )