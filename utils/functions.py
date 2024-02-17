
import json

def SQLtoJSON(field_names, input):
    try:
        # field_names = [i[0] for i in cursor.description]
        data = [dict(zip(field_names, row)) for row in input]
        json_data = json.dumps(data, default=str)
        json_data = json.loads(json_data)
        return json_data
    except Exception as e:
        print(f"[SQLtoJSON] An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

