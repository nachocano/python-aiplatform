# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from uuid import uuid4
import pytest
import os

from samples import (
    create_training_pipeline_image_classification_sample,
    cancel_training_pipeline_sample,
    delete_training_pipeline_sample,
)

PROJECT_ID = os.getenv("BUILD_SPECIFIC_GCLOUD_PROJECT")
DATASET_ID = "1084241610289446912"  # Permanent 50 Flowers Dataset
DISPLAY_NAME = f"temp_create_training_pipeline_image_classification_test_{uuid4()}"


@pytest.fixture
def shared_state():
    state = {}
    yield state


@pytest.fixture(scope="function", autouse=True)
def teardown(shared_state):
    yield

    training_pipeline_id = shared_state["training_pipeline_name"].split("/")[-1]

    # Stop the training pipeline
    cancel_training_pipeline_sample.cancel_training_pipeline_sample(
        project=PROJECT_ID, training_pipeline_id=training_pipeline_id
    )

    # Delete the training pipeline
    delete_training_pipeline_sample.delete_training_pipeline_sample(
        project=PROJECT_ID, training_pipeline_id=training_pipeline_id
    )


def test_ucaip_generated_create_training_pipeline_video_classification_sample(
    capsys, shared_state
):

    create_training_pipeline_image_classification_sample.create_training_pipeline_image_classification_sample(
        project=PROJECT_ID,
        display_name=DISPLAY_NAME,
        dataset_id=DATASET_ID,
        model_display_name=f"Temp Model for {DISPLAY_NAME}",
    )

    out, _ = capsys.readouterr()

    # Save resource name of the newly created training pipeline
    shared_state["training_pipeline_name"] = out.split("name:")[1].split("\n")[0]
