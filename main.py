import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(host="my_postgres",
                            database='meteo_db',
                            user="robert",
                            password="student",
                            port=5432)
    return conn

# Ruta pentru adaugarea unei tari în baza de date
@app.route('/api/countries', methods=['POST'])
def post_country():
    try:
        data = request.get_json()

        if 'nume' not in data or 'lat' not in data or 'lon' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tari WHERE nume_tara = %s;", (data['nume'],))
        country_exists = cursor.fetchone()

        if country_exists:
            conn.close()
            return jsonify({'error': 'Tara deja existenta'}), 409

        cursor.execute("INSERT INTO Tari (nume_tara, latitudine, longitudine) VALUES (%s, %s, %s) RETURNING id;",
                       (data['nume'], data['lat'], data['lon']))

        country_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return jsonify({'id': country_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea tuturor tarilor din baza de date
@app.route('/api/countries', methods=['GET'])
def get_countries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nume_tara, latitudine, longitudine FROM Tari;")
        countries = cursor.fetchall()

        conn.close()

        countries_list = [{'id': country[0], 'nume': country[1], 'lat': country[2], 'lon': country[3]} for country in countries]

        return jsonify(countries_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru modificarea unei tari în baza de date
@app.route('/api/countries/<int:id>', methods=['PUT'])
def put_country(id):
    try:
        data = request.get_json()

        if 'nume' not in data or 'lat' not in data or 'lon' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tari WHERE id = %s;", (id,))
        country_exists = cursor.fetchone()

        if not country_exists:
            conn.close()
            return jsonify({'error': 'Tara nu a fost gasita'}), 404

        cursor.execute("UPDATE Tari SET id = %s, nume_tara = %s, latitudine = %s, longitudine = %s WHERE id = %s;",
                       (data['id'], data['nume'], data['lat'], data['lon'], id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Tara modificata cu success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Ruta pentru stergerea unei tari din baza de date
@app.route('/api/countries/<int:id>', methods=['DELETE'])
def delete_country(id):
    try:
        if id is None:
            return jsonify({'error': 'Id invalid'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tari WHERE id = %s;", (id,))
        country_exists = cursor.fetchone()

        if not country_exists:
            conn.close()
            return jsonify({'error': 'Tara nu a fost gasita'}), 404

        cursor.execute("DELETE FROM Tari WHERE id = %s;", (id,))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Tara stearsa cu success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
# Ruta pentru adaugarea unui oras în baza de date
@app.route('/api/cities', methods=['POST'])
def post_city():
    try:
        data = request.get_json()

        if 'idTara' not in data or 'nume' not in data or 'lat' not in data or 'lon' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("SELECT id FROM Tari WHERE id = %s;", (data['idTara'],))
        country_exists = cursor.fetchone()

        if not country_exists:
            conn.close()
            return jsonify({'error': 'Tara nu a fost gasita'}), 404

        cursor.execute("SELECT id FROM Orase WHERE id_tara = %s AND nume_oras = %s;", (data['idTara'], data['nume']))
        city_exists = cursor.fetchone()

        if city_exists:
            conn.close()
            return jsonify({'error': 'Orasul exista'}), 409

        cursor.execute("INSERT INTO Orase (id_tara, nume_oras, latitudine, longitudine) VALUES (%s, %s, %s, %s) RETURNING id;",
                       (data['idTara'], data['nume'], data['lat'], data['lon']))

        city_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return jsonify({'id': city_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea tuturor oraselor din baza de date
@app.route('/api/cities', methods=['GET'])
def get_cities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, id_tara, nume_oras, latitudine, longitudine FROM Orase;")
        cities = cursor.fetchall()

        conn.close()

        cities_list = [{'id': city[0], 'idTara': city[1], 'nume': city[2], 'lat': city[3], 'lon': city[4]} for city in cities]

        return jsonify(cities_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea oraselor care apartin de o tara specificata
@app.route('/api/cities/country/<int:id_tara>', methods=['GET'])
def get_cities_by_country(id_tara):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Tari WHERE id = %s;", (id_tara,))
        existing_country = cursor.fetchone()

        if not existing_country:
            conn.close()
            return jsonify({'error': 'Tara nu a fost gasita'}), 404

        cursor.execute("SELECT id, id_tara, nume_oras, latitudine, longitudine FROM Orase WHERE id_tara = %s;", (id_tara,))
        cities = cursor.fetchall()

        conn.close()

        cities_list = [{'id': city[0], 'idTara': city[1], 'nume': city[2], 'lat': city[3], 'lon': city[4]} for city in cities]

        return jsonify(cities_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru modificarea unui oras în baza de date
@app.route('/api/cities/<int:id>', methods=['PUT'])
def put_city(id):
    try:
        data = request.get_json()

        if 'idTara' not in data or 'nume' not in data or 'lat' not in data or 'lon' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Orase WHERE id = %s;", (id,))
        city_exists = cursor.fetchone()

        if not city_exists:
            conn.close()
            return jsonify({'error': 'Orasul nu exista'}), 404

        cursor.execute("SELECT id FROM Orase WHERE id_tara = %s AND nume_oras = %s AND id != %s;",
                       (data['idTara'], data['nume'], id))
        city_exists = cursor.fetchone()

        if city_exists:
            conn.close()
            return jsonify({'error': 'Orasul exista deja in tara specificata'}), 409

        cursor.execute("UPDATE Orase SET id = %s, id_tara = %s, nume_oras = %s, latitudine = %s, longitudine = %s WHERE id = %s;",
                       (data['id'], data['idTara'], data['nume'], data['lat'], data['lon'], id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Oras modificat cu succes'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Ruta pentru stergerea unui oras din baza de date
@app.route('/api/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    try:
        if id is None:
            return jsonify({'error': 'Id invalid'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Orase WHERE id = %s;", (id,))
        city_exists = cursor.fetchone()

        if not city_exists:
            conn.close()
            return jsonify({'error': 'Orasul nu exista'}), 404

        cursor.execute("DELETE FROM Orase WHERE id = %s;", (id,))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Oras sters cu succes'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Ruta pentru adaugarea unei temperaturi in baza de date
@app.route('/api/temperatures', methods=['POST'])
def post_temperature():
    try:
        data = request.get_json()

        if 'idOras' not in data or 'valoare' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("SELECT id FROM Orase WHERE id = %s;", (data['idOras'],))
        existing_city = cursor.fetchone()

        if not existing_city:
            conn.close()
            return jsonify({'error': 'Orasul nu a fost gasit'}), 404

        cursor.execute("SELECT id FROM Temperaturi WHERE id_oras = %s AND timestamp = CURRENT_TIMESTAMP;",
                       (data['idOras'],))
        existing_temperature = cursor.fetchone()

        if existing_temperature:
            conn.close()
            return jsonify({'error': 'Temperatura deja existenta'}), 409

        cursor.execute("INSERT INTO Temperaturi (id_oras, valoare) VALUES (%s, %s) RETURNING id;",
                       (data['idOras'], data['valoare']))

        temperature_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return jsonify({'id': temperature_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea tuturor temperaturilor din baza de date
@app.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        date_start = request.args.get('from')
        date_end = request.args.get('until')

        conn = get_db_connection()
        cursor = conn.cursor()

        if lat:
            cursor.execute("SELECT id, valoare, timestamp FROM Temperaturi WHERE id_oras IN "
                           "(SELECT id FROM Orase WHERE latitudine = %s);",
                           (lat,))
        if lon:
            cursor.execute("SELECT id, valoare, timestamp FROM Temperaturi WHERE id_oras IN "
                           "(SELECT id FROM Orase WHERE longitudine = %s);",
                           (lon,))
        if date_start:
            cursor.execute("SELECT id, valoare, timestamp FROM Temperaturi WHERE timestamp >= %s;",
                           (date_start,))

        if date_end:
            cursor.execute("SELECT id, valoare, timestamp FROM Temperaturi WHERE timestamp <= %s;",
                           (date_end,))
    
        if lat is None and lon is None and date_start is None and date_end is None:
            cursor.execute("SELECT id, valoare, timestamp FROM Temperaturi;")

        temperatures = cursor.fetchall()
        conn.close()

        temperatures_list = [{'id': temp[0], 'valoare': temp[1], 'timestamp': temp[2]} for temp in temperatures]

        return jsonify(temperatures_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea temperaturilor dintr-un oras dat
@app.route('/api/temperatures/cities/<int:id_oras>', methods=['GET'])
def get_temperatures_by_city(id_oras):
    try:
        date_start = request.args.get('from')
        date_end = request.args.get('until')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT id, valoare, timestamp FROM Temperaturi WHERE id_oras = %s"
        params = [id_oras]

        if date_start:
            query += " AND timestamp >= to_timestamp(%s) AT TIME ZONE 'UTC'"
            params.append(date_start)
        if date_end:
            query += " AND timestamp <= to_timestamp(%s) AT TIME ZONE 'UTC'"
            params.append(date_end)

        cursor.execute(query, tuple(params))
        temperatures = cursor.fetchall()

        conn.close()

        temperatures_list = [{'id': temp[0], 'valoare': temp[1], 'timestamp': temp[2]} for temp in temperatures]

        return jsonify(temperatures_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru obtinerea temperaturilor dintr-o tara data
@app.route('/api/temperatures/countries/<int:id_tara>', methods=['GET'])
def get_temperatures_by_country(id_tara):
    try:
        date_start = request.args.get('from')
        date_end = request.args.get('until')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT Temperaturi.id, Temperaturi.valoare, Temperaturi.timestamp " \
                "FROM Temperaturi " \
                "JOIN Orase ON Temperaturi.id_oras = Orase.id " \
                "WHERE Orase.id_tara = %s"

        params = [id_tara]

        if date_start:
            query += " AND Temperaturi.timestamp >= to_timestamp(%s) AT TIME ZONE 'UTC'"
            params.append(date_start)
        if date_end:
            query += " AND Temperaturi.timestamp <= to_timestamp(%s) AT TIME ZONE 'UTC'"
            params.append(date_end)

        cursor.execute(query, tuple(params))
        temperatures = cursor.fetchall()

        conn.close()

        temperatures_list = [{'id': temp[0], 'valoare': temp[1], 'timestamp': temp[2]} for temp in temperatures]

        return jsonify(temperatures_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Ruta pentru modificarea unei temperaturi in baza de date
@app.route('/api/temperatures/<int:id>', methods=['PUT'])
def put_temperature(id):
    try:
        data = request.get_json()

        if 'idOras' not in data or 'valoare' not in data:
            return jsonify({'error': 'Date incomplete'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Temperaturi WHERE id = %s;", (id,))
        temperature = cursor.fetchone()
        conn.close()

        if not temperature:
            return jsonify({'error': 'Temperatura nu exista in baza de date'}), 404

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE Temperaturi SET id_oras = %s, valoare = %s WHERE id = %s;",
                       (data['idOras'], data['valoare'], id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Temperatura modificata cu success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Ruta pentru stergerea unei temperaturi din baza de date
@app.route('/api/temperatures/<int:id>', methods=['DELETE'])
def delete_temperature(id):
    try:
        if id is None:
            return jsonify({'error': 'Id invalid'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("SELECT id FROM Temperaturi WHERE id = %s;", (id,))
        existing_temperature = cursor.fetchone()

        if not existing_temperature:
            conn.close()
            return jsonify({'error': 'Temperatura nu a fost gasita'}), 404

        cursor.execute("DELETE FROM Temperaturi WHERE id = %s;", (id,))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Temperatura stearsa cu success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)