from database import db
from models import Task


# =========================
# TESTE 1 - to_dict()
# =========================
def test_task_to_dict():
    task = Task(
        title="Comprar leite",
        description="Ir ao mercado",
        status="pending"
    )

    result = task.to_dict()

    assert result["title"] == "Comprar leite"
    assert result["description"] == "Ir ao mercado"
    assert result["status"] == "pending"


# =========================
# TESTE 2 - default status
# =========================
def test_task_default_status(app):
    with app.app_context():
        task = Task(title="Nova tarefa")

        db.session.add(task)
        db.session.commit()

        assert task.status == "pending"


# =========================
# TESTE 3 - persistência no banco
# =========================
def test_task_persistence(app):
    with app.app_context():
        task = Task(title="Tarefa no banco")

        db.session.add(task)
        db.session.commit()

        assert task.id is not None

        saved = Task.query.get(task.id)

        assert saved is not None
        assert saved.title == "Tarefa no banco"
        assert saved.status == "pending"


# =========================
# TESTE 4 - update
# =========================
def test_task_update(app):
    with app.app_context():
        task = Task(title="Original")

        db.session.add(task)
        db.session.commit()

        task.title = "Atualizado"
        db.session.commit()

        updated = Task.query.get(task.id)

        assert updated.title == "Atualizado"


# =========================
# TESTE 5 - delete
# =========================
def test_task_delete(app):
    with app.app_context():
        task = Task(title="Para deletar")

        db.session.add(task)
        db.session.commit()

        task_id = task.id

        db.session.delete(task)
        db.session.commit()

        deleted = Task.query.get(task_id)

        assert deleted is None