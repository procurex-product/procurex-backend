import bcrypt
from mysql.connector import pooling
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import datetime
app = Flask(__name__)
CORS(app)

# Database Configuration
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "prakash610",
#     "database": "procurex"
# }

db_config = {
    'host': 'productdb.cocsaoggytrc.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Fruits123',
    'database': 'productdb'
}

# db_config={
#     'host':'attendance-system.cepf8h0tkttq.ap-south-1.rds.amazonaws.com',
#         'database':'attendanceSystem',
#         'user':'admin',
#         'password':'studentdata2023'
# }

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=25,
    **db_config
)

@app.route("/")
def read_root():
    return {"Hello": "World"}


@app.route("/api/productAdd", methods=["POST"])
def create_product():
    name = request.json.get("name")
    description = request.json.get("description")

    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the data into the database
        insert_query = "INSERT INTO Products (name, description) VALUES (%s, %s)"
        data = (name, description)
        cursor.execute(insert_query, data)
        connection.commit()

        # Getting the generated primary key
        product_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the created product information
        return jsonify({"id": product_id, "name": name, "description": description})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/products")
def get_all_products():
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all products from the database
        select_query = "SELECT * FROM Products"
        cursor.execute(select_query)
        products = cursor.fetchall()

        # Creating a list of product dictionaries
        product_list = []
        for product in products:
            product_dict = {
                "id": product[0],
                "name": product[1],
                "description": product[2]
            }
            product_list.append(product_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of products as a JSON response
        return jsonify(product_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500




@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    request_data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the product in the database
        update_query = "UPDATE Products SET name=%s, description=%s WHERE product_id=%s"
        data = (
            request_data["name"],
            request_data["description"],
            product_id,
        )
        cursor.execute(update_query, data)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Return the updated product
        updated_product = {
            "id": product_id,
            "name": request_data["name"],
            "description": request_data["description"],
        }
        return jsonify(updated_product)

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error updating product:", error)
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/products/<int:product_id>", methods=["GET", "DELETE"])
def handle_product(product_id):
    if request.method == "GET":
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Retrieving a product by its ID from the database
            select_query = "SELECT * FROM Products WHERE product_id = %s"
            cursor.execute(select_query, (product_id,))
            product = cursor.fetchone()

            if product:
                # Creating a product dictionary
                product_dict = {
                    "id": product[0],
                    "name": product[1],
                    "description": product[2]
                }

                # Closing the cursor and connection
                cursor.close()
                connection.close()

                # Returning the product as a JSON response
                return jsonify(product_dict)
            else:
                # Product not found
                return jsonify({"error": "Product not found"}), 404

        except mysql.connector.Error as error:
            # Handling database errors
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == "DELETE":
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Deleting the product from the database
            delete_query = "DELETE FROM Products WHERE product_id = %s"
            cursor.execute(delete_query, (product_id,))
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            return jsonify({"message": "Product deleted successfully"})

        except mysql.connector.Error as error:
            # Handling database errors
            return jsonify({"error": "Database error occurred"}), 500

# ... (previous code for other APIs)

########################ALLOTMENT#############################

# Allotment Photoshoot API

# Backend Flask APIs for Allotment Photoshoot


@app.route("/api/allotment/photoshoot", methods=["POST"])
def handle_allotment_photoshoot():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the allotment photoshoot into the database
        insert_query = "INSERT INTO Allotment_Photoshoot (product_id, allotted_date, timeline_deadline, submission_date, comments) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data["product_id"],
            data["allotted_date"],
            data["timeline_deadline"],
            data["submission_date"],
            data["comments"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Return the inserted allotment photoshoot
        inserted_allotment_photoshoot = {
            "allotment_id": cursor.lastrowid,
            "product_id": data["product_id"],
            "allotted_date": data["allotted_date"],
            "timeline_deadline": data["timeline_deadline"],
            "submission_date": data["submission_date"],
            "comments": data["comments"],
        }
        return jsonify(inserted_allotment_photoshoot), 201

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error inserting allotment photoshoot:", error)
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/allotment/photoshoot/<int:allotment_id>", methods=["PUT", "DELETE"])
def handle_specific_allotment_photoshoot(allotment_id):
    if request.method == "PUT":
        data = request.json
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Updating the allotment photoshoot in the database
            update_query = "UPDATE Allotment_Photoshoot SET allotted_date=%s, timeline_deadline=%s, submission_date=%s, comments=%s WHERE allotment_id=%s AND product_id=%s"
            values = (
                data["allotted_date"],
                data["timeline_deadline"],
                data["submission_date"],
                data["comments"],
                allotment_id,
                data["product_id"],
            )
            cursor.execute(update_query, values)
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            # Return the updated allotment photoshoot
            updated_allotment_photoshoot = {
                "allotment_id": allotment_id,
                "product_id": data["product_id"],
                "allotted_date": data["allotted_date"],
                "timeline_deadline": data["timeline_deadline"],
                "submission_date": data["submission_date"],
                "comments": data["comments"],
            }
            return jsonify(updated_allotment_photoshoot)

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error updating allotment photoshoot:", error)
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == "DELETE":
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Deleting the allotment photoshoot from the database
            delete_query = "DELETE FROM Allotment_Photoshoot WHERE allotment_id = %s"
            cursor.execute(delete_query, (allotment_id,))
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            return jsonify({"message": "Allotment photoshoot deleted successfully"})

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error deleting allotment photoshoot:", error)
            return jsonify({"error": "Database error occurred"}), 500

# Backend Flask APIs for Allotment Listing


@app.route("/api/allotment/listing", methods=["POST"])
def handle_allotment_listing():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the allotment listing into the database
        insert_query = "INSERT INTO Allotment_Listing (product_id, allotted_date, timeline_deadline, submission_date, comments) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data["product_id"],
            data["allotted_date"],
            data["timeline_deadline"],
            data["submission_date"],
            data["comments"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Return the inserted allotment listing
        inserted_allotment_listing = {
            "allotment_id": cursor.lastrowid,
            "product_id": data["product_id"],
            "allotted_date": data["allotted_date"],
            "timeline_deadline": data["timeline_deadline"],
            "submission_date": data["submission_date"],
            "comments": data["comments"],
        }
        return jsonify(inserted_allotment_listing), 201

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error inserting allotment listing:", error)
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/allotment/listing/<int:allotment_id>", methods=["PUT", "DELETE"])
def handle_specific_allotment_listing(allotment_id):
    if request.method == "PUT":
        data = request.json
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Updating the allotment listing in the database
            update_query = "UPDATE Allotment_Listing SET allotted_date=%s, timeline_deadline=%s, submission_date=%s, comments=%s WHERE allotment_id=%s AND product_id=%s"
            values = (
                data["allotted_date"],
                data["timeline_deadline"],
                data["submission_date"],
                data["comments"],
                allotment_id,
                data["product_id"],
            )
            cursor.execute(update_query, values)
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            # Return the updated allotment listing
            updated_allotment_listing = {
                "allotment_id": allotment_id,
                "product_id": data["product_id"],
                "allotted_date": data["allotted_date"],
                "timeline_deadline": data["timeline_deadline"],
                "submission_date": data["submission_date"],
                "comments": data["comments"],
            }
            return jsonify(updated_allotment_listing)

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error updating allotment listing:", error)
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == "DELETE":
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Deleting the allotment listing from the database
            delete_query = "DELETE FROM Allotment_Listing WHERE allotment_id = %s"
            cursor.execute(delete_query, (allotment_id,))
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            return jsonify({"message": "Allotment listing deleted successfully"})

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error deleting allotment listing:", error)
            return jsonify({"error": "Database error occurred"}), 500

# Backend Flask APIs for Allotment Content


@app.route("/api/allotment/content", methods=["POST"])
def handle_allotment_content():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the allotment content into the database
        insert_query = "INSERT INTO Allotment_Content (product_id, allotted_date, timeline_deadline, submission_date, comments) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data["product_id"],
            data["allotted_date"],
            data["timeline_deadline"],
            data["submission_date"],
            data["comments"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Return the inserted allotment content
        inserted_allotment_content = {
            "allotment_id": cursor.lastrowid,
            "product_id": data["product_id"],
            "allotted_date": data["allotted_date"],
            "timeline_deadline": data["timeline_deadline"],
            "submission_date": data["submission_date"],
            "comments": data["comments"],
        }
        return jsonify(inserted_allotment_content), 201

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error inserting allotment content:", error)
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/allotment/content/<int:allotment_id>", methods=["PUT", "DELETE"])
def handle_specific_allotment_content(allotment_id):
    if request.method == "PUT":
        data = request.json
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Updating the allotment content in the database
            update_query = "UPDATE Allotment_Content SET allotted_date=%s, timeline_deadline=%s, submission_date=%s, comments=%s WHERE allotment_id=%s AND product_id=%s"
            values = (
                data["allotted_date"],
                data["timeline_deadline"],
                data["submission_date"],
                data["comments"],
                allotment_id,
                data["product_id"],
            )
            cursor.execute(update_query, values)
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            # Return the updated allotment content
            updated_allotment_content = {
                "allotment_id": allotment_id,
                "product_id": data["product_id"],
                "allotted_date": data["allotted_date"],
                "timeline_deadline": data["timeline_deadline"],
                "submission_date": data["submission_date"],
                "comments": data["comments"],
            }
            return jsonify(updated_allotment_content)

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error updating allotment content:", error)
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == "DELETE":
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            # Deleting the allotment content from the database
            delete_query = "DELETE FROM Allotment_Content WHERE allotment_id = %s"
            cursor.execute(delete_query, (allotment_id,))
            connection.commit()

            # Closing the cursor and connection
            cursor.close()
            connection.close()

            return jsonify({"message": "Allotment content deleted successfully"})

        except mysql.connector.Error as error:
            # Handling database errors
            print("Error deleting allotment content:", error)
            return jsonify({"error": "Database error occurred"}), 500


# # Backend Flask API for Allotment Photoshoot

@app.route("/api/allotment/photoshoot/<string:product_id>", methods=["GET"])
def get_allotment_photoshoots_by_product(product_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving allotment photoshoots for the given product_id from the database
        select_query = "SELECT * FROM Allotment_Photoshoot WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        allotment_photoshoots = cursor.fetchall()

        # Creating a list of allotment photoshoot dictionaries
        allotment_photoshoots_list = []
        for photoshoot in allotment_photoshoots:
            allotment_photoshoot_dict = {
                "allotment_id": photoshoot[0],
                "product_id": photoshoot[1],
                "allotted_date": photoshoot[2].isoformat() if photoshoot[2] else None,
                "timeline_deadline": photoshoot[3].isoformat() if photoshoot[3] else None,
                "submission_date": photoshoot[4].isoformat() if photoshoot[4] else None,
                "comments": photoshoot[5],
            }
            allotment_photoshoots_list.append(allotment_photoshoot_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the allotment photoshoots as a JSON response
        return jsonify(allotment_photoshoots_list)

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error retrieving allotment photoshoots:", error)
        return jsonify({"error": "Database error occurred"}), 500


# # Backend Flask APIs for Allotment Listing

@app.route("/api/allotment/listing/<string:product_id>", methods=["GET"])
def get_allotment_listings_by_product(product_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving allotment listings for the given product_id from the database
        select_query = "SELECT * FROM Allotment_Listing WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        allotment_listings = cursor.fetchall()

        # Creating a list of allotment listing dictionaries
        allotment_listings_list = []
        for listing in allotment_listings:
            allotment_listing_dict = {
                "allotment_id": listing[0],
                "product_id": listing[1],
                "allotted_date": listing[2].isoformat() if listing[2] else None,
                "timeline_deadline": listing[3].isoformat() if listing[3] else None,
                "submission_date": listing[4].isoformat() if listing[4] else None,
                "comments": listing[5],
            }
            allotment_listings_list.append(allotment_listing_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the allotment listings as a JSON response
        return jsonify(allotment_listings_list)

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error retrieving allotment listings:", error)
        return jsonify({"error": "Database error occurred"}), 500


# # Backend Flask APIs for Allotment Content

@app.route("/api/allotment/content/<string:product_id>", methods=["GET"])
def get_allotment_contents_by_product(product_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving allotment contents for the given product_id from the database
        select_query = "SELECT * FROM Allotment_Content WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        allotment_contents = cursor.fetchall()

        # Creating a list of allotment content dictionaries
        allotment_contents_list = []
        for content in allotment_contents:
            allotment_content_dict = {
                "allotment_id": content[0],
                "product_id": content[1],
                "allotted_date": content[2].isoformat() if content[2] else None,
                "timeline_deadline": content[3].isoformat() if content[3] else None,
                "submission_date": content[4].isoformat() if content[4] else None,
                "comments": content[5],
            }
            allotment_contents_list.append(allotment_content_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the allotment contents as a JSON response
        return jsonify(allotment_contents_list)

    except mysql.connector.Error as error:
        # Handling database errors
        print("Error retrieving allotment contents:", error)
        return jsonify({"error": "Database error occurred"}), 500

########################################Vendors#######################################


@app.route("/api/vendors/add", methods=["POST"])
def add_vendor():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the data into the database
        insert_query = "INSERT INTO Vendors (product_id, name, contact_email, contact_phone, company, details, attachment, rates, notes, comments, finalized) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            data["productId"],
            data["name"],
            data["contact_email"],
            data["contact_phone"],
            data["company"],
            data["details"],
            data["attachment"],
            data["rates"],
            data["notes"],
            data["comments"],
            data["finalized"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Getting the vendor_id of the newly added vendor
        vendor_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the newly added vendor as a JSON response
        new_vendor = {
            "vendor_id": vendor_id,
            "productId": data["productId"],
            "name": data["name"],
            "contact_email": data["contact_email"],
            "contact_phone": data["contact_phone"],
            "company": data["company"],
            "details": data["details"],
            "attachment": data["attachment"],
            "rates": data["rates"],
            "notes": data["notes"],
            "comments": data["comments"],
            "finalized": data["finalized"],
        }
        return jsonify(new_vendor)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/vendors/<int:product_id>", methods=["GET"])
def get_all_vendors(product_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all vendors for the given product_id from the database
        select_query = "SELECT * FROM Vendors WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        vendors = cursor.fetchall()

        # Creating a list of vendor dictionaries
        vendor_list = []
        for vendor in vendors:
            vendor_dict = {
                "vendor_id": vendor[0],
                # Change the index to 2 for the 'name' field
                "name": vendor[1],
                "contact_email": vendor[2],
                "contact_phone": vendor[3],
                "company": vendor[4],
                "details": vendor[5],
                "attachment": vendor[6],
                "rates": vendor[7],
                "notes": vendor[8],
                "comments": vendor[9],
                # Change the index to 11 for the 'finalized' field
                "finalized": vendor[10],
                # Change the index to 1 for the 'product_id' field
                "product_id": vendor[11],
            }
            vendor_list.append(vendor_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of vendors as a JSON response
        return jsonify(vendor_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/vendors/<int:vendor_id>", methods=["DELETE"])
def delete_vendor(vendor_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Deleting the vendor from the database
        delete_query = "DELETE FROM Vendors WHERE vendor_id = %s"
        cursor.execute(delete_query, (vendor_id,))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Vendor deleted successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/vendors/<int:vendor_id>/finalize", methods=["PUT"])
def finalize_vendor(vendor_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the finalized status of the vendor in the database
        update_query = "UPDATE Vendors SET finalized = %s WHERE vendor_id = %s"
        cursor.execute(update_query, (int(data["finalized"]), vendor_id))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Vendor finalized status updated successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/vendors/finalized/<int:product_id>", methods=["GET"])
def get_finalized_vendors(product_id):

    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all vendors for the given product_id from the database
        select_query = "SELECT * FROM Vendors WHERE product_id = %s AND finalized=1"
        cursor.execute(select_query, (product_id,))
        vendors = cursor.fetchall()

        # Creating a list of vendor dictionaries
        vendor_list = []
        for vendor in vendors:
            vendor_dict = {
                "vendor_id": vendor[0],
                # Change the index to 2 for the 'name' field
                "name": vendor[1],
                "contact_email": vendor[2],
                "contact_phone": vendor[3],
                "company": vendor[4],
                "details": vendor[5],
                "attachment": vendor[6],
                "rates": vendor[7],
                "notes": vendor[8],
                "comments": vendor[9],
                # Change the index to 11 for the 'finalized' field
                "finalized": vendor[10],
                # Change the index to 1 for the 'product_id' field
                "product_id": vendor[11],
            }
            vendor_list.append(vendor_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of vendors as a JSON response
        return jsonify(vendor_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500

########################### Vendor Details ######################################


@app.route("/api/vendorDetails/<int:vendor_id>", methods=["GET"])
def get_vendor_by_id(vendor_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving the vendor with the given vendor_id from the database
        select_query = "SELECT * FROM Vendors WHERE vendor_id = %s"
        cursor.execute(select_query, (vendor_id,))
        vendor = cursor.fetchone()

        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404

        # Creating a dictionary to represent the vendor
        vendor_dict = {
            "vendor_id": vendor[0],
            "product_id": vendor[11],
            "name": vendor[1],
            "contact_email": vendor[2],
            "contact_phone": vendor[3],
            "company": vendor[4],
            "details": vendor[5],
            "attachment": vendor[6],
            "rates": vendor[7],
            "notes": vendor[8],
            "comments": vendor[9],
            "finalized": vendor[10],
        }

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the vendor details as a JSON response
        return jsonify(vendor_dict)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


############################################### Shipment #############################################
# Helper function to establish a database connection


@app.route("/api/shipments/<int:vendor_id>", methods=["GET"])
def get_shipments(vendor_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all shipments for the given vendor_id from the database
        select_query = "SELECT * FROM Shipment WHERE vendor_id = %s"
        cursor.execute(select_query, (vendor_id,))
        shipments = cursor.fetchall()

        # Creating a list of shipment dictionaries
        shipment_list = []
        for shipment in shipments:
            shipment_dict = {
                "shipment_id": shipment[0],
                "vendor_id": shipment[1],
                "tracking_id": shipment[2],
                "dispatch": shipment[3],
                "tracker": shipment[4],
                "comments": shipment[5],
            }
            shipment_list.append(shipment_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of shipments as a JSON response
        return jsonify(shipment_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/shipments/add", methods=["POST"])
def add_shipment():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the data into the database
        insert_query = "INSERT INTO Shipment (vendor_id, tracking_id, dispatch, tracker, comments) VALUES (%s, %s, %s, %s, %s)"
        values = (
            data["vendor_id"],
            data["tracking_id"],
            data["dispatch"],
            data["tracker"],
            data["comments"]
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Getting the shipment_id of the newly added shipment
        shipment_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the newly added shipment as a JSON response
        new_shipment = {
            "shipment_id": shipment_id,
            "vendor_id": data["vendor_id"],
            "tracking_id": data["tracking_id"],
            "dispatch": data["dispatch"],
            "tracker": data["tracker"],
            "comments": data["comments"],
        }
        return jsonify(new_shipment)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/shipments/<int:shipment_id>", methods=["PUT"])
def update_shipment(shipment_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the shipment data in the database
        update_query = "UPDATE Shipment SET tracking_id = %s, dispatch = %s, tracker = %s, comments = %s WHERE shipment_id = %s"
        values = (
            data["tracking_id"],
            data["dispatch"],
            data["tracker"],
            data["comments"],
            shipment_id
        )
        cursor.execute(update_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Shipment updated successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/shipments/<int:shipment_id>", methods=["DELETE"])
def delete_shipment(shipment_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Deleting the shipment from the database
        delete_query = "DELETE FROM Shipment WHERE shipment_id = %s"
        cursor.execute(delete_query, (shipment_id,))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Shipment deleted successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


################################################ Payment ##############################################


@app.route("/api/payments/<int:vendor_id>", methods=["GET"])
def get_payments(vendor_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all payments for the given vendor_id from the database
        select_query = "SELECT * FROM Payment WHERE vendor_id = %s"
        cursor.execute(select_query, (vendor_id,))
        payments = cursor.fetchall()

        # Creating a list of payment dictionaries
        payment_list = []
        for payment in payments:
            payment_dict = {
                "payment_id": payment[0],
                "vendor_id": payment[1],
                "mail_sent": bool(payment[2]),
                "approval": bool(payment[3]),
                "upload_success": bool(payment[4]),
                "payment_date": str(payment[5]),
                "transaction_number": payment[6],
                "comments": payment[7],
            }
            payment_list.append(payment_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of payments as a JSON response
        return jsonify(payment_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/payments/add", methods=["POST"])
def add_payment():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the data into the database
        insert_query = "INSERT INTO Payment (vendor_id, mail_sent, approval, upload_success, payment_date, transaction_number, comments) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            data["vendor_id"],
            data["mail_sent"],
            data["approval"],
            data["upload_success"],
            data["payment_date"],
            data["transaction_number"],
            data["comments"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Getting the payment_id of the newly added payment
        payment_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the newly added payment as a JSON response
        new_payment = {
            "payment_id": payment_id,
            "vendor_id": data["vendor_id"],
            "mail_sent": data["mail_sent"],
            "approval": data["approval"],
            "upload_success": data["upload_success"],
            "payment_date": data["payment_date"],
            "transaction_number": data["transaction_number"],
            "comments": data["comments"],
        }
        return jsonify(new_payment)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/payments/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the payment data in the database
        update_query = "UPDATE Payment SET mail_sent = %s, approval = %s, upload_success = %s, payment_date = %s, transaction_number = %s, comments = %s WHERE payment_id = %s"
        values = (
            data["mail_sent"],
            data["approval"],
            data["upload_success"],
            data["payment_date"],
            data["transaction_number"],
            data["comments"],
            payment_id,
        )
        cursor.execute(update_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Payment updated successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/payments/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Deleting the payment from the database
        delete_query = "DELETE FROM Payment WHERE payment_id = %s"
        cursor.execute(delete_query, (payment_id,))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Payment deleted successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


###############################################  Receipt ################################################


@app.route("/api/receipts/add", methods=["POST"])
def add_receipt():
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Inserting the data into the database
        insert_query = "INSERT INTO Receipt (vendor_id, receipt_date, quantity_received, comments) VALUES (%s, %s, %s, %s)"
        values = (
            data["vendor_id"],
            data["receipt_date"],
            data["quantity_received"],
            data["comments"]
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Getting the receipt_id of the newly added receipt
        receipt_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the newly added receipt as a JSON response
        new_receipt = {
            "receipt_id": receipt_id,
            "vendor_id": data["vendor_id"],
            "receipt_date": data["receipt_date"],
            "quantity_received": data["quantity_received"],
            "comments": data["comments"],
        }
        return jsonify(new_receipt)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


# API endpoint to update a receipt
@app.route("/api/receipts/<int:receipt_id>", methods=["PUT"])
def update_receipt(receipt_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the receipt in the database
        update_query = "UPDATE Receipt SET receipt_date = %s, quantity_received = %s, comments = %s WHERE receipt_id = %s"
        values = (
            data["receipt_date"],
            data["quantity_received"],
            data["comments"],
            receipt_id
        )
        cursor.execute(update_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Receipt updated successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


# API endpoint to delete a receipt
@app.route("/api/receipts/<int:receipt_id>", methods=["DELETE"])
def delete_receipt(receipt_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Deleting the receipt from the database
        delete_query = "DELETE FROM Receipt WHERE receipt_id = %s"
        cursor.execute(delete_query, (receipt_id,))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Receipt deleted successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


# API endpoint to fetch all receipts
@app.route("/api/receipts/<int:vendor_id>", methods=["GET"])
def get_all_receipts(vendor_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all receipts from the database
        select_query = "SELECT * FROM Receipt where vendor_id=%s"
        cursor.execute(select_query, (vendor_id,))
        receipts = cursor.fetchall()

        # Creating a list of receipt dictionaries
        receipt_list = []
        for receipt in receipts:
            receipt_dict = {
                "receipt_id": receipt[0],
                "vendor_id": receipt[1],
                "receipt_date": receipt[2].strftime("%Y-%m-%d"),
                "quantity_received": receipt[3],
                "comments": receipt[4],
            }
            receipt_list.append(receipt_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of receipts as a JSON response
        return jsonify(receipt_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500

###################################### Notes Manager #######################################################


@app.route("/api/notes/<int:product_id>", methods=["GET"])
def get_notes(product_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Retrieving all notes for the given product_id from the database
        select_query = "SELECT * FROM Notes WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        notes = cursor.fetchall()

        # Creating a list of note dictionaries
        note_list = []
        for note in notes:
            note_dict = {
                "note_id": note[0],
                "product_id": note[1],
                "title": note[2],
                "note": note[3],
            }
            note_list.append(note_dict)

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the list of notes as a JSON response
        return jsonify(note_list)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/notes/add/<int:product_id>", methods=["POST"])
def add_note(product_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        print(data)
        # Inserting the data into the database
        insert_query = "INSERT INTO Notes (product_id, title, note) VALUES (%s, %s, %s)"
        values = (
            product_id,
            data["title"],
            data["note"],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        # Getting the note_id of the newly added note
        note_id = cursor.lastrowid

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning the newly added note as a JSON response
        new_note = {
            "note_id": note_id,
            "product_id": data["product_id"],
            "title": data["title"],
            "note": data["note"],
        }
        return jsonify(new_note)

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Updating the note data in the database
        update_query = "UPDATE Notes SET title = %s, note = %s WHERE note_id = %s"
        values = (
            data["title"],
            data["note"],
            note_id
        )
        cursor.execute(update_query, values)
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Note updated successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Deleting the note from the database
        delete_query = "DELETE FROM Notes WHERE note_id = %s"
        cursor.execute(delete_query, (note_id,))
        connection.commit()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # Returning a success message as a JSON response
        return jsonify({"message": "Note deleted successfully"})

    except mysql.connector.Error as error:
        # Handling database errors
        return jsonify({"error": "Database error occurred"}), 500


########################### Product Status ################################

############################ Monthly Metrics ######################
# Assuming you have imported necessary libraries and set up the Flask app

@app.route('/api/product/monthly-metrics/<int:product_id>', methods=['GET'])
def get_product_monthly_metrics(product_id):
    try:
        # Replace the following lines with your database query to fetch monthly metrics for the given product_id
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM ProductMonthlyMetrics WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        monthly_metrics = cursor.fetchall()

        cursor.close()
        connection.close()

        # Convert the result into a list of dictionaries
        monthly_metrics_list = [
            {
                'metric_id': metric[0],
                'product_id': metric[1],
                'month': metric[2],
                'year': metric[3],
                'spent_amount': float(metric[4]),
                'revenue_amount': float(metric[5]),
            }
            for metric in monthly_metrics
        ]
        return jsonify(monthly_metrics_list)
    except Exception as e:
        print('Error fetching product monthly metrics:', e)
        return jsonify({"error": "Error fetching product monthly metrics"}), 500


@app.route('/api/product/monthly-metrics/<int:product_id>', methods=['POST'])
def add_product_monthly_metrics(product_id):
    try:
        data = request.get_json()
        # Replace the following lines with your database query to add the new monthly metrics
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        print(data)

        insert_query = "INSERT INTO ProductMonthlyMetrics (product_id, month, year, spent_amount, revenue_amount) VALUES (%s, %s, %s, %s, %s)"
        values = (
            product_id,
            data['month'],
            data['year'],
            data['spent_amount'],
            data['revenue_amount'],
        )
        cursor.execute(insert_query, values)
        connection.commit()

        cursor.close()
        connection.close()

        new_metric_id = cursor.lastrowid
        new_metric = {
            'metric_id': new_metric_id,
            'product_id': data['product_id'],
            'month': data['month'],
            'year': data['year'],
            'spent_amount': float(data['spent_amount']),
            'revenue_amount': float(data['revenue_amount']),
        }
        return jsonify(new_metric)
    except Exception as e:
        print('Error adding product monthly metrics:', e)
        return jsonify({"error": "Error adding product monthly metrics"}), 500


@app.route('/api/product/monthly-metrics/<int:metric_id>', methods=['PUT'])
def handle_specific_product_monthly_metrics(metric_id):
    try:
        if request.method == 'PUT':
            data = request.get_json()
            # Replace the following lines with your database query to update the specific monthly metrics
            connection = connection_pool.get_connection()
            cursor = connection.cursor()

            update_query = "UPDATE ProductMonthlyMetrics SET month=%s, year=%s, spent_amount=%s, revenue_amount=%s WHERE metric_id=%s"
            values = (
                data['month'],
                data['year'],
                data['spent_amount'],
                data['revenue_amount'],
                metric_id,
            )
            cursor.execute(update_query, values)
            connection.commit()

            cursor.close()
            connection.close()

            updated_metric = {
                'metric_id': metric_id,
                'month': data['month'],
                'year': data['year'],
                'spent_amount': float(data['spent_amount']),
                'revenue_amount': float(data['revenue_amount']),
            }
            return jsonify(updated_metric)

    except Exception as e:
        print('Error handling specific product monthly metrics:', e)
        return jsonify({"error": "Error handling specific product monthly metrics"}), 500

# Assuming you have imported necessary libraries and set up the Flask app


@app.route('/api/product/monthly-metrics/<int:metric_id>', methods=['DELETE'])
def delete_product_monthly_metrics(metric_id):
    try:
        # Replace the following lines with your database query to delete the specific monthly metrics
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM ProductMonthlyMetrics WHERE metric_id = %s"
        cursor.execute(delete_query, (metric_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Product monthly metrics deleted successfully"})
    except Exception as e:
        print('Error deleting product monthly metrics:', e)
        return jsonify({"error": "Error deleting product monthly metrics"}), 500


############################# Product Status ######################

# Assuming you have imported necessary libraries and set up the Flask app

# Assuming you have imported necessary libraries and set up the Flask app

@app.route('/api/product/status/<int:product_id>', methods=['GET'])
def get_product_status(product_id):
    try:
        # Replace the following lines with your database query to fetch the product status for the given product_id
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM Products WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        status = cursor.fetchone()

        cursor.close()
        connection.close()

        # Convert the result into a dictionary
        if status:
            product_status = {
                'product_id': status[1],
                'is_assigned_for_advertising': bool(status[3]),
                'is_live': bool(status[4]),
            }
            return jsonify(product_status)
        else:
            return jsonify({"error": "Product status not found"}), 404
    except Exception as e:
        print('Error fetching product status:', e)
        return jsonify({"error": "Error fetching product status"}), 500


@app.route('/api/product/status/<int:product_id>', methods=['PUT'])
def update_product_status(product_id):
    try:
        data = request.get_json()
        # Replace the following lines with your database query to update the product status for the given product_id
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        update_query = "UPDATE Products SET is_assigned_for_advertising=%s, is_live=%s WHERE product_id=%s"
        values = (
            data['is_assigned_for_advertising'],
            data['is_live'],
            product_id,
        )
        cursor.execute(update_query, values)
        connection.commit()

        cursor.close()
        connection.close()

        updated_status = {
            'product_id': product_id,
            'is_assigned_for_advertising': bool(data['is_assigned_for_advertising']),
            'is_live': bool(data['is_live']),
        }
        return jsonify(updated_status)
    except Exception as e:
        print('Error updating product status:', e)
        return jsonify({"error": "Error updating product status"}), 500

############################ Charts ##############################

# Assuming you have imported necessary libraries and set up the Flask app


@app.route('/api/year-options', methods=['GET'])
def get_year_options():
    try:
        # Fetch the available years from the ProductMonthlyMetrics table in the database
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        query = "SELECT DISTINCT year FROM ProductMonthlyMetrics ORDER BY year DESC"
        cursor.execute(query)
        years = [year[0] for year in cursor.fetchall()]

        cursor.close()
        connection.close()

        return jsonify(years)

    except Exception as e:
        print('Error fetching year options:', e)
        return jsonify({"error": "Error fetching year options"}), 500

 # Assuming you have imported necessary libraries and set up the Flask app


@app.route('/api/monthly-metrics', methods=['GET'])
def get_monthly_metrics():
    try:
        # Get the selected year from the query parameters
        selected_year = request.args.get('year', type=int)

        # Fetch the monthly metrics data for the selected year from the ProductMonthlyMetrics table in the database
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        query = "SELECT month, year, spent_amount, revenue_amount FROM ProductMonthlyMetrics WHERE year = %s ORDER BY month"
        cursor.execute(query, (selected_year,))
        monthly_metrics = cursor.fetchall()

        cursor.close()
        connection.close()

        # Convert the query result to a list of dictionaries
        monthly_data = [
            {
                "month": entry[0],
                "year": entry[1],
                "spent_amount": entry[2],
                "revenue_amount": entry[3]
            }
            for entry in monthly_metrics
        ]

        return jsonify(monthly_data)

    except Exception as e:
        print('Error fetching monthly metrics:', e)
        return jsonify({"error": "Error fetching monthly metrics"}), 500


################################### Sign IN ########################################


# MySQL Database Configuration


def get_user_by_email(email):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        print(email)
        query = "SELECT * FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return None


def verify_password(password, hashed_password):
    return password == hashed_password


@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # if email not in data or password not in data:
    #     return jsonify({'message': 'Username and password are required.'}), 400
    
    user = get_user_by_email(email)
    
    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    # Assuming the password hash is stored in the fourth column (index 3)
    if verify_password(password, user[3]):
        # Authentication successful, you can generate a token or session here if needed
        print("verified")
        return jsonify({'message': 'Authentication successful.','username':user[1]}), 200
    else:
        return jsonify({'message': 'Invalid credentials.'}), 401


################################### Sign UP #########################################


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Check if the username or email already exists
        query = 'SELECT * FROM Users WHERE username = %s OR email = %s'
        cursor.execute(query, (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 409

        # Insert the new user into the database
        insert_query = 'INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)'
        cursor.execute(insert_query, (username, email, password))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Sign up successful'}), 200

    except mysql.connector.Error as error:
        print('Error creating new user:', error)
        return jsonify({'error': 'Database error occurred'}), 500


if __name__ == "__main__":
    app.run()
