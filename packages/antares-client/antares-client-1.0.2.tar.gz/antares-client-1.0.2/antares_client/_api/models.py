from enum import Enum
from typing import List

import astropy.timeseries
import pandas as pd
from marshmallow import post_load
from marshmallow_jsonapi import fields, Schema

from .api import _get_resource, _list_resources
from .fields import _Lightcurve
from ..config import config
from ..utils import mjd_to_datetime


class _AlertSchema(Schema):
    class Meta:
        type_ = "alert"

    id = fields.String(attribute="alert_id")
    properties = fields.Dict()
    mjd = fields.Float()
    resource_meta = fields.ResourceMeta()
    document_meta = fields.DocumentMeta()

    @post_load
    def make_alert(self, data: dict, **kwargs):
        return Alert(**data)


class _LocusSchema(Schema):
    class Meta:
        type_ = "locus"

    id = fields.Str(attribute="locus_id")
    htm16 = fields.Int()
    ra = fields.Float()
    dec = fields.Float()
    properties = fields.Dict()
    lightcurve = _Lightcurve()
    alerts = fields.Relationship()
    tags = fields.List(fields.Str())
    catalogs = fields.List(fields.Str())
    catalog_matches = fields.List(fields.Dict())
    resource_meta = fields.ResourceMeta()
    document_meta = fields.DocumentMeta()

    @post_load
    def make_locus(self, data: dict, **kwargs):
        return Locus(**data, _state=_LocusState.DETAIL)


class _LocusListingSchema(Schema):
    class Meta:
        type_ = "locus_listing"

    id = fields.Str(attribute="locus_id")
    htm16 = fields.Int()
    ra = fields.Float()
    dec = fields.Float()
    properties = fields.Dict()
    locus = fields.Relationship()
    alerts = fields.Relationship()
    tags = fields.List(fields.Str())
    catalogs = fields.List(fields.Str())
    resource_meta = fields.ResourceMeta()
    document_meta = fields.DocumentMeta()

    @post_load
    def make_locus(self, data: dict, **kwargs):
        return Locus(**data, _state=_LocusState.LISTING)


class Alert:
    def __init__(self, alert_id: str, mjd: float, properties: dict, **kwargs):
        self.alert_id = alert_id
        self.mjd = mjd
        self.properties = properties


class _LocusState(Enum):
    LISTING = "listing"
    DETAIL = "detail"


class Locus:
    def __init__(
        self,
        locus_id: str,
        ra: float,
        dec: float,
        properties: dict,
        tags: List[str],
        alerts: List[Alert] = None,
        catalogs: List[str] = None,
        catalog_objects: List[dict] = None,
        lightcurve: pd.DataFrame = None,
        watch_list_ids: List[str] = None,
        watch_object_ids: List[str] = None,
        _state: _LocusState = _LocusState.LISTING,
        **kwargs
    ):
        self.locus_id = locus_id
        self.ra = ra
        self.dec = dec
        self.properties = properties
        self.tags = tags
        self.catalogs = catalogs
        if self.catalogs is None:
            self.catalogs = []
        self.watch_list_ids = watch_list_ids
        if self.watch_list_ids is None:
            self.watch_list_ids = []
        self.watch_object_ids = watch_object_ids
        if self.watch_object_ids is None:
            self.watch_object_ids = []
        self._alerts = alerts
        self._catalog_objects = catalog_objects
        self._lightcurve = lightcurve
        self._timeseries = None
        self._state = _state

    def _fetch_alerts(self):
        alerts = _list_resources(
            config["ANTARES_API_BASE_URL"]
            + "/".join(("loci", self.locus_id, "alerts")),
            _AlertSchema,
        )
        self._alerts = list(alerts)

    def _fetch_locus_details(self):
        locus = _get_resource(
            config["ANTARES_API_BASE_URL"] + "/".join(("loci", self.locus_id)),
            _LocusSchema,
        )
        self._catalog_objects = locus.catalog_objects
        self._lightcurve = locus.lightcurve
        self._state = _LocusState.DETAIL

    @property
    def timeseries(self):
        if self._timeseries is None:
            self._timeseries = astropy.timeseries.TimeSeries(
                data=[alert.properties for alert in self.alerts],
                time=[mjd_to_datetime(alert.mjd) for alert in self.alerts],
            )
        return self._timeseries

    @timeseries.setter
    def timeseries(self, value):
        self._timeseries = value

    @property
    def alerts(self):
        if self._alerts is None:
            self._fetch_alerts()
        return self._alerts

    @alerts.setter
    def alerts(self, value):
        self._alerts = value

    @property
    def catalog_objects(self):
        if self._catalog_objects is None and self._state == _LocusState.LISTING:
            self._fetch_locus_details()
        return self._catalog_objects

    @catalog_objects.setter
    def catalog_objects(self, value):
        self._catalog_objects = value

    @property
    def lightcurve(self):
        if self._lightcurve is None and self._state == _LocusState.LISTING:
            self._fetch_locus_details()
        return self._lightcurve

    @lightcurve.setter
    def lightcurve(self, value):
        self._lightcurve = value
