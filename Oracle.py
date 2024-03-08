import getpass
import oracledb

#pw = getpass.getpass("Enter password: ")

connection = oracledb.connect(
    user="admin",
    password="Gudiya@123456",
    dsn="rajaniishdb_high",
    config_dir=r"C:\Tools\Oracle Wallet\Wallet_RAJANIISHDB",
    wallet_location=r"C:\Tools\Oracle Wallet\Wallet_RAJANIISHDB",
    wallet_password="Gudiya@1")


print(connection.version)


cursor = connection.cursor()
cursor.execute("SELECT network_service_banner FROM v$session_connect_info")
for row in cursor:
    print(row)

# Close the cursor and connection
cursor.close()

connection.close()
