import logging
from datetime import datetime

from fastapi import HTTPException

from opennem.api.export.router import api_export_energy_month
from opennem.api.stats.router import (
    energy_network_fueltech_api,
    power_network_fueltech_api,
    price_network_region_api,
)
from opennem.api.weather.router import station_observations_api
from opennem.db import get_database_engine
from opennem.exporter.aws import write_to_s3

YEAR_MIN = 2010

logger = logging.getLogger(__name__)


def wem_export_power():
    engine = get_database_engine()

    stat_set = power_network_fueltech_api(
        network_code="WEM",
        network_region="WEM",
        interval="30m",
        period="7d",
        engine=engine,
    )

    weather = station_observations_api(
        station_code="009021",
        interval="30m",
        period="7d",
        network_code="WEM",
        engine=engine,
    )

    price = price_network_region_api(
        engine=engine,
        network_code="WEM",
        network_region_code="WEM",
        interval="30m",
        period="7d",
    )

    # demand = wem_demand()

    stat_set.data = stat_set.data + price.data + weather.data

    POWER_ENDPOINT = "/power/wem.json"

    # @TODO migrate to s3 methods
    byte_count = write_to_s3(POWER_ENDPOINT, stat_set.json(exclude_unset=True))

    logger.info("Wrote {} bytes to {}".format(byte_count, POWER_ENDPOINT))


def wem_export_years():
    engine = get_database_engine()

    for year in range(datetime.now().year, YEAR_MIN - 1, -1):

        stat_set = None

        try:
            stat_set = energy_network_fueltech_api(
                network_code="WEM",
                network_region="WEM",
                interval="1d",
                year=year,
                period="1Y",
                engine=engine,
            )
        except HTTPException as e:
            logger.info(
                "Could not get energy network fueltech for {} {} : {}".format(
                    "WEM", year, e
                )
            )
            continue

        # market_value = wem_market_value_year(year)

        write_to_s3(
            f"/wem/energy/daily/{year}.json", stat_set.json(exclude_unset=True)
        )


def wem_export_all():
    """

        @TODO this is slow atm because of on_energy_sum
    """

    engine = get_database_engine()

    stats = energy_network_fueltech_api(
        network_code="WEM",
        period="all",
        engine=engine,
        interval="1M",
        network_region=None,
    )

    # market_value = wem_market_value_all()

    write_to_s3("/wem/energy/monthly/all.json", stats.json(exclude_unset=True))


def wem_run_all():
    wem_export_power()
    wem_export_years()


if __name__ == "__main__":
    wem_export_all()
