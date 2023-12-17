SELECT gaiadr3.astrophysical_parameters.radius_flame,gaiadr3.astrophysical_parameters.lum_flame,gaiadr3.astrophysical_parameters.teff_gspphot,gaiadr3.astrophysical_parameters.distance_gspphot
FROM gaiadr3.astrophysical_parameters
INNER JOIN gaiadr3.gaia_source ON gaiadr3.astrophysical_parameters.source_id=gaiadr3.gaia_source.source_id
WHERE gaiadr3.gaia_source.random_index BETWEEN 0 AND 50000000
AND gaiadr3.astrophysical_parameters.radius_flame IS NOT NULL
AND gaiadr3.astrophysical_parameters.lum_flame IS NOT NULL
AND gaiadr3.astrophysical_parameters.teff_gspphot IS NOT NULL
AND gaiadr3.astrophysical_parameters.distance_gspphot IS NOT NULL
AND (gaiadr3.astrophysical_parameters.radius_flame_upper * 1.0 - gaiadr3.astrophysical_parameters.radius_flame_lower * 1.0) / gaiadr3.astrophysical_parameters.radius_flame < 0.1
AND (gaiadr3.astrophysical_parameters.lum_flame_upper * 1.0 - gaiadr3.astrophysical_parameters.lum_flame_lower * 1.0) / gaiadr3.astrophysical_parameters.lum_flame < 0.02
AND (gaiadr3.astrophysical_parameters.teff_gspphot_upper * 1.0 - gaiadr3.astrophysical_parameters.teff_gspphot_lower * 1.0) / gaiadr3.astrophysical_parameters.teff_gspphot < 0.02
AND (gaiadr3.astrophysical_parameters.distance_gspphot_upper * 1.0 - gaiadr3.astrophysical_parameters.distance_gspphot_lower * 1.0) / gaiadr3.astrophysical_parameters.distance_gspphot < 0.02