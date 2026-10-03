from app.database.queries import add_customer, get_customers


try:
    customer_id = add_customer(
        demand=10,
        earliest=8,
        latest=12,
        service_time=0.25,
        latitude=12.9716,
        longitude=77.5946
    )

    print("Added customer ID:", customer_id)

    customers = get_customers()

    print("Customers:", customers)

except Exception as error:
    print("Database operation failed:")
    print(error)