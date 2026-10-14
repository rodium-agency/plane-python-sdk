from collections.abc import Mapping
from typing import Any

from ...models.work_items import PaginatedWorkItemSubscriberResponse, WorkItemSubscriber
from ..base_resource import BaseResource


class WorkItemSubscribers(BaseResource):
    """Subscribers of a single work item."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkItemSubscriberResponse:
        """List the active subscribers of a work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            params: Optional query parameters (``cursor``, ``per_page``)
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/subscribers",
            params=params,
        )
        return PaginatedWorkItemSubscriberResponse.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        subscriber: str | None = None,
    ) -> WorkItemSubscriber:
        """Subscribe a project member. Omit ``subscriber`` to subscribe the API key user.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            subscriber: User id to subscribe. Defaults to the authenticated user.
        """
        data: dict[str, Any] = {}
        if subscriber:
            data["subscriber"] = subscriber
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/subscribers",
            data,
        )
        return WorkItemSubscriber.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        subscriber: str | None = None,
    ) -> None:
        """Unsubscribe a project member. The opt-out survives later automatic subscriptions.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            subscriber: User id, or ``me``. Defaults to the authenticated user.
        """
        params = {"subscriber": subscriber} if subscriber else None
        self._delete(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}/subscribers",
            params=params,
        )
