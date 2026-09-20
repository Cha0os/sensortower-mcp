#!/usr/bin/env python3
"""Store Marketing API tools for Sensor Tower MCP Server."""

from typing import Annotated, Literal, Optional, Union

from fastmcp import FastMCP
from pydantic import Field

from ..base import SensorTowerTool, validate_date_format, validate_os_parameter


class StoreMarketingTools(SensorTowerTool):
    """Tools for Store Marketing API endpoints."""

    category = "StoreMarketing"

    def register_tools(self, mcp: FastMCP) -> None:
        """Register all store marketing tools with FastMCP."""

        @self.tool(
            mcp,
            name="get_featured_today_stories",
            title="Get Featured Today Stories",
        )
        async def get_featured_today_stories(
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ] = "US",
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured Today stories from the App Store."""

            params = {"country": country}
            if start_date:
                params["start_date"] = validate_date_format(start_date)
            if end_date:
                params["end_date"] = validate_date_format(end_date)

            return await self.make_request("/v1/ios/featured/today/stories", params)

        @self.tool(
            mcp,
            name="get_featured_apps",
            title="Get Featured Apps",
        )
        async def get_featured_apps(
            category: Annotated[
                Union[int, str],
                Field(description="Category identifier"),
            ],
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ] = "US",
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured apps on the App Store's Apps & Games pages."""

            params = {
                "category": category,
                "country": country,
            }
            if start_date:
                params["start_date"] = validate_date_format(start_date)
            if end_date:
                params["end_date"] = validate_date_format(end_date)

            return await self.make_request("/v1/ios/featured/apps", params)

        @self.tool(
            mcp,
            name="get_featured_creatives",
            title="Get Featured Creatives",
        )
        async def get_featured_creatives(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            app_id: Annotated[str, Field(description="App identifier", min_length=1)],
            countries: Annotated[
                Optional[str],
                Field(description="Comma-separated country codes", default=None),
            ] = None,
            types: Annotated[
                Optional[str],
                Field(description="Comma-separated creative types", default=None),
            ] = None,
            start_date: Annotated[
                Optional[str],
                Field(description="Start date in YYYY-MM-DD format", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="End date in YYYY-MM-DD format", default=None),
            ] = None,
        ) -> dict:
            """Retrieve featured creatives and their positions over time."""

            os_value = validate_os_parameter(os, ["ios", "android"])
            params = {"app_id": app_id}

            optional_params = {
                "countries": countries,
                "types": types,
                "start_date": validate_date_format(start_date) if start_date else None,
                "end_date": validate_date_format(end_date) if end_date else None,
            }

            for key, value in optional_params.items():
                if value:
                    params[key] = value

            return await self.make_request(
                f"/v1/{os_value}/featured/creatives",
                params,
            )

        @self.tool(
            mcp,
            name="get_keywords",
            title="Get Keywords",
        )
        async def get_keywords(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            app_id: Annotated[str, Field(description="App identifier", min_length=1)],
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ] = "US",
            limit: Annotated[
                Optional[int],
                Field(description="Maximum keywords to return", ge=1, default=None),
            ] = None,
            offset: Annotated[
                Optional[int],
                Field(description="Offset for pagination", ge=0, default=None),
            ] = None,
            devices: Annotated[
                Optional[str],
                Field(description="Comma-separated devices (iOS only)", default=None),
            ] = None,
        ) -> dict:
            """Get current keyword rankings for an app."""

            os_value = validate_os_parameter(os, ["ios", "android"])
            params = {
                "bundle": "aso_top_keywords",
                "breakdown": "keyword",
                "os": os_value,
                "app_ids": app_id,
                "regions": country,
            }
            if limit is not None:
                params["limit"] = limit
            if offset is not None:
                params["offset"] = offset
            if devices:
                params["devices"] = devices

            return await self.make_request("/v1/facets/metrics", params)

        @self.tool(
            mcp,
            name="get_reviews",
            title="Get Reviews",
        )
        async def get_reviews(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            app_id: Annotated[str, Field(description="App identifier", min_length=1)],
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ],
            start_date: Annotated[
                Optional[str],
                Field(description="Filter reviews from this date", default=None),
            ] = None,
            end_date: Annotated[
                Optional[str],
                Field(description="Filter reviews up to this date", default=None),
            ] = None,
            rating_filter: Annotated[
                Optional[str],
                Field(description="Filter by rating or sentiment", default=None),
            ] = None,
            search_term: Annotated[
                Optional[str],
                Field(description="Filter by review content", default=None),
            ] = None,
            username: Annotated[
                Optional[str],
                Field(description="Filter by reviewer username", default=None),
            ] = None,
            limit: Annotated[
                Optional[int],
                Field(description="Maximum reviews per call (max 200)", ge=1, le=200, default=None),
            ] = None,
            page: Annotated[
                Optional[int],
                Field(description="Page number for pagination", ge=1, default=None),
            ] = None,
        ) -> dict:
            """Get app reviews and ratings data."""

            os_value = validate_os_parameter(os, ["ios", "android"])
            params = {
                "app_id": app_id,
                "country": country,
            }

            optional_params = {
                "start_date": validate_date_format(start_date) if start_date else None,
                "end_date": validate_date_format(end_date) if end_date else None,
                "rating_filter": rating_filter,
                "search_term": search_term,
                "username": username,
                "limit": limit,
                "page": page,
            }

            for key, value in optional_params.items():
                if value is not None:
                    params[key] = value

            return await self.make_request(
                f"/v1/{os_value}/review/get_reviews",
                params,
            )

        @self.tool(
            mcp,
            name="research_keyword",
            title="Research Keyword",
        )
        async def research_keyword(
            os: Annotated[
                Literal["ios", "android"],
                Field(description="Operating system"),
            ],
            term: Annotated[str, Field(description="Keyword term to research", min_length=1)],
            country: Annotated[
                str,
                Field(description="ISO country code", min_length=2, max_length=2),
            ],
            devices: Annotated[
                Optional[str],
                Field(description="Comma-separated devices (iOS only)", default=None),
            ] = None,
        ) -> dict:
            """Retrieve the apps ranking for a keyword, with traffic and difficulty scores."""

            os_value = validate_os_parameter(os, ["ios", "android"])
            params = {
                "bundle": "aso_keyword_research",
                "os": os_value,
                "keywords": term,
                "regions": country,
            }
            if devices:
                params["devices"] = devices

            return await self.make_request("/v1/facets/metrics", params)
