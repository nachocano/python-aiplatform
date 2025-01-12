# Copyright 2021 Google LLC
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


import create_training_pipeline_custom_training_managed_dataset_sample
import test_constants as constants


def test_create_training_pipeline_custom_job_sample(
    mock_sdk_init,
    mock_image_dataset,
    mock_init_custom_training_job,
    mock_run_custom_training_job,
    mock_get_image_dataset,
):

    create_training_pipeline_custom_training_managed_dataset_sample.create_training_pipeline_custom_training_managed_dataset_sample(
        project=constants.PROJECT,
        location=constants.LOCATION,
        display_name=constants.DISPLAY_NAME,
        args=constants.ARGS,
        script_path=constants.SCRIPT_PATH,
        container_uri=constants.CONTAINER_URI,
        model_serving_container_image_uri=constants.CONTAINER_URI,
        dataset_id=constants.RESOURCE_ID,
        model_display_name=constants.DISPLAY_NAME_2,
        replica_count=constants.REPLICA_COUNT,
        machine_type=constants.MACHINE_TYPE,
        accelerator_type=constants.ACCELERATOR_TYPE,
        accelerator_count=constants.ACCELERATOR_COUNT,
        training_fraction_split=constants.TRAINING_FRACTION_SPLIT,
        validation_fraction_split=constants.VALIDATION_FRACTION_SPLIT,
        test_fraction_split=constants.TEST_FRACTION_SPLIT,
    )

    mock_get_image_dataset.assert_called_once_with(constants.RESOURCE_ID)

    mock_sdk_init.assert_called_once_with(
        project=constants.PROJECT, location=constants.LOCATION
    )
    mock_init_custom_training_job.assert_called_once_with(
        display_name=constants.DISPLAY_NAME,
        script_path=constants.SCRIPT_PATH,
        container_uri=constants.CONTAINER_URI,
        model_serving_container_image_uri=constants.CONTAINER_URI,
    )
    mock_run_custom_training_job.assert_called_once_with(
        dataset=mock_image_dataset,
        model_display_name=constants.DISPLAY_NAME_2,
        args=constants.ARGS,
        replica_count=constants.REPLICA_COUNT,
        machine_type=constants.MACHINE_TYPE,
        accelerator_type=constants.ACCELERATOR_TYPE,
        accelerator_count=constants.ACCELERATOR_COUNT,
        training_fraction_split=constants.TRAINING_FRACTION_SPLIT,
        validation_fraction_split=constants.VALIDATION_FRACTION_SPLIT,
        test_fraction_split=constants.TEST_FRACTION_SPLIT,
        sync=True,
    )
