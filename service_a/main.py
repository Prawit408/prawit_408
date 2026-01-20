import grpc
from concurrent import futures
import threading
from fastapi import FastAPI
import uvicorn
import json
import os

# นำเข้าไฟล์ที่สร้างจาก user.proto สำหรับการสื่อสารแบบ gRPC
import user_pb2
import user_pb2_grpc

# สร้างอินสแตนซ์ของ FastAPI สำหรับบริการ REST API
app = FastAPI()

# --- ส่วนของการจัดการข้อมูล (Data Management) ---

def load_movies_db():
    """
    ฟังก์ชันสำหรับอ่านข้อมูลจากไฟล์ JSON แบบ Synchronous
    เพื่อให้มั่นใจว่าข้อมูลหนัง Spider-Man ถูกโหลดขึ้นมาก่อนการประมวลผล
    """
    file_path = os.path.join(os.path.dirname(__file__), "movies.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("movies", [])
    except Exception as e:
        # แสดงข้อผิดพลาดหากไม่สามารถอ่านไฟล์ JSON ได้
        print(f"Error loading JSON: {e}")
        return []

# --- ส่วนของ gRPC Server Logic ---

class UserService(user_pb2_grpc.UserServiceServicer):
    """
    คลาสสำหรับจัดการคำขอ gRPC (Servicer) 
    ทำหน้าที่ตอบกลับข้อมูลหนังตาม movie_id ที่ได้รับ
    """
    def GetUser(self, request, context):
        # โหลดฐานข้อมูลหนัง Spider-Man
        movies = load_movies_db()
        
        # ค้นหาหนังที่มี ID ตรงกับ user_id ที่ Client ส่งมา (Synchronous Searching)
        movie = next((m for m in movies if str(m["movie_id"]) == str(request.user_id)), None)
        
        if movie:
            # หากพบข้อมูล จะส่งคำตอบกลับตามโครงสร้างที่นิยามไว้ใน proto
            # Mapping: title -> user_name และ director -> email
            return user_pb2.UserResponse(
                user_name=movie["title"],
                email=f"Director: {movie['director']}",
                is_active=True
            )
        
        # กรณีไม่พบข้อมูล ส่งค่าว่างกลับไป
        return user_pb2.UserResponse(user_name="Movie Not Found")

def run_grpc():
    """ฟังก์ชันสำหรับเริ่มต้นการทำงานของ gRPC Server บนพอร์ต 50051"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Server started on port 50051")
    server.start()
    server.wait_for_termination()

# --- ส่วนของ REST API Logic (Service C จะเรียกใช้ส่วนนี้) ---

@app.get("/movies")
def get_all_movies():
    """Endpoint สำหรับดึงรายชื่อหนัง Spider-Man ทั้งหมด (RESTful GET)"""
    return load_movies_db()

@app.get("/user/{user_id}")
def get_movie_by_id(user_id: str):
    """Endpoint สำหรับค้นหาหนังรายเรื่องผ่านพอร์ต 8000"""
    movies = load_movies_db()
    movie = next((m for m in movies if str(m["movie_id"]) == user_id), None)
    return movie if movie else {"error": "Movie Not Found"}

if __name__ == "__main__":
    # ใช้ Threading เพื่อรัน gRPC และ REST API ไปพร้อมกันใน Service เดียว
    threading.Thread(target=run_grpc, daemon=True).start()
    
    # รัน FastAPI Server (พอร์ต 8000) สำหรับการสื่อสารแบบ REST
    uvicorn.run(app, host="0.0.0.0", port=8000)