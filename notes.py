from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from forms import NoteForm
from models import *
from parser import apply_tag_filter, parse_search_query
from services.tags import parse_tags
from utils import render_markdown

notes = Blueprint("notes", __name__)

@notes.route("/dashboard")
@login_required
def dashboard():
    notes = current_user.notes
    return render_template("dashboard.html", notes=notes)

@notes.route("/notes/export")
@login_required
def export_notes():
    user_notes = (
        Note.query
        .filter(Note.user_id == current_user.id)
        .order_by(Note.id.asc())
        .all()
    )

    archive = BytesIO()

    with ZipFile(
        archive,
        mode="w",
        compression=ZIP_DEFLATED,
    ) as zip_file:
        if not user_notes:
            zip_file.writestr(
                "README.txt",
                "This account does not contain any notes yet.\n",
            )

        for note in user_notes:
            safe_title = secure_filename(
                str(note.title or "")
            )

            if not safe_title:
                safe_title = "untitled-note"

            filename = f"{safe_title}-{note.id}.md"
            content = str(note.content or "")

            zip_file.writestr(
                filename,
                content.encode("utf-8"),
            )

    archive.seek(0)

    return send_file(
        archive,
        mimetype="application/zip",
        as_attachment=True,
        download_name="markdown-notes-backup.zip",
    )

@notes.route("/notes/search")
@login_required
def search_notes():
    q = request.args.get("q", "")
    mode, value = parse_search_query(q)

    query = Note.query.filter(Note.user_id == current_user.id)

    if mode == "tag":
        query = apply_tag_filter(query, value)
    elif mode == "content":
        query = query.filter(Note.content.contains(value))
    elif mode == "title":
        query = query.filter(Note.title.contains(value))
    else:
        query = query.filter(
            Note.title.contains(value) |
            Note.content.contains(value)
        )

    notes = query.all()

    return render_template("note_list.html", notes=notes)

@notes.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():
    form = NoteForm()

    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )

        note.tags = parse_tags(request.form.get("tags", ""))

        db.session.add(note)
        db.session.commit()
        return redirect(f"/notes/{note.id}")

    return render_template("note_form.html",
                           form=form,
                           header="New note",
                           button="Create")

@notes.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    form = NoteForm(obj=note)  # <-- pre-fill form from model

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.tags = parse_tags(request.form.get("tags",""))
        db.session.commit()
        return redirect(f"/notes/{note.id}")

    tags_string = ", ".join(t.name for t in note.tags)

    return render_template(
        "note_form.html",
        form=form,
        note=note,
        tags=tags_string,
        header="Edit note",
        button="Save"
    )

@notes.route("/notes/<int:note_id>/autosave", methods=["POST"])
@login_required
def autosave_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    db.session.commit()
    return jsonify({"status": "ok"})

@notes.route("/notes/<int:note_id>")
@login_required
def read_note(note_id):
    note = Note.query.filter_by(
            id=note_id,
            user_id=current_user.id
        ).first_or_404()

    rendered = render_markdown(note.content)

    return render_template("read_note.html",note=note, rendered=rendered)

@notes.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()
    return redirect("/dashboard")
