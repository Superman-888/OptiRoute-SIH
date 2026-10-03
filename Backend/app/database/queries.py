from app.database.connection import get_connection


def get_vehicles():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    vehicle_id,
                    capacity
                FROM vehicles
                ORDER BY vehicle_id;
            """)

            return cursor.fetchall()

    finally:
        conn.close()


def add_vehicle(capacity):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO vehicles (capacity)
                VALUES (%s)
                RETURNING vehicle_id, capacity;
            """, (capacity,))

            vehicle = cursor.fetchone()

            conn.commit()

            return vehicle

    finally:
        conn.close()


def get_customers():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    customer_id,
                    demand,
                    earliest,
                    latest,
                    service_time,
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude
                FROM customers
                ORDER BY customer_id;
            """)

            return cursor.fetchall()

    finally:
        conn.close()


def get_customers_by_ids(customer_ids):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    customer_id,
                    demand,
                    earliest,
                    latest,
                    service_time,
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude
                FROM customers
                WHERE customer_id = ANY(%s)
                ORDER BY customer_id;
            """, (customer_ids,))

            return cursor.fetchall()

    finally:
        conn.close()


def add_customer(
    demand,
    earliest,
    latest,
    service_time,
    latitude,
    longitude
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO customers
                    (
                        demand,
                        earliest,
                        latest,
                        service_time,
                        location
                    )
                VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        ST_SetSRID(
                            ST_MakePoint(%s, %s),
                            4326
                        )
                    )
                RETURNING customer_id;
            """, (
                demand,
                earliest,
                latest,
                service_time,
                longitude,
                latitude
            ))

            customer_id = cursor.fetchone()[0]

            conn.commit()

            return customer_id

    finally:
        conn.close()


def save_route(
    vehicle_id,
    route_sequence,
    total_distance,
    total_time,
    total_traffic_cost,
    fitness
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO routes
                    (
                        vehicle_id,
                        route_sequence,
                        total_distance,
                        total_time,
                        total_traffic_cost,
                        fitness
                    )
                VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                RETURNING route_id;
            """, (
                vehicle_id,
                route_sequence,
                total_distance,
                total_time,
                total_traffic_cost,
                fitness
            ))

            route_id = cursor.fetchone()[0]

            conn.commit()

            return route_id

    finally:
        conn.close()