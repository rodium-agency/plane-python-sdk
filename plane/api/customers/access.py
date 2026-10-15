from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import Customer, CustomerAccessUpdate


class CustomerAccess(BaseResource):
    """Portal access key and revocation for a customer."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def regenerate_key(self, workspace_slug: str, customer_id: str) -> Customer:
        """Issue a new portal access key. The previous key stops working.

        The new key is returned once, on `access_key`.
        """
        response = self._post(f"{workspace_slug}/customers/{customer_id}/access-key", {})
        return Customer.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        customer_id: str,
        data: CustomerAccessUpdate,
    ) -> Customer:
        """Revoke, restore, or set the expiry of the customer's public portal."""
        response = self._patch(
            f"{workspace_slug}/customers/{customer_id}/access",
            data.model_dump(exclude_none=True),
        )
        return Customer.model_validate(response)
