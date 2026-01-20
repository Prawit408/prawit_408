from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

# กำหนด URL ของ Service A สำหรับการเรียกแบบ REST API
SERVICE_A_URL = "http://service_a:8000"

@app.get("/user/{user_id}")
def get_user_from_service_a(user_id: str):
    """
    ฟังก์ชันดึงข้อมูลจาก Service A ผ่าน RESTful API แบบ Synchronous
    Client (Service C) จะรอ Response จากต้นทางก่อนแสดงผล
    """
    try:
        # ส่ง HTTP GET request ไปยัง Service A
        response = requests.get(f"{SERVICE_A_URL}/user/{user_id}")
        
        # ตรวจสอบว่าเรียกข้อมูลสำเร็จหรือไม่
        if response.status_code == 200:
            return response.json()
        return {"error": "ไม่สามารถดึงข้อมูลจาก Service A ได้"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # รัน Service C บนพอร์ต 8002 เพื่อเป็นช่องทางแสดงผลแบบ REST
    uvicorn.run(app, host="0.0.0.0", port=8002)