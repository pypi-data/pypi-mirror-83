#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
from deprecated import deprecated
from dli.client.components.urls import dataset_urls
from dli.client.model_descriptor import ModelDescriptor
from dli.models.structured_dataset_model import StructuredDatasetModel
from dli.models.unstructured_dataset_model import UnstructuredDatasetModel


class DatasetFactory:

    @classmethod
    @deprecated
    def _from_v1_response_to_v2(cls, v1_response):
        response = cls._client.session.get(
            dataset_urls.v2_by_id.format(
                id=v1_response['properties']['datasetId']
            )
        )

        return cls._from_v2_response(response.json())

    @classmethod
    def _from_v2_response(cls, response_json):
        return cls._construct_dataset_using(
            response_json['data']['attributes'], response_json['data']['id']
        )

    @classmethod
    def _from_v2_response_unsheathed(cls, response_json):
        return cls._construct_dataset_using(
            response_json['attributes'], response_json['id']
        )

    @classmethod
    def _from_v2_list_response(cls, response_json):
        return [
            cls._construct_dataset_using(
                dataset['attributes'], dataset['id']
            )
            for dataset in response_json['data']
        ]

    @classmethod
    def _construct_dataset_using(cls, attributes, dataset_id):
        location = attributes.pop('location')
        # In the interests of not breaking backwards compatability.
        # TODO find a way to migrate this to the new nested API.
        if not location:
            location = None
        else:
            location = location[next(iter(location))]

        # ca depend
        if attributes["content_type"] == "Unstructured":
            return cls._client.Unstructured(
                **attributes,
                location=location,
                dataset_id=dataset_id
            )
        else:
            return cls._client.Structured(
                **attributes,
                location=location,
                dataset_id=dataset_id
            )
