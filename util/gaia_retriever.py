from astroquery.gaia import Gaia
import pandas as pd
import time

QUERY = ("SELECT gaiadr3.astrophysical_parameters.teff_gspphot,gaiadr3.astrophysical_parameters.lum_flame "
         "FROM gaiadr3.astrophysical_parameters "
         "INNER JOIN gaiadr3.gaia_source ON gaiadr3.astrophysical_parameters.source_id=gaiadr3.gaia_source.source_id "
         "WHERE gaiadr3.astrophysical_parameters.teff_gspphot IS NOT NULL "
         "AND gaiadr3.astrophysical_parameters.lum_flame IS NOT NULL "
         "AND gaiadr3.astrophysical_parameters.classprob_dsc_combmod_whitedwarf > 0.999 "
         "AND gaiadr3.gaia_source.random_index BETWEEN 0 AND 500000")


def sync_retrieve_astrophysical_parameters():
    job = Gaia.launch_job(QUERY)

    return job.get_results().to_pandas()


def async_retrieve_astrophysical_parameters():
    job = Gaia.launch_job_async(QUERY, background=True)

    print(job)

    while job.get_phase(update = True) != 'COMPLETED':
        print("Job still processing..")
        time.sleep(5)

    print("Job complete!")

    return job.get_results().to_pandas()


def local_retrieve_astrophysical_parameters():
    df1 = pd.read_csv('../gaia_data/filtered_data/gaia-1 filtered.csv', header=0, sep=r'\s*,\s*', engine='python')  # Header: 0 lines; comma-separated (allow spaces)
    df2 = pd.read_csv('../gaia_data/filtered_data/gaia-2 filtered.csv', header=0, sep=r'\s*,\s*', engine='python')  # Header: 0 lines; comma-separated (allow spaces)

    return pd.concat([df1, df2])

