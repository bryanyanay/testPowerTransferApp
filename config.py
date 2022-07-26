db_user = 'admin'
db_password = 'qVX2yQTWDdoO6IzeKUX7RA39dVA_uZ'
database = 'test_power_transfer_app' # [this also works, but maybe its not secure?? i'm not sure]
db_host = 'northamerica-northeast2.d6301a4e-28af-45f8-a5ca-53fba3745b7a.gcp.ybdb.io' # i got this from the settings page for my cluster, in the connection parameters section
db_port = 5433 # the port for YSQL i believe


# i think we're supposed to use smth like this:
# database = 'test_power_transfer_app?ssl=true&sslmode=verify-full&sslrootcert=C:\Users\\alber\OneDrive\Bryan\Code\\testPowerTransferApp\\root.crt'
# which includes the root.crt; but it doesn't work for some reason and just the database name works, so we'll use that for now

"""
https://stackoverflow.com/questions/3327312/how-can-i-drop-all-the-tables-in-a-postgresql-database

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
"""
