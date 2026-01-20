โปรเจค: 6604101408_Prawit_Midterm


วิชา: Cloud-native Development Engineering  ชื่อนักศึกษา: นายประวิทย์ ประภาวรารัตน์ (รหัสนักศึกษา 6604101408)

1. สถาปัตยกรรมของระบบ (Microservices Architecture)
โปรเจคนี้ประกอบด้วย 3 Microservices ที่พัฒนาด้วย FastAPI และสื่อสารกันแบบ Synchronous:

Service A (Data Provider): เป็นตัวเก็บข้อมูลหนัง Spider-Man ในรูปแบบ JSON และเปิดช่องทางให้ Service อื่นดึงข้อมูลผ่าน gRPC (Port 50051) และ REST API (Port 8000).

Service B (gRPC Client): ทำหน้าที่เป็น Client เรียกข้อมูลจาก Service A ผ่าน gRPC เพื่อแสดงผลข้อมูลหนัง.

Service C (REST Client): ทำหน้าที่เรียกข้อมูลจาก Service A ผ่าน RESTful API ตามมาตรฐาน HTTP GET.

2. การสื่อสารระหว่าง Service (Inter-service Communication)
Request: Client จะส่ง movie_id ไปหา Service A.

Response: Service A จะคืนค่าข้อมูลหนัง (Title, Director, Rating) โดยทำการ Mapping ข้อมูลเข้ากับ Schema ของ user.proto (user_name, email).

3. วิธีการรันระบบ (How to Run)
ใช้ Docker Compose เพื่อ Build และรันทุก Service พร้อมกัน:

ไปที่ Root Directory (โฟลเดอร์ที่มีไฟล์ docker-compose.yml).

พิมพ์คำสั่งใน Terminal: docker-compose up --build.

ระบบจะทำการติดตั้ง Dependencies จากไฟล์ requirements.txt ของแต่ละโฟลเดอร์โดยอัตโนมัติ.

4. ผลลัพธ์การทำงาน (Expected Output)
Service B (gRPC): เข้าไปที่ http://localhost:8001/user/1 จะปรากฏข้อมูลหนัง Spider-Man จากการเรียก gRPC.

Service C (REST): เข้าไปที่ http://localhost:8002/user/1 จะปรากฏข้อมูลหนังในรูปแบบ JSON จากการเรียก REST API.