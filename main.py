from astroquery.gaia import Gaia
from util.gaia_retriever import async_retrieve_astrophysical_parameters as retrieve_parameters
import config

Gaia.ROW_LIMIT = -1
Gaia.login(user=config.user, password=config.password)

QUERY = open("").read()

parameters = retrieve_parameters(QUERY)

print(parameters)
