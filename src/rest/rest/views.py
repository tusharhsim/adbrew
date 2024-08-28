import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient, errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            db = client['todo_db']
            todos_collection = db['todos']
            logger.info("Connected to MongoDB")
            return todos_collection
        except errors.ServerSelectionTimeoutError as err:
            logger.error(f"Failed to connect to MongoDB: {err}")
            raise


class TodoOperations:
    @staticmethod
    def get_todos(collection):
        try:
            todos = list(collection.find())
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return todos
        except Exception as e:
            logger.error(f"Error fetching todos: {e}")
            raise

    @staticmethod
    def create_todo(collection, description):
        try:
            new_todo = {'description': description}
            result = collection.insert_one(new_todo)
            new_todo['_id'] = str(result.inserted_id)
            return new_todo
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            raise


class RequestHandler:
    @staticmethod
    def handle_get(collection):
        try:
            todos = TodoOperations.get_todos(collection)
            return JsonResponse(todos, safe=False)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    @staticmethod
    def handle_post(collection, data):
        try:
            description = data.get('description')
            if description:
                new_todo = TodoOperations.create_todo(collection, description)
                return JsonResponse(new_todo, status=201)
            else:
                return JsonResponse({'error': 'Description is required'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_exempt
def todos(request):
    collection = DatabaseConnection.get_connection()

    if request.method == 'GET':
        return RequestHandler.handle_get(collection)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            return RequestHandler.handle_post(collection, data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
