from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import CustomerProject, ReplaceCustomerProjects


class CustomerProjects(BaseResource):
    """Projects linked to a customer. The public portal offers the intake-enabled ones."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, customer_id: str) -> list[CustomerProject]:
        """List the projects linked to a customer."""
        response = self._get(f"{workspace_slug}/customers/{customer_id}/projects")
        return [CustomerProject.model_validate(item) for item in response]

    def replace(
        self,
        workspace_slug: str,
        customer_id: str,
        data: ReplaceCustomerProjects,
    ) -> list[CustomerProject]:
        """Replace the full set of projects linked to a customer."""
        response = self._post(
            f"{workspace_slug}/customers/{customer_id}/projects",
            data.model_dump(exclude_none=True),
        )
        return [CustomerProject.model_validate(item) for item in response]
