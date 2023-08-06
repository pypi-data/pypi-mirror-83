from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
import io
import json
import os
import uuid
from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]


API_ROOT = 'https://www.googleapis.com/bigquery/v2'
SCOPES = [
    'https://www.googleapis.com/auth/bigquery.insertdata',
    'https://www.googleapis.com/auth/bigquery',
]

BIGQUERY_EMULATOR_HOST = os.environ.get('BIGQUERY_EMULATOR_HOST')
if BIGQUERY_EMULATOR_HOST:
    API_ROOT = 'http://{}/bigquery/v2'.format((BIGQUERY_EMULATOR_HOST))

class SourceFormat(Enum):
    AVRO = 'AVRO'
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    ORC = 'ORC'
    PARQUET = 'PARQUET'


class Disposition(Enum):
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_EMPTY = 'WRITE_EMPTY'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'


class SchemaUpdateOption(Enum):
    ALLOW_FIELD_ADDITION = 'ALLOW_FIELD_ADDITION'
    ALLOW_FIELD_RELAXATION = 'ALLOW_FIELD_RELAXATION'


class Job(object):
    def __init__(self, job_id                = None,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self.job_id = job_id
        self._project = project
        self.session = SyncSession(session)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def project(self)       :
        if self._project:
            return self._project

        if BIGQUERY_EMULATOR_HOST:
            self._project = str(os.environ.get('BIGQUERY_PROJECT_ID', 'dev'))
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    def headers(self)                  :
        if BIGQUERY_EMULATOR_HOST:
            return {}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    @staticmethod
    def _make_query_body(
            query     ,
            write_disposition             ,
            use_query_cache      ,
            dry_run      , use_legacy_sql      ,
            destination_table                   )                  :
        return {
            'configuration': {
                'query': {
                    'query': query,
                    'writeDisposition': write_disposition.value,
                    'destinationTable': {
                        'projectId': destination_table.project,
                        'datasetId': destination_table.dataset_name,
                        'tableId': destination_table.table_name,
                    } if destination_table else destination_table,
                    'useQueryCache': use_query_cache,
                    'useLegacySql': use_legacy_sql,
                },
                'dryRun': dry_run,
            },
        }

    def _post_json(
            self, url     , body                , session                   ,
            timeout     )                  :
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get
    def get_job(self, session                    = None,
                      timeout      = 60)                  :
        """Get the specified job resource by job ID."""

        project = self.project()
        url = '{}/projects/{}/jobs/{}'.format((API_ROOT), (project), (self.job_id))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults
    def get_query_results(self, session                    = None,
                                timeout      = 60)                  :
        """Get the specified jobQueryResults by job ID."""

        project = self.project()
        url = '{}/projects/{}/queries/{}'.format((API_ROOT), (project), (self.job_id))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel
    def cancel(self, session                    = None,
                     timeout      = 60)                  :
        """Cancel the specified job by job ID."""

        project = self.project()
        url = '{}/projects/{}/queries/{}/cancel'.format((API_ROOT), (project), (self.job_id))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery
    def insert_via_query(
            self, query     , session                    = None,
            write_disposition              = Disposition.WRITE_EMPTY,
            timeout      = 60, use_query_cache       = True,
            dry_run       = False, use_legacy_sql       = True,
            destination_table                    = None)                  :
        """Create table as a result of the query"""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_query_body(query=query,
                                     write_disposition=write_disposition,
                                     use_query_cache=use_query_cache,
                                     dry_run=dry_run,
                                     use_legacy_sql=use_legacy_sql,
                                     destination_table=destination_table)
        response = self._post_json(url, body, session, timeout)
        if not dry_run:
            self.job_id = response['jobReference']['jobId']
        return response


class Table(object):
    def __init__(self, dataset_name     , table_name     ,
                 project                = None,
                 service_file                                  = None,
                 session                    = None,
                 token                  = None)        :
        self.dataset_name = dataset_name
        self.table_name = table_name
        self._project = project
        self.session = SyncSession(session)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def project(self)       :
        if self._project:
            return self._project

        if BIGQUERY_EMULATOR_HOST:
            self._project = str(os.environ.get('BIGQUERY_PROJECT_ID', 'dev'))
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    def headers(self)                  :
        if BIGQUERY_EMULATOR_HOST:
            return {}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    @staticmethod
    def _mk_unique_insert_id(row                )       :
        # pylint: disable=unused-argument
        return uuid.uuid4().hex

    def _make_copy_body(
            self, source_project     , destination_project     ,
            destination_dataset     ,
            destination_table     )                  :
        return {
            'configuration': {
                'copy': {
                    'writeDisposition': 'WRITE_TRUNCATE',
                    'destinationTable': {
                        'projectId': destination_project,
                        'datasetId': destination_dataset,
                        'tableId': destination_table,
                    },
                    'sourceTable': {
                        'projectId': source_project,
                        'datasetId': self.dataset_name,
                        'tableId': self.table_name,
                    }
                }
            }
        }

    @staticmethod
    def _make_insert_body(
            rows                      , **_3to2kwargs                                 )                  :
        insert_id_fn = _3to2kwargs['insert_id_fn']; del _3to2kwargs['insert_id_fn']
        template_suffix = _3to2kwargs['template_suffix']; del _3to2kwargs['template_suffix']
        ignore_unknown = _3to2kwargs['ignore_unknown']; del _3to2kwargs['ignore_unknown']
        skip_invalid = _3to2kwargs['skip_invalid']; del _3to2kwargs['skip_invalid']
        body = {
            'kind': 'bigquery#tableDataInsertAllRequest',
            'skipInvalidRows': skip_invalid,
            'ignoreUnknownValues': ignore_unknown,
            'rows': [{
                'insertId': insert_id_fn(row),
                'json': row,
            } for row in rows],
        }

        if template_suffix is not None:
            body['templateSuffix'] = template_suffix

        return body

    def _make_load_body(
            self, source_uris           , project     , autodetect      ,
            source_format              ,
            write_disposition             ,
            ignore_unknown_values      ,
            schema_update_options                          
        )                  :
        return {
            'configuration': {
                'load': {
                    'autodetect': autodetect,
                    'ignoreUnknownValues': ignore_unknown_values,
                    'sourceUris': source_uris,
                    'sourceFormat': source_format.value,
                    'writeDisposition': write_disposition.value,
                    'schemaUpdateOptions': [
                        e.value for e in schema_update_options],
                    'destinationTable': {
                        'projectId': project,
                        'datasetId': self.dataset_name,
                        'tableId': self.table_name,
                    },
                },
            },
        }

    def _make_query_body(
            self, query     , project     ,
            write_disposition             ,
            use_query_cache      ,
            dry_run      )                  :
        return {
            'configuration': {
                'query': {
                    'query': query,
                    'writeDisposition': write_disposition.value,
                    'destinationTable': {
                        'projectId': project,
                        'datasetId': self.dataset_name,
                        'tableId': self.table_name,
                    },
                    'useQueryCache': use_query_cache,
                },
                'dryRun': dry_run,
            },
        }

    def _post_json(
            self, url     , body                , session                   ,
            timeout     )                  :
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers, params=None,
                            timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete
    def delete(self,
                     session                    = None,
                     timeout      = 60)                  :
        """Deletes the table specified by tableId from the dataset."""
        project = self.project()
        url = ('{}/projects/{}/datasets/'
               '{}/tables/{}'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.session.delete(url, headers=headers, params=None,
                                      timeout=timeout)
        try:
            data                 = resp.json()
        except Exception:  # pylint: disable=broad-except
            # For some reason, `gcloud-rest` seems to have intermittent issues
            # parsing this response. In that case, fall back to returning the
            # raw response body.
            try:
                data = {'response': resp.text()}
            except (AttributeError, TypeError):
                data = {'response': resp.text}

        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/get
    def get(
            self, session                    = None,
            timeout      = 60)                  :
        """Gets the specified table resource by table ID."""
        project = self.project()
        url = ('{}/projects/{}/datasets/'
               '{}/tables/{}'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll
    def insert(
            self, rows                      , skip_invalid       = False,
            ignore_unknown       = True, session                    = None,
            template_suffix                = None,
            timeout      = 60, **_3to2kwargs
    )                  :
        if 'insert_id_fn' in _3to2kwargs: insert_id_fn = _3to2kwargs['insert_id_fn']; del _3to2kwargs['insert_id_fn']
        else: insert_id_fn =  None
        """
        Streams data into BigQuery

        By default, each row is assigned a unique insertId. This can be
        customized by supplying an `insert_id_fn` which takes a row and
        returns an insertId.

        In cases where at least one row has successfully been inserted and at
        least one row has failed to be inserted, the Google API will return a
        2xx (successful) response along with an `insertErrors` key in the
        response JSON containing details on the failing rows.
        """
        if not rows:
            return {}

        project = self.project()
        url = ('{}/projects/{}/datasets/{}/'
               'tables/{}/insertAll'.format((API_ROOT), (project), (self.dataset_name), (self.table_name)))

        body = self._make_insert_body(
            rows, skip_invalid=skip_invalid, ignore_unknown=ignore_unknown,
            template_suffix=template_suffix,
            insert_id_fn=insert_id_fn or self._mk_unique_insert_id)
        return self._post_json(url, body, session, timeout)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfigurationtablecopy
    def insert_via_copy(
            self, destination_project     , destination_dataset     ,
            destination_table     , session                    = None,
            timeout      = 60)       :
        """Copy BQ table to another table in BQ"""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_copy_body(
            project, destination_project,
            destination_dataset, destination_table)
        response = self._post_json(url, body, session, timeout)
        return Job(response['jobReference']['jobId'], self._project,
                   session=self.session, token=self.token)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
    def insert_via_load(
            self, source_uris           , session                    = None,
            autodetect       = False,
            source_format               = SourceFormat.CSV,
            write_disposition              = Disposition.WRITE_TRUNCATE,
            timeout      = 60,
            ignore_unknown_values       = False,
            schema_update_options                                     = None
        )       :
        """Loads entities from storage to BigQuery."""
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_load_body(
            source_uris, project, autodetect, source_format, write_disposition,
            ignore_unknown_values, schema_update_options or []
        )
        response = self._post_json(url, body, session, timeout)
        return Job(response['jobReference']['jobId'], self._project,
                   session=self.session, token=self.token)

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery
    def insert_via_query(
            self, query     , session                    = None,
            write_disposition              = Disposition.WRITE_EMPTY,
            timeout      = 60, use_query_cache       = True,
            dry_run       = False)       :
        """Create table as a result of the query"""
        warnings.warn('using Table#insert_via_query is deprecated.'
                      'use Job#insert_via_query instead', DeprecationWarning)
        project = self.project()
        url = '{}/projects/{}/jobs'.format((API_ROOT), (project))

        body = self._make_query_body(query, project, write_disposition,
                                     use_query_cache, dry_run)
        response = self._post_json(url, body, session, timeout)
        job_id = response['jobReference']['jobId'] if not dry_run else None
        return Job(job_id, self._project,
                   session=self.session, token=self.token)

    def close(self)        :
        self.session.close()

    def __enter__(self)           :
        return self

    def __exit__(self, *args     )        :
        self.close()
