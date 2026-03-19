import json
import os
import shutil

def sync_data():
    # 경로 설정
    base_dir = r"c:\ys_start\GE"
    json_path = os.path.join(base_dir, "questions.json")
    web_dir = os.path.join(base_dir, "web")
    web_json_path = os.path.join(web_dir, "questions.json")
    web_js_path = os.path.join(web_dir, "data.js")

    if not os.path.exists(json_path):
        print(f"오류: {json_path} 파일을 찾을 수 없습니다.")
        return

    # 1. 원본 데이터 로드
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 2. 웹 폴더에 JSON 복사 (백업 및 서버용)
    shutil.copy2(json_path, web_json_path)
    print(f"성공: {web_json_path} 복사 완료.")

    # 3. data.js 생성 (로컬 파일 실행 시 CORS 방지용)
    js_content = f"window.QUIZ_DATA = {json.dumps(data, ensure_ascii=False)};"
    with open(web_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"성공: {web_js_path} 동기화 완료.")

    print(f"\n[업데이트 완료] 총 {len(data)}개의 문제가 모든 플랫폼에 반영되었습니다.")

if __name__ == "__main__":
    sync_data()
