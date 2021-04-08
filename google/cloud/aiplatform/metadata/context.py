# -*- coding: utf-8 -*-

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import re
import logging
from typing import Optional, Dict

from google.api_core import exceptions
from google.cloud.aiplatform import utils
from google.auth import credentials as auth_credentials

from google.cloud.aiplatform import base, initializer
from google.cloud.aiplatform_v1beta1.types import context as gca_context

RESOURCE_NAME_PATTERN = re.compile(
    r"^projects\/(?P<project>[\w-]+)\/locations\/(?P<location>[\w-]+)\/metadataStores\/(?P<store>[\w-]+)\/contexts\/(?P<id>[\w-]+)$"
)


class _Context(base.AiPlatformResourceNounWithFutureManager):
    """Metadata Context resource for AI Platform"""

    client_class = utils.MetadataClientWithOverride
    _is_client_prediction_client = False
    _resource_noun = "contexts"
    _getter_method = "get_context"
    _delete_method = None

    def __init__(
        self,
        context_name: str,
        metadata_store_id: Optional[str] = "default",
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ):
        """Retrieves an existing Context given a Context name or ID.

        Args:
            context_name (str):
                A fully-qualified Context resource name or context ID
                Example: "projects/123/locations/us-central1/metadataStores/default/contexts/my-context".
                or "my-context" when project and location are initialized or passed.
            metadata_store_id (str):
                MetadataStore to retrieve resource from. If not set, metadata_store_id is set to "default".
                If context_name is a fully-qualified Context, its metadata_store_id overrides this one.
            project (str):
                Optional project to retrieve resource from. If not set, project
                set in aiplatform.init will be used.
            location (str):
                Optional location to retrieve resource from. If not set, location
                set in aiplatform.init will be used.
            credentials (auth_credentials.Credentials):
                Custom credentials to use to upload this model. Overrides
                credentials set in aiplatform.init.
        """

        super().__init__(
            project=project, location=location, credentials=credentials,
        )

        # If we receive a full resource name, we extract the metadata_store_id and use that
        if context_name.find("/") != -1:
            metadata_store_id = _Context._extract_metadata_store_id(context_name)

        resource_name = utils.full_resource_name(
            resource_name=context_name,
            resource_noun=f"metadataStores/{metadata_store_id}/{self._resource_noun}",
            project=self.project,
            location=self.location,
        )
        self._gca_resource = getattr(self.api_client, self._getter_method)(
            name=resource_name
        )

    @classmethod
    def create(
        cls,
        context_id: str,
        schema_title: str,
        display_name: Optional[str] = None,
        schema_version: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict] = {},
        metadata_store_id: str = "default",
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials: Optional[auth_credentials.Credentials] = None,
    ) -> "_Context":
        """Creates a new Context resource.

        Args:
            context_id (str):
                Required. The {context_id} portion of the resource name with
                the format:
                projects/{project}/locations/{location}/metadataStores/{metadata_store_id}/contexts/{context_id}.
            schema_title (str):
                Required. schema_title identifies the schema title used by the created context.
            display_name (str):
                Optional. The user-defined name of the context.
            schema_version (str):
                Optional. schema_version specifies the version used by the created context.
                If not set, defaults to use the latest version.
            description (str):
                Optional. Describes the purpose and content of the context resource to be created.
            metadata (Dict):
                Optional. metadata contains the metadata information that will be stored in the context resource.
            metadata_store_id (str):
                The {metadata_store_id} portion of the resource name with
                the format:
                projects/{project}/locations/{location}/metadataStores/{metadata_store_id}/contexts/{context_id}
                If not provided, the MetadataStore's ID will be set to "default".
            project (str):
                Project to create this context into. Overrides project set in
                aiplatform.init.
            location (str):
                Location to create this context into. Overrides location set in
                aiplatform.init.
            credentials (auth_credentials.Credentials):
                Custom credentials to use to create this context. Overrides
                credentials set in aiplatform.init.

        Returns:
            context (Context):
                Instantiated representation of the managed Metadata Context resource.

        """
        api_client = cls._instantiate_client(location=location, credentials=credentials)
        gapic_context = gca_context.Context(
            schema_title=schema_title,
            schema_version=schema_version,
            display_name=display_name,
            description=description,
            metadata=metadata,
        )

        parent = initializer.global_config.common_location_path(
            project=project, location=location
        )

        try:
            api_client.create_context(
                parent=parent + f"/metadataStores/{metadata_store_id}",
                context=gapic_context,
                context_id=context_id,
            )
        except exceptions.AlreadyExists:
            logging.info(f"Context '{context_id}' already exist")

        return cls(
            context_name=parent
            + f"/metadataStores/{metadata_store_id}/{_Context._resource_noun}/{context_id}",
            metadata_store_id={metadata_store_id},
            project=project,
            location=location,
            credentials=credentials,
        )

    @classmethod
    def _extract_metadata_store_id(cls, resource_name) -> str:
        """Extracts the metadata store id from the resource name.

        Args:
            resource_name (str):
                Required. A fully-qualified metadata resource name. For example
                projects/{project}/locations/{location}/metadataStores/{metadata_store_id}/contexts/{context_id}.
        Returns:
            metadata_store_id (str):
                The metadata store id for the particular resource name.
        Raises:
            ValueError if it does not exist.
        """
        match = RESOURCE_NAME_PATTERN.match(resource_name)
        if not match:
            raise ValueError(
                f"failed to extract metadata_store_id from resource {resource_name}"
            )
        return match["store"]
