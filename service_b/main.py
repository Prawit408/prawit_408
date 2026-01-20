import grpc
from fastapi import FastAPI
import uvicorn

# นำเข้าไฟล์ที่ได้จากการคอมไพล์ user.proto
import user_pb2
import user_pb2_grpc

app = FastAPI()

def get_user_info_grpc(user_id: int):
    """
    ฟังก์ชันเชื่อมต่อกับ Service A ผ่าน gRPC แบบ Synchronous
    จะรอจนกว่า Service A จะส่งข้อมูลกลับมาถึงจะทำงานขั้นต่อไป
    """
    # สร้างช่องทางการเชื่อมต่อ (Channel) ไปยัง Service A ที่พอร์ต 50051
    with grpc.insecure_channel('service_a:50051') as channel:
        # สร้าง Stub เพื่อใช้เรียกฟังก์ชันของ gRPC Server
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # ส่งคำขอ (Request) พร้อม user_id ไปยัง Service A
        response = stub.GetUser(user_pb2.UserRequest(user_id=user_id))
        
        # คืนค่าข้อมูลที่ได้รับ (ซึ่งถูกแม็พมาจากข้อมูล Spider-Man ใน Service A)
        return {
            "movie_title": response.user_name,
            "director_info": response.email,
            "status": response.is_active
        }

@app.get("/user/{user_id}")
def read_user(user_id: int):
    """
    Endpoint สำหรับแสดงผลข้อมูลหนัง Spider-Man ที่ดึงผ่าน gRPC
    """
    return get_user_info_grpc(user_id)

if __name__ == "__main__":
    # รัน Service B บนพอร์ต 8001 ตามที่กำหนดในระบบ Microservices
    uvicorn.run(app, host="0.0.0.0", port=8001)