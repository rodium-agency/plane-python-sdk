from collections.abc import Mapping
from typing import Any

from ..models.work_items import PaginatedWorkspaceSubscriptionResponse, SubscriptionBulkDelete
from .base_resource import BaseResource


class Subscriptions(BaseResource):
    """A user's work item subscriptions across a workspace."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedWorkspaceSubscriptionResponse:
        """List subscriptions in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            params: ``subscriber``, ``project_id``, ``cursor`` and ``per_page``.
                ``subscriber`` defaults to the authenticated user. Pass ``me`` or a user id.
        """
        response = self._get(f"{workspace_slug}/subscriptions", params=params)
        return PaginatedWorkspaceSubscriptionResponse.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        params: Mapping[str, Any] | None = None,
    ) -> SubscriptionBulkDelete:
        """Unsubscribe every matching subscription and return how many were removed.

        ``BaseResource._delete`` drops a JSON body, and this endpoint answers ``200``
        with ``{"deleted": n}`` rather than ``204``. The response is read here so the
        count is not discarded.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (``subscriber``, ``project_id``).
        """
        url = self._build_url(f"{workspace_slug}/subscriptions")
        response = self.session.delete(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.config.timeout,
        )
        payload = self._handle_response(response)
        return SubscriptionBulkDelete.model_validate(payload)
