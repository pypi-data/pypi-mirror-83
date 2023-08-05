#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from typing import Any, MutableMapping, Optional, Union, Collection
from .utils import NamespacedClient

class CatClient(NamespacedClient):
    def aliases(
        self,
        *,
        name: Optional[Any] = ...,
        expand_wildcards: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def allocation(
        self,
        *,
        node_id: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def count(
        self,
        *,
        index: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def health(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        ts: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def help(
        self,
        *,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        format: Optional[str] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def indices(
        self,
        *,
        index: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        expand_wildcards: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        health: Optional[Any] = ...,
        help: Optional[Any] = ...,
        include_unloaded_segments: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        pri: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def master(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def nodes(
        self,
        *,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        full_id: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def recovery(
        self,
        *,
        index: Optional[Any] = ...,
        active_only: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        detailed: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def shards(
        self,
        *,
        index: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def segments(
        self,
        *,
        index: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def pending_tasks(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def thread_pool(
        self,
        *,
        thread_pool_patterns: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        size: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def fielddata(
        self,
        *,
        fields: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def plugins(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def nodeattrs(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def repositories(
        self,
        *,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def snapshots(
        self,
        *,
        repository: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        ignore_unavailable: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def tasks(
        self,
        *,
        actions: Optional[Any] = ...,
        detailed: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        node_id: Optional[Any] = ...,
        parent_task: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def templates(
        self,
        *,
        name: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        local: Optional[Any] = ...,
        master_timeout: Optional[Any] = ...,
        s: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def ml_data_frame_analytics(
        self,
        *,
        id: Optional[Any] = ...,
        allow_no_match: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def ml_datafeeds(
        self,
        *,
        datafeed_id: Optional[Any] = ...,
        allow_no_datafeeds: Optional[Any] = ...,
        allow_no_match: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def ml_jobs(
        self,
        *,
        job_id: Optional[Any] = ...,
        allow_no_jobs: Optional[Any] = ...,
        allow_no_match: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def ml_trained_models(
        self,
        *,
        model_id: Optional[Any] = ...,
        allow_no_match: Optional[Any] = ...,
        bytes: Optional[Any] = ...,
        format: Optional[Any] = ...,
        from_: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        size: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
    def transforms(
        self,
        *,
        transform_id: Optional[Any] = ...,
        allow_no_match: Optional[Any] = ...,
        format: Optional[Any] = ...,
        from_: Optional[Any] = ...,
        h: Optional[Any] = ...,
        help: Optional[Any] = ...,
        s: Optional[Any] = ...,
        size: Optional[Any] = ...,
        time: Optional[Any] = ...,
        v: Optional[Any] = ...,
        pretty: Optional[bool] = ...,
        human: Optional[bool] = ...,
        error_trace: Optional[bool] = ...,
        filter_path: Optional[Union[str, Collection[str]]] = ...,
        request_timeout: Optional[Union[int, float]] = ...,
        ignore: Optional[Union[int, Collection[int]]] = ...,
        opaque_id: Optional[str] = ...,
        params: Optional[MutableMapping[str, Any]] = ...,
        headers: Optional[MutableMapping[str, str]] = ...
    ) -> Any: ...
