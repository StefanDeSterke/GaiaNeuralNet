SELECT gaiadr3.gaia_source.bp_rp,gaiadr3.gaia_source.parallax,gaiadr3.gaia_source.distance_gspphot
FROM gaiadr3.gaia_source
WHERE gaiadr3.gaia_source.bp_rp IS NOT NULL
AND gaiadr3.gaia_source.distance_gspphot IS NOT NULL
AND gaiadr3.gaia_source.parallax IS NOT NULL
AND gaiadr3.gaia_source.random_index BETWEEN 0 AND 50000