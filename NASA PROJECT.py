import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime



conn = mysql.connector.connect(host = "localhost",user = "root",password = "12345",database = "my_database")
curr = conn.cursor()
conn.commit()

if __name__ == "__main__":
    st.title(":red[NASA EARTH OBJECT TRACKING🚀]")


page = st.sidebar.radio("Navigation", ( "Queries📝", "Filters🔎"))

if page == "Queries📝":
    st.title("Asteroid Approaches")

query = st.selectbox("Choose a query", [
        "1. Count how many times each asteroid has approached Earth",
        "2. Average velocity of each asteroid over multiple approaches",
        "3. List top 10 fastest asteroids",
        "4. Find potentially hazardous asteroids that have approached Earth more than 3 times",
        "5. Find the month with the most asteroid approaches",
        "6. Get the asteroid with the fastest ever approach speed",
        "7. Sort asteroids by maximum estimated diameter (descending)",
        "8. An asteroid whose closest approach is getting nearer over time (Hint: Use ORDER BY close_approach_date and look at miss_distance)",
        "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
        "10. List names of asteroids that approached Earth with velocity > 50,000 km/h",
        "11. Count how many approaches happened per month",
        "12. Find asteroid with the highest brightness",
        "13. Get number of hazardous vs non-hazardous asteroids",
        "14. Find asteroids that passed closer than the Moon along with their close approach date and distance",
        "15. Find asteroids that came within 0.05 AU",
        "16. Find the asteroids that has the earliest recorded close approach date to earth",
        "17. List the average estimated diameter of all asteroids",
        "18. count the number of asteroid approaches recorded per year",
        "19. list the top three month with the highest average approach velocity of asteroids"
    ])

if query == "1. Count how many times each asteroid has approached Earth":
        curr.execute ("""
            select a.name, count(ca.neo_reference_id) as number_of_approaches
            from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            group by a.name
            LIMIT 100;           
        """)
        result = curr.fetchall()
        df = pd.DataFrame(result,columns=['name','approach_count'])
        st.dataframe(df)
    
elif query == "2. Average velocity of each asteroid over multiple approaches":
        curr.execute("""
            select a.name, count(ca.neo_reference_id) as number_of_approaches
            from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            group by a.name
            LIMIT 100;
        """)
        result = curr.fetchall()
        df = pd.DataFrame(result,columns=['name','average_velocity'])
        st.dataframe(df)

elif query == "3. List top 10 fastest asteroids":
        curr.execute("""
            select a.name, ca.relative_velocity_kmph
            from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            order by ca.relative_velocity_kmph DESC
            LIMIT 10;
        """)
        result = curr.fetchall()
        df = pd.DataFrame(result,columns=['name','relative_velocity_kmph'])
        st.dataframe(df)

elif query == "4. Find potentially hazardous asteroids that have approached Earth more than 3 times":
        curr.execute("""
            select a.name, count(ca.neo_reference_id) as number_of_approaches
            from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            WHERE a.is_potentially_hazardous_asteroid = "true"
            group by a.name
            HAVING count(ca.neo_reference_id) > 3
            LIMIT 100;
        """)
        result = curr.fetchall()
        df = pd.DataFrame(result,columns=['name','approach_count'])
        st.dataframe(df)

elif query == "5. Find the month with the most asteroid approaches":
        curr.execute("""
            select MONTH(ca.neo_reference_id) as number_of_approaches
            from close_approach ca
            group by approach_month
            order by approach_count DESC
            LIMIT 1;  
        """)
        result = curr.fetchall()
        df = pd.DataFrame(result,columns=['month','approach_count'])
        st.dataframe(df)

