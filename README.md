# 💖 Pyarometer - Love Predictor 💖

Welcome to **Pyarometer**, the ultimate love compatibility predictor! 🌟✨  
This project combines the magic of Python 🐍, Flask 🌐, and MongoDB 🍃 to calculate love compatibility between two names. Whether you're curious about your soulmate or just having fun, Pyarometer has got you covered! 💕

---

## 🌟 Features

- 🔮 **Love Compatibility Calculator**: Enter two names and discover their compatibility percentage!
- 🖼️ **Beautiful UI**: A sleek and responsive design with animations and gradients.
- 📊 **MongoDB Integration**: Stores compatibility checks for future reference.
- 🚀 **API Endpoint**: Use `/api/compatibility` to integrate the compatibility calculator into your own projects.
- 🎉 **Special Cases**: Easter eggs for certain name pairs with unique compatibility scores!

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 🎨  
- **Backend**: Python (Flask) 🐍  
- **Database**: MongoDB 🍃  
- **Deployment**: Vercel 🌐  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+ 🐍
- MongoDB Atlas account 🍃

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/pyarometer.git
   cd pyarometer

2. Install dependencies"
   ```bash
   pip install -r requirements.txt

3. Set up your .env file with your MongoDB URI:
   ```bash
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority

4. Run the app locally:
   ```bash
   python app.py

## 🌐 API Usage

### Endpoint: `/api/compatibility`
- **Method**: POST  
- **Request Body**:  
  ```json
  {
    "name1": "Alice",
    "name2": "Bob"
  }
  ```
- **Response**:  
  ```json
  {
    "compatibility": 85
  }
  ```

---

## 🎨 Screenshots

### Home Page
![image](https://github.com/user-attachments/assets/cf9ed47c-e527-450a-8e0d-b1bb54e0f4bc)


### Results Page
![image](https://github.com/user-attachments/assets/57a5426b-dee1-43e5-b894-7d38a9a55740)


---

## 📜 License

This project is licensed under the [MIT License](LICENSE). 📝  

---

## 🤝 Contributing

We welcome contributions! Feel free to open issues or submit pull requests. 🙌  

---

## 🌟 Acknowledgments

- **Flask** for powering the backend 🌐  
- **MongoDB** for seamless database integration 🍃  
- **Vercel** for deployment 🚀  

---

## 🧡 Made with Love by [Abhijeet Jha](https://github.com/yourusername) 💖
```
