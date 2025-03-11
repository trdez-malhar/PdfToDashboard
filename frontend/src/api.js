import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api";

export const getUsers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users`);
    return response.data;
  } catch (error) {
    console.error("Error fetching users:", error);
    return [];
  }
};

export const addUser = async (userData) => {
  try {
    await axios.post(`${API_BASE_URL}/add-user`, userData);
    alert("User added successfully!");
  } catch (error) {
    console.error("Error adding user:", error);
  }
};
