import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    console.log('useEffect called');
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    console.log('Fetching todos...');
    try {
      const response = await axios.get('http://localhost:8000/todos');
      console.log('Todos fetched:', response.data);
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting new todo:', newTodo);
    if (!newTodo.trim()) return;

    try {
      const response = await axios.post('http://localhost:8000/todos', { description: newTodo });
      console.log('Todo created:', response.data);
      setNewTodo('');
      fetchTodos();
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  return (
    <div style={{ padding: '20px'}}>
      <h1>Todo List</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Enter todo description"
          style={{ padding: '10px', width: '300px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>Add Todo</button>
      </form>
      <ul>
        {todos.map((todo) => (
          <li key={todo._id}>{todo.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;