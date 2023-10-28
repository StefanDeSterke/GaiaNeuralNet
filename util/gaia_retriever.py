from astroquery.gaia import Gaia
import pandas as pd
import time


def sync_retrieve_astrophysical_parameters(query: str) -> pd.DataFrame:
    job = Gaia.launch_job(query)

    return job.get_results().to_pandas()


def async_retrieve_astrophysical_parameters(query: str) -> pd.DataFrame:
    job = Gaia.launch_job_async(query, background=True)

    print(job)

    while job.get_phase(update=True) != 'COMPLETED':
        print("Job still processing..")
        time.sleep(5)

    print("Job complete!")

    return job.get_results().to_pandas()


def local_retrieve_astrophysical_parameters():
    df1 = pd.read_csv('../gaia_data/filtered_data/gaia-1 filtered.csv', header=0, sep=r'\s*,\s*',
                      engine='python')  # Header: 0 lines; comma-separated (allow spaces)
    df2 = pd.read_csv('../gaia_data/filtered_data/gaia-2 filtered.csv', header=0, sep=r'\s*,\s*',
                      engine='python')  # Header: 0 lines; comma-separated (allow spaces)

    return pd.concat([df1, df2])
