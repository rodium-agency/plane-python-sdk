from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    CustomerAttachment,
    CustomerAttachmentUpload,
    CustomerAttachmentUploadResponse,
)


class CustomerAttachments(BaseResource):
    """Files attached to a customer record."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, customer_id: str) -> list[CustomerAttachment]:
        """List files attached to the customer record."""
        response = self._get(f"{workspace_slug}/customers/{customer_id}/attachments")
        return [CustomerAttachment.model_validate(item) for item in response]

    def create(
        self,
        workspace_slug: str,
        customer_id: str,
        data: CustomerAttachmentUpload,
    ) -> CustomerAttachmentUploadResponse:
        """Create a presigned upload for a file on the customer record."""
        response = self._post(
            f"{workspace_slug}/customers/{customer_id}/attachments",
            data.model_dump(exclude_none=True),
        )
        return CustomerAttachmentUploadResponse.model_validate(response)

    def complete(self, workspace_slug: str, customer_id: str, asset_id: str) -> None:
        """Mark a presigned customer attachment as uploaded."""
        self._patch(f"{workspace_slug}/customers/{customer_id}/attachments/{asset_id}", {})

    def delete(self, workspace_slug: str, customer_id: str, asset_id: str) -> None:
        """Delete a file from the customer record."""
        self._delete(f"{workspace_slug}/customers/{customer_id}/attachments/{asset_id}")
