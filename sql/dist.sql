SELECT gaiadr3.astrophysical_parameters.lum_flame,gaiadr3.gaia_source.phot_g_mean_mag,gaiadr3.astrophysical_parameters.bc_flame,(1/gaiadr3.gaia_source.parallax),gaiadr3.gaia_source.distance_gspphot
FROM gaiadr3.astrophysical_parameters
INNER JOIN gaiadr3.gaia_source ON gaiadr3.astrophysical_parameters.source_id=gaiadr3.gaia_source.source_id
WHERE gaiadr3.gaia_source.random_index BETWEEN 0 AND 50000000
AND gaiadr3.gaia_source.phot_g_mean_mag IS NOT NULL
AND gaiadr3.astrophysical_parameters.lum_flame IS NOT NULL
AND gaiadr3.astrophysical_parameters.bc_flame IS NOT NULL
AND gaiadr3.gaia_source.distance_gspphot IS NOT NULL
AND (gaiadr3.gaia_source.distance_gspphot_upper * 1.0 - gaiadr3.gaia_source.distance_gspphot_lower * 1.0) / gaiadr3.gaia_source.distance_gspphot < 0.02
AND (gaiadr3.astrophysical_parameters.lum_flame_upper * 1.0 - gaiadr3.astrophysical_parameters.lum_flame_lower * 1.0) / gaiadr3.astrophysical_parameters.lum_flame < 0.02
AND (1/gaiadr3.gaia_source.phot_g_mean_flux_over_error) < 0.002
AND (1/gaiadr3.gaia_source.parallax_over_error) < 0.02