SELECT gaiadr3.astrophysical_parameters.teff_gspphot,gaiadr3.astrophysical_parameters.mass_flame,lum_flame
FROM gaiadr3.astrophysical_parameters
INNER JOIN gaiadr3.gaia_source ON gaiadr3.astrophysical_parameters.source_id=gaiadr3.gaia_source.source_id
WHERE gaiadr3.astrophysical_parameters.teff_gspphot IS NOT NULL
AND gaiadr3.astrophysical_parameters.mass_flame IS NOT NULL
AND gaiadr3.astrophysical_parameters.lum_flame IS NOT NULL
AND gaiadr3.gaia_source.random_index BETWEEN 0 AND 500000