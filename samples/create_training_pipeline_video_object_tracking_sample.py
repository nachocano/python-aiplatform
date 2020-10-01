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

# [START aiplatform_create_training_pipeline_video_object_tracking_sample]
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def create_training_pipeline_video_object_tracking_sample(
    display_name: str, dataset_id: str, model_display_name: str, project: str
):
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.PipelineServiceClient(client_options=client_options)
    location = "us-central1"
    parent = "projects/{project}/locations/{location}".format(
        project=project, location=location
    )
    training_task_inputs_dict = {"modelType": "CLOUD"}
    training_task_inputs = json_format.ParseDict(training_task_inputs_dict, Value())

    training_pipeline = {
        "display_name": display_name,
        "training_task_definition": "gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_video_object_tracking_1.0.0.yaml",
        "training_task_inputs": training_task_inputs,
        "input_data_config": {"dataset_id": dataset_id},
        "model_to_upload": {"display_name": model_display_name},
    }
    response = client.create_training_pipeline(
        parent=parent, training_pipeline=training_pipeline
    )
    print("response")
    print(" name:", response.name)
    print(" display_name:", response.display_name)
    print(" training_task_definition:", response.training_task_definition)
    print(
        " training_task_inputs:",
        json_format.MessageToDict(response._pb.training_task_inputs),
    )
    print(
        " training_task_metadata:",
        json_format.MessageToDict(response._pb.training_task_metadata),
    )
    print(" state:", response.state)
    print(" start_time:", response.start_time)
    print(" end_time:", response.end_time)
    print(" labels:", response.labels)
    input_data_config = response.input_data_config
    model_to_upload = response.model_to_upload
    error = response.error


# [END aiplatform_create_training_pipeline_video_object_tracking_sample]