elif query == "6. Get the asteroid with the fastest ever approach speed":
    curr.execute("""
            select a.name, MAX(ca.relative_velocity_kmph) as max_velocity
            from asteroids a
            join close_approach ca on a.id = ca.neo_reference_id
            group by a.name
            order by max_velocity DESC
            LIMIT 1;
        """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','max_velocity'])
    st.dataframe(df)

elif query == "7. Sort asteroids by maximum estimated diameter (descending)":
    curr.execute("""
            select name, estimated_diameter_max_km AS max_diameter
            from asteroids a
            order by estimated_diameter_max_km DESC
            LIMIT 100;
        """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','max_diameter'])
    st.dataframe(df)

elif query == "8. An asteroid whose closest approach is getting nearer over time (Hint: Use ORDER BY close_approach_date and look at miss_distance)":
    curr.execute("""
            SELECT
                a.name,
                ca.close_approach_date,
                ca.miss_distance_km,
                
            FROM
                asteroids a
            JOIN
                close_approach ca ON a.id = ca.neo_reference_id
            ORDER BY
                a.name, ca.close_approach_date   
            LIMIT 100;
        """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','close_approach_date','miss_distance_km'])
    st.dataframe(df)

elif query == "9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
    curr.execute("""
            SELECT DISTINCT
                a.name,
                ca.close_approach_date,
                ca.miss_distance_km
            FROM
                asteroids a
            JOIN
                close_approach ca ON a.id = ca.neo_reference_id
            WHERE
                ca.miss_distance_km =(
                    select min(ca2.miss_distance_km)
                    from close_approach ca2
                    where ca2.neo_reference_id = a.id 
                    )
                    LIMIT 100;
        """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','close_approach_date','miss_distance'])
    st.dataframe(df)

elif query == "10. List names of asteroids that approached Earth with velocity > 50,000 km/h":
    curr.execute("""
        SELECT DISTINCT
            a.name,
            ca.relative_velocity_kmph
        FROM
            asteroids a
        JOIN
            close_approach ca ON a.id = ca.neo_reference_id
        WHERE
            ca.relative_velocity_kmph > 50000
            LIMIT 100;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name'])
    st.dataframe(df)

elif query == "11. Count how many approaches happened per month":
    curr.execute("""
        SELECT
            MONTH(ca.close_approach_date) AS approach_month,
            MONTHNAME(ca.close_approach_date) AS approach_month_name,
            COUNT(*) AS number_of_approaches
        FROM
            close_approach ca
        GROUP BY
            approach_month, approach_month_name
        ORDER BY
            approach_month;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['month','approach_count'])
    st.dataframe(df)

elif query == "12. Find asteroid with the highest brightness":
    curr.execute("""
        SELECT
            name,
            absolute_magnitude_h
        FROM
            asteroids
        ORDER BY
            absolute_magnitude_h ASC
            LIMIT 1;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','max_brightness'])
    st.dataframe(df)

elif query == "13. Get number of hazardous vs non-hazardous asteroids":
    curr.execute("""
        SELECT
            CASE is_potentially_hazardous_asteroid
            WHEN 1 THEN 'Hazardous'
            ELSE 'Non-Hazardous'
            END AS hazard_status,
            COUNT(*) AS number_of_asteroids
        FROM
            asteroids
        GROUP BY
            hazard_status
            LIMIT 100;

     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['hazardous','count'])
    st.dataframe(df)

elif query == "14. Find asteroids that passed closer than the Moon along with their close approach date and distance":
    curr.execute("""
        SELECT
            a.name,
            ca.close_approach_date,
            ca.miss_distance_km
        FROM
            asteroids a
        JOIN
            close_approach ca ON a.id = ca.neo_reference_id
        WHERE
            ca.miss_distance_km < 384400
            LIMIT 100;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','close_approach_date','miss_distance'])
    st.dataframe(df)

elif query == "15. Find asteroids that came within 0.05 AU":
    curr.execute("""
        SELECT
            a.name,
            ca.close_approach_date,
            ca.astronomical
        FROM
            asteroids a
        JOIN
            close_approach ca ON a.id = ca.neo_reference_id
        WHERE
            ca.astronomical < 0.05
            LIMIT 100;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','close_approach_date','miss_distance'])
    st.dataframe(df)

elif query == "16. Find the asteroids that has the earliest recorded close approach date to earth":
    curr.execute("""
        SELECT
            a.name,
            ca.close_approach_date
        FROM
            asteroids a
        JOIN
            close_approach ca ON a.id = ca.neo_reference_id
        ORDER BY
            ca.close_approach_date ASC
            LIMIT 100;  
    """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['name','earliest_date'])
    st.dataframe(df)

elif query == "17. List the average estimated diameter of all asteroids":
    curr.execute("""
        SELECT
            AVG(estimated_diameter_max_km) AS average_max_diameter_km
        FROM
            asteroids;
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['average_diameter'])
    st.dataframe(df)

elif query == "18. count the number of asteroid approaches recorded per year":
    curr.execute("""
        SELECT
            YEAR(ca.close_approach_date) AS approach_year,
            COUNT(*) AS number_of_approaches
        FROM
            close_approach ca
        GROUP BY
            approach_year
        ORDER BY
            approach_year;  
    
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['year','approach_count'])
    st.dataframe(df)

elif query == "19. list the top three month with the highest average approach velocity of asteroids":
    curr.execute("""
        SELECT
            MONTHNAME(ca.close_approach_date) AS approach_month,
            AVG(ca.relative_velocity_kmph) AS average_velocity
        FROM
            close_approach ca
        GROUP BY
            approach_month
        ORDER BY
            average_velocity DESC
            LIMIT 3; 
     """)
    result = curr.fetchall()
    df = pd.DataFrame(result,columns=['month','average_velocity'])
    st.dataframe(df)

if page == "Filters🔎":
    st.title("Filtered Approaches")
    dia_min_range = st.slider("Min Estimated Diameter (km)", 0.0, 20.0, (0.0, 10.0))
    dia_max_range = st.slider("Max Estimated Diameter (km)", 0.0, 20.0, (0.0, 10.0))
    vel_range = st.slider("Relative Velocity (km/h)", 0.0,1000.0, (0.0, 200.0))
    au_range = st.slider("Astronomical Unit", 0.0, 1.0,(0.0, 1.0))
    start_date = st.date_input("Start Date", datetime(2024, 1, 1))
    end_date = st.date_input("End Date", datetime(2025, 4, 13))

    if st.button("Filter"):
        query = """
            SELECT * FROM ASTEROIDS
            inner join close_approach
            on asteroids.id = close_approach.neo_reference_id
            WHERE ASTEROIDS.estimated_diameter_min_km  BETWEEN %s AND %s
            AND ASTEROIDS.estimated_diameter_max_km BETWEEN %s AND  %s
            AND CLOSE_APPROACH.relative_velocity_kmph BETWEEN %s AND %s
            AND CLOSE_APPROACH.astronomical BETWEEN %s AND %s
            AND CLOSE_APPROACH.close_approach_date BETWEEN %s AND %s LIMIT 100;
            """
        params = (dia_min_range[0], dia_min_range[1],
                  dia_max_range[0], dia_max_range[1],
                  vel_range[0], vel_range[1],
                  au_range[0], au_range[1],
                  start_date, end_date)
        print(query)
        conn.ping(reconnect = True)
        curr.execute(query, params)
        result = curr.fetchall()
        df = pd.DataFrame(result, columns=[i[0] for i in curr.description])
        st.dataframe(df)

dataset = st.selectbox("choose a dataset", ["Asteroids🌠", "Close_approach🛰️"])

if dataset == "Asteroids🌠":
        curr.execute("select * from Asteroids")
        result = curr.fetchall()
        df = pd.DataFrame(result, columns=[i[0] for i in curr.description])
        st.dataframe(df)
        

elif dataset == "Close_approach🛰️":
        curr.execute("select * from Close_approach")
        result = curr.fetchall()
        df = pd.DataFrame(result, columns=[i[0] for i in curr.description])
        st.dataframe(df)
        





