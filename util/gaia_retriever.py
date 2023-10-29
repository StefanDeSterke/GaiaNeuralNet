from astroquery.gaia import Gaia
import pandas as pd
import time


def sync_retrieve_astrophysical_parameters(query: str) -> pd.DataFrame:
    job = Gaia.launch_job(query)

    return job.get_results().to_pandas()


def async_retrieve_astrophysical_parameters(query: str, file_dump: bool, file: str = None) -> pd.DataFrame:
    job = Gaia.launch_job_async(query, background=True, dump_to_file=file_dump, output_file=file)
    print(job)

    while True:
        phase = job.get_phase(update=True)

        if phase == 'COMPLETED':
            break
        elif phase == 'ERROR':
            raise Exception(f"Something went wrong trying to retrieve the astrophysical parameters:\n{job.get_error()}")

        print("Job still processing..")
        time.sleep(5)

    print("Job complete!")

    job.save_results(verbose=True)

    return job.get_results().to_pandas()


def local_retrieve_astrophysical_parameters():
    df1 = pd.read_csv('../gaia_data/filtered_data/gaia-1 filtered.csv', header=0, sep=r'\s*,\s*',
                      engine='python')  # Header: 0 lines; comma-separated (allow spaces)
    df2 = pd.read_csv('../gaia_data/filtered_data/gaia-2 filtered.csv', header=0, sep=r'\s*,\s*',
                      engine='python')  # Header: 0 lines; comma-separated (allow spaces)

    return pd.concat([df1, df2])
