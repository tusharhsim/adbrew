import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient, errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client['todo_db']
    todos_collection = db['todos']
    logger.info("Connected to MongoDB")
except errors.ServerSelectionTimeoutError as err:
    logger.error(f"Failed to connect to MongoDB: {err}")
    raise

@csrf_exempt
def todos(request):
    if request.method == 'GET':
        try:
            todos = list(todos_collection.find())
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return JsonResponse(todos, safe=False)
        except Exception as e:
            logger.error(f"Error fetching todos: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            description = data.get('description')
            if description:
                new_todo = {'description': description}
                result = todos_collection.insert_one(new_todo)
                new_todo['_id'] = str(result.inserted_id)
                return JsonResponse(new_todo, status=201)
            else:
                return JsonResponse({'error': 'Description is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)