# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Record response serializers."""

import json

from flask_resources.serializers import JSONSerializer

from invenio_rdm_records.vocabularies import Vocabularies


class UIJSONSerializer(JSONSerializer):
    """UI JSON serializer implementation."""

    def _serialize_access_right(self, obj):
        """Inject ui config for `access_right` field."""
        access_right_vocabulary = self._serialize_ui_options_from_vocabulary(
            "access_right")
        category_value = obj["access"]["access_right"]
        return dict(
            access_right=dict(
                category=category_value,
                icon=access_right_vocabulary[category_value]['icon']
            ))

    def _serialize_ui_options_from_vocabulary(
            self, vocabulary_name):
        """Creates a flattened dictionary with the vocabulary data.

        :params vocabulary_name: name of the vocabulary to be used
        """
        flattened_vocabulary = {}
        vocabulary = Vocabularies.get_vocabulary(
            vocabulary_name).dump_options()
        if type(vocabulary) is dict:
            flattened_vocabulary = {}
            for key in vocabulary.keys():
                for option in vocabulary[key]:
                    flattened_vocabulary[option['value']] = option

        else:
            for option in vocabulary:
                flattened_vocabulary[option['value']] = option
        return flattened_vocabulary

    def _add_bucket_labels(self, agg_obj, vocabulary):
        """Inject labels in the aggregation buckets.

        :params agg_obj: Current aggregation object.
        :params vocabulary: Dict with vocabulary data.
        """
        buckets = agg_obj['buckets']
        for bucket in buckets:
            bucket['label'] = str(vocabulary.get(bucket['key'])['text'])
            for key in bucket:
                if isinstance(bucket[key], dict) and 'buckets' in bucket[key]:
                    sub_bucket = bucket[key]
                    self._add_bucket_labels(sub_bucket, vocabulary)

    def _serialize_aggregations(self, obj_list):
        """Inject ui config in aggregations."""
        aggregations = obj_list.get("aggregations")
        if aggregations:
            for aggregation_key in aggregations:
                agg_vocabulary = self._serialize_ui_options_from_vocabulary(
                    aggregation_key)
                if not agg_vocabulary:
                    continue
                self._add_bucket_labels(
                    aggregations[aggregation_key], agg_vocabulary)

    def serialize_obj_ui(self, obj):
        """Dump ui config for object."""
        obj.setdefault('ui', {}).update(self._serialize_access_right(obj))

    def serialize_object(self, obj, response_ctx=None, *args, **kwargs):
        """Dump the object into a json string."""
        self.serialize_obj_ui(obj)
        return json.dumps(obj)

    def serialize_object_list(
            self, obj_list, response_ctx=None, *args, **kwargs):
        """Dump the object list into a json string."""
        self._serialize_aggregations(obj_list)
        for obj in obj_list["hits"]["hits"]:
            self.serialize_obj_ui(obj)
        return json.dumps(obj_list)
