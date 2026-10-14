from unittest.mock import MagicMock

from plane import PlaneClient
from plane.models.work_items import (
    PaginatedWorkspaceSubscriptionResponse,
    SubscriptionBulkDelete,
    WorkItemSubscriber,
)

PAGE = {
    "grouped_by": None,
    "sub_grouped_by": None,
    "total_count": 1,
    "next_cursor": "",
    "prev_cursor": "",
    "next_page_results": False,
    "prev_page_results": False,
    "count": 1,
    "total_pages": 1,
    "total_results": 1,
    "extra_stats": None,
}


def _client() -> PlaneClient:
    return PlaneClient(api_key="test", base_url="https://plane.example")


def _json(status: int, body: dict) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.content = b"{}"
    response.headers = {"content-type": "application/json"}
    response.json.return_value = body
    return response


def test_subscriber_response_keeps_the_member():
    row = WorkItemSubscriber.model_validate(
        {
            "id": "sub-1",
            "created_at": "2026-10-14T10:00:00Z",
            "subscriber": {"id": "user-1", "display_name": "Diego"},
        }
    )

    assert row.subscriber is not None
    assert row.subscriber.display_name == "Diego"


def test_workspace_subscription_names_the_work_item():
    page = PaginatedWorkspaceSubscriptionResponse.model_validate(
        {
            **PAGE,
            "results": [
                {
                    "id": "sub-1",
                    "project": "project-1",
                    "subscriber": {"id": "user-1"},
                    "issue": {
                        "id": "item-1",
                        "name": "Login",
                        "sequence_id": 12,
                        "project_id": "project-1",
                    },
                }
            ],
        }
    )

    assert page.results[0].issue.sequence_id == 12
    assert SubscriptionBulkDelete.model_validate({"deleted": 4}).deleted == 4


def test_create_posts_the_work_item_subscribers_path():
    client = _client()
    client.work_items.subscribers.session.post = MagicMock(
        return_value=_json(
            201,
            {"id": "sub-1", "subscriber": {"id": "user-1"}, "created_at": "2026-10-14T10:00:00Z"},
        )
    )

    created = client.work_items.subscribers.create(
        "rodium", "project-1", "item-1", subscriber="user-2"
    )

    call = client.work_items.subscribers.session.post.call_args
    assert call.args[0].endswith(
        "/api/v1/workspaces/rodium/projects/project-1/work-items/item-1/subscribers/"
    )
    assert call.kwargs["json"] == {"subscriber": "user-2"}
    assert created.id == "sub-1"


def test_create_omits_the_subscriber_when_it_is_the_api_key_user():
    client = _client()
    client.work_items.subscribers.session.post = MagicMock(
        return_value=_json(200, {"id": "sub-1", "subscriber": {"id": "user-1"}})
    )

    client.work_items.subscribers.create("rodium", "project-1", "item-1")

    assert client.work_items.subscribers.session.post.call_args.kwargs["json"] == {}


def test_delete_sends_the_subscriber_query():
    client = _client()
    response = MagicMock()
    response.status_code = 204
    response.content = b""
    client.work_items.subscribers.session.delete = MagicMock(return_value=response)

    client.work_items.subscribers.delete("rodium", "project-1", "item-1", subscriber="me")

    call = client.work_items.subscribers.session.delete.call_args
    assert call.args[0].endswith(
        "/api/v1/workspaces/rodium/projects/project-1/work-items/item-1/subscribers/"
    )
    assert call.kwargs["params"] == {"subscriber": "me"}


def test_bulk_delete_returns_the_removed_count():
    client = _client()
    client.subscriptions.session.delete = MagicMock(return_value=_json(200, {"deleted": 3}))

    removed = client.subscriptions.delete(
        "rodium", params={"subscriber": "me", "project_id": "project-1"}
    )

    call = client.subscriptions.session.delete.call_args
    assert call.args[0].endswith("/api/v1/workspaces/rodium/subscriptions/")
    assert call.kwargs["params"] == {"subscriber": "me", "project_id": "project-1"}
    assert removed.deleted == 3
