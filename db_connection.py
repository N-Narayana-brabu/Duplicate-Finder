
# backend
import streamlit as st
import pandas as pd
import mysql.connector
import base64


# Function to insert data into MySQL database
def insert_data_into_database(dataframe):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="workiy_email_duplicates_finder"
        )

        # Create a MySQL cursor
        cursor = connection.cursor()

        # Iterate through the rows of the dataframe and insert into the database
        for index, row in dataframe.iterrows():
            # Assuming your table has columns named 'column1', 'column2', etc.
            query = f"INSERT INTO lead_sheet (FirstName,LastName,EmailAddress,Designation,LinkedIn,CompanyName,CompanyWebsite,CompanyLinkedInURL,CMSVersion,Province,CompanyPhone,CompanyRevenue,Address,ValidationSource,ValidatedBy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (row['FirstName'], row['LastName'], row['EmailAddress'], row['Designation'], row['LinkedIn'], row['CompanyName'], row['CompanyWebsite'], row['CompanyLinkedInURL'], row['CMSVersion'], row['Province'], row['CompanyPhone'], row['CompanyRevenue'], row['Address'], row['ValidationSource'], row['ValidatedBy'])  # Adjust column names accordingly

            # Execute the query
            cursor.execute(query, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error inserting data into database: {e}")
        return False


# Function to delete data from MySQL database
def delete_data_from_database():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="workiy_email_duplicates_finder"
        )

        # Create a MySQL cursor
        cursor = connection.cursor()

        # Assuming you want to delete all data from the table
        query = "DELETE FROM lead_sheet"

        # Execute the query
        cursor.execute(query)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error deleting data from database: {e}")
        return False

# Function to insert data into MySQL database
def insert_existing_email_into_database(dataframe):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="workiy_email_duplicates_finder"
        )

        # Create a MySQL cursor
        cursor = connection.cursor()

        # Iterate through the rows of the dataframe and insert into the database
        for index, row in dataframe.iterrows():
            # Assuming your table has columns named 'column1', 'column2', etc.
            query = f"INSERT INTO Existing_Email_id(EmailAddress) VALUES (%s)"
            values = (row['EmailAddress'],)  # Adjust column names accordingly

            # Execute the query
            cursor.execute(query, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error inserting data into database: {e}")
        return False


# Function to delete data from MySQL database
def delete_existing_email_from_database():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="workiy_email_duplicates_finder"
        )

        # Create a MySQL cursor
        cursor = connection.cursor()

        # Assuming you want to delete all data from the table
        query = "DELETE FROM Existing_Email_id"

        # Execute the query
        cursor.execute(query)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error deleting data from database: {e}")
        return False


# Function to create a download link for the updated data
def get_table_download_link():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="workiy_email_duplicates_finder"
    )

    # Fetch the updated data from lead_sheet
    query_select_lead_sheet = "SELECT * FROM lead_sheet"
    df_updated = pd.read_sql(query_select_lead_sheet, connection)

    # Create a download link
    csv = df_updated.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="updated_lead_sheet.csv">! Click Here To Download Updated Lead Sheet</a>'

    # Close connection
    connection.close()

    return href

if __name__ == "__main__":
    main()



# Function to compare and delete rows in lead_sheet based on Existing_Email_id
def compare_and_delete():
    deleted_rows_count = 0  # Initialize a counter for deleted rows
    deleted_email_addresses = []  # Initialize a list to store deleted email addresses

    email_occurrence_count = {}  # Dictionary to store occurrence count for each email address

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="workiy_email_duplicates_finder"
        )

        # Create a MySQL cursor
        cursor = connection.cursor()

        # Get EmailAddress and its occurrence count from lead_sheet before deletion
        query_occurrence_count = "SELECT EmailAddress, COUNT(*) FROM lead_sheet GROUP BY EmailAddress"
        cursor.execute(query_occurrence_count)
        email_occurrence_count = dict(cursor.fetchall())

        # Get distinct EmailAddress values from Existing_Email_id table
        query_existing_email = "SELECT DISTINCT EmailAddress FROM Existing_Email_id"
        cursor.execute(query_existing_email)
        existing_email_addresses = [result[0] for result in cursor.fetchall()]

        # Delete rows from lead_sheet where EmailAddress matches Existing_Email_id
        for email_address in existing_email_addresses:
            query_delete = "DELETE FROM lead_sheet WHERE EmailAddress = %s"
            cursor.execute(query_delete, (email_address,))
            deleted_rows_count += cursor.rowcount  # Increment the counter
            deleted_email_addresses.append(email_address)  # Add deleted email address to the list

        # Commit changes and close connection
        connection.commit()
    except Exception as e:
        st.error(f"Error comparing and deleting data: {e}")
        connection.rollback()  # Rollback changes in case of an exception
    finally:
        # Close cursor and connection in the finally block
        cursor.close()
        connection.close()

        return deleted_rows_count, deleted_email_addresses, email_occurrence_count # Return the total number of deleted rows and the list of deleted email addresses