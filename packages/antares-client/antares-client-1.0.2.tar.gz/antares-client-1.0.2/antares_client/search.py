"""
Search the ANTARES database for objects of interest.
"""
import json
from typing import Dict, Iterator, Optional
from urllib.parse import urljoin

import astropy.coordinates
import astropy.units

from ._api.api import _get_resource, _list_all_resources
from ._api.models import Locus, _LocusSchema, _LocusListingSchema
from .config import config


def search(query: Dict) -> Iterator[Locus]:
    """
    Searches the ANTARES database for loci that meet certain criteria.

    Parameters
    ----------
    query: dict
        An ElasticSearch query. Must contain a top-level "query" key and only that
        top-level key. Other ES search arguments (e.g. "aggregations") are not allowed.

    Returns
    ----------
    Iterator over Locus objects

    """
    return _list_all_resources(
        urljoin(config["ANTARES_API_BASE_URL"], "loci"),
        _LocusListingSchema,
        params={
            "page[limit]": 100,
            "elasticsearch_query[locus_listing]": json.dumps(query),
        },
    )


def cone_search(
    center: astropy.coordinates.SkyCoord, radius: astropy.coordinates.Angle
) -> Iterator[Locus]:
    """
    Searches the ANTARES database for loci in a certain region.

    Parameters
    ----------
    center: astropy.coordiantes.SkyCoord
    radius: astropy.coordiantes.Angle

    Returns
    ----------
    Iterator over Locus objects

    """
    return search(
        {
            "query": {
                "bool": {
                    "filter": {
                        "sky_distance": {
                            "distance": f"{radius.to_string(unit=astropy.units.deg, decimal=True)} degree",
                            "htm16": {"center": center.to_string()},
                        },
                    },
                },
            },
        }
    )


def get_by_id(locus_id: str) -> Optional[Locus]:
    """
    Gets an ANTARES locus by its ANTARES ID.

    Parameters
    ----------
    locus_id: str

    Returns
    ----------
    Locus or None

    """
    return _get_resource(
        urljoin(config["ANTARES_API_BASE_URL"], "loci/{}".format(locus_id)),
        _LocusSchema,
    )


def get_by_ztf_object_id(ztf_object_id: str) -> Optional[Locus]:
    """
    Gets an ANTARES locus by its ZTF Object ID.

    Parameters
    ----------
    ztf_object_id: str

    Returns
    ----------
    Locus or None

    """
    try:
        return next(
            search(
                {
                    "query": {
                        "bool": {
                            "filter": {
                                "term": {"properties.ztf_object_id": ztf_object_id},
                            },
                        },
                    },
                }
            )
        )
    except StopIteration:
        return None
