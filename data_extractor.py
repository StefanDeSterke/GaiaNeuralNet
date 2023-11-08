from util.gaia_retriever import async_retrieve_astrophysical_parameters as retrieve_parameters
from astroquery.gaia import Gaia
import config
from pathlib import Path

script_location = Path(__file__).absolute().parent

Gaia.ROW_LIMIT = -1
Gaia.login(user=config.user, password=config.password)

QUERY = open(script_location / "sql/dist.sql").read()

parameters = retrieve_parameters(QUERY, file_dump=True, file=str(script_location / "tables/dist.vot.gz"))

print(parameters)