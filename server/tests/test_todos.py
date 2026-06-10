"""
Tests for the Todo resource — CRUD operations.

Uses the conftest fixtures for in-memory SQLite, FakeRedis, and a pre-registered
test user with an active token.
"""

import pytest
from jsalchemy_api.exceptions import RecordNotFound


class TestTodoCreate:
    """POST a new Todo record."""

    @pytest.mark.asyncio
    async def test_good_path(self, rm, test_user):
        result = await rm.action(test_user["token"], "todo", "post", title="Buy milk")
        new_todos = result.get("new", {}).get("Todo", [])
        assert len(new_todos) == 1
        todo = new_todos[0]
        assert todo["title"] == "Buy milk"
        assert todo["completed"] is False
        assert "id" in todo

    @pytest.mark.asyncio
    async def test_create_multiple(self, rm, test_user):
        await rm.action(test_user["token"], "todo", "post", title="First")
        await rm.action(test_user["token"], "todo", "post", title="Second")
        r = await rm.action(test_user["token"], "todo", "query")
        assert r["payload"]["totalCount"] == 2, f"Expected 2, got {r}"


class TestTodoRead:
    """GET existing Todo records."""

    @pytest.mark.asyncio
    async def test_get_by_pk(self, rm, test_user):
        created = await rm.action(test_user["token"], "todo", "post", title="Read me")
        todo_id = str(created["new"]["Todo"][0]["id"])
        result = await rm.action(test_user["token"], "todo", "get", pks=[todo_id])
        read_data = result.get("read", {}).get("Todo", [])
        assert len(read_data) == 1
        assert read_data[0]["title"] == "Read me"

    @pytest.mark.asyncio
    async def test_get_not_found_returns_empty(self, rm, test_user):
        """GET for a non-existent PK returns an empty list (not an error)."""
        result = await rm.action(test_user["token"], "todo", "get", pks=["99999"])
        read_data = result.get("read", {}).get("Todo", [])
        assert read_data == []

    @pytest.mark.asyncio
    async def test_query_by_filter(self, rm, test_user):
        await rm.action(test_user["token"], "todo", "post", title="Done!", completed=True)
        await rm.action(test_user["token"], "todo", "post", title="Still pending")
        r = await rm.action(test_user["token"], "todo", "query", filter={"completed": True})
        assert r["payload"]["totalCount"] == 1, f"Expected 1, got {r}"
        assert len(r["payload"]["pks"]) == 1


class TestTodoUpdate:
    """PUT to update an existing Todo record."""

    @pytest.mark.asyncio
    async def test_good_path(self, rm, test_user):
        created = await rm.action(test_user["token"], "todo", "post", title="Old title")
        todo_id = str(created["new"]["Todo"][0]["id"])
        await rm.action(test_user["token"], "todo", "put", id=todo_id, title="New title")
        result = await rm.action(test_user["token"], "todo", "get", pks=[todo_id])
        read_data = result.get("read", {}).get("Todo", [])
        assert read_data[0]["title"] == "New title"

    @pytest.mark.asyncio
    async def test_update_nonexistent_raises(self, rm, test_user):
        with pytest.raises(RecordNotFound):
            await rm.action(test_user["token"], "todo", "put", id="-1", title="Nope")


class TestTodoDelete:
    """DELETE a Todo record."""

    @pytest.mark.asyncio
    async def test_good_path(self, rm, test_user):
        created = await rm.action(test_user["token"], "todo", "post", title="Delete me")
        todo_id = str(created["new"]["Todo"][0]["id"])
        await rm.action(test_user["token"], "todo", "delete", pks=[todo_id])
        result = await rm.action(test_user["token"], "todo", "get", pks=[todo_id])
        read_data = result.get("read", {}).get("Todo", [])
        assert read_data == []

    @pytest.mark.asyncio
    async def test_delete_nonexistent_raises(self, rm, test_user):
        with pytest.raises(RecordNotFound):
            await rm.action(test_user["token"], "todo", "delete", pks=["99999"])

    @pytest.mark.asyncio
    async def test_delete_all(self, rm, test_user):
        await rm.action(test_user["token"], "todo", "post", title="A")
        await rm.action(test_user["token"], "todo", "post", title="B")
        await rm.action(test_user["token"], "todo", "delete_all")
        r = await rm.action(test_user["token"], "todo", "query")
        assert r["payload"]["totalCount"] == 0, f"Expected 0, got {r}"