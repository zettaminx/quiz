import tkinter as tk
import customtkinter as ctk
import json
import random
import sys
import os

# PyInstaller에서 리소스 경로를 처리하기 위한 함수
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🛡️ 정보보안기사 Master - 28개년 전수 실기")
        self.geometry("650x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # 데이터 로드
        self.all_questions = []
        self.questions = []
        self.load_data()
        
        self.current_index = 0
        self.show_answer_mode = False
        self.selected_subject = "전체"

        # 메인 컨테이너
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # 초기 선택 화면 표시
        self.show_subject_selection()

    def load_data(self):
        try:
            with open(resource_path("questions.json"), "r", encoding="utf-8") as f:
                self.all_questions = json.load(f)
        except Exception as e:
            self.all_questions = [{"id": 0, "exam_info": "오류", "subject": "오류", "question": f"데이터 로드 실패: {str(e)}", "answer": "", "commentary": ""}]

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_subject_selection(self):
        self.clear_container()
        
        # 헤더
        ctk.CTkLabel(self.container, text="학습 과목을 선택하세요", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(20, 20))

        # 세부 과목 분류 정의
        categories = {
            "전체": ["전체"],
            "시스템 보안": ["시스템 보안 > 시스템 일반", "시스템 보안 > 리눅스/유닉스", "시스템 보안 > 윈도우", "시스템 보안 > 시스템 관리", "시스템 보안 > 보안 기법", "시스템 보안 > 악성코드"],
            "네트워크 보안": ["네트워크 보안 > 네트워크 일반", "네트워크 보안 > 프로토콜", "네트워크 보안 > 네트워크 공격", "네트워크 보안 > 네트워크 공격/방어", "네트워크 보안 > 공격 기법", "네트워크 보안 > 방화벽", "네트워크 보안 > 보안 장비", "네트워크 보안 > 무선 보안", "네트워크 보안 > 클라우드 보안"],
            "애플리케이션 보안": ["애플리케이션 보안 > 애플리케이션 일반", "애플리케이션 보안 > 웹 보안", "애플리케이션 보안 > DB 보안", "애플리케이션 보안 > 암호학"],
            "정보보호 관리 및 법규": ["정보보호 관리 및 법규 > 관리체계", "정보보호 관리 및 법규 > 법령", "정보보호 관리 및 법규 > 유관기관"]
        }
        
        # 스크롤 가능한 영역
        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent", height=500)
        scroll_frame.pack(fill="both", expand=True, padx=20)

        for main_cat, subs in categories.items():
            if main_cat == "전체":
                btn = ctk.CTkButton(
                    scroll_frame, 
                    text="전체 문제 풀기", 
                    command=lambda s="전체": self.start_quiz(s),
                    height=50,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    fg_color="#E74C3C",
                    hover_color="#C0392B",
                    corner_radius=8
                )
                btn.pack(pady=10, fill="x", padx=20)
                continue

            # 메인 카테고리 레이블 및 버튼
            cat_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            cat_frame.pack(fill="x", pady=(15, 5))
            
            ctk.CTkLabel(cat_frame, text=f"■ {main_cat}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#3498DB").pack(side="left", padx=5)
            
            # 메인 카테고리 전체 풀기 버튼
            ctk.CTkButton(
                cat_frame, 
                text=f"{main_cat} 전체 풀기", 
                width=140,
                height=25,
                command=lambda s=main_cat: self.start_quiz(s),
                fg_color="#2980B9",
                hover_color="#1F618D",
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(side="right", padx=20)
            
            for sub in subs:
                if sub == main_cat: continue
                # 해당 소주제의 전체 문제 수 계산
                sub_questions = [q for q in self.all_questions if q.get("subject") == sub]
                n = len(sub_questions)
                
                btn_txt_base = sub.split(" > ")[-1] if " > " in sub else sub
                
                if n <= 10:
                    btn = ctk.CTkButton(
                        scroll_frame, 
                        text=f"{btn_txt_base} ({n}문제)", 
                        command=lambda s=sub: self.start_quiz(s),
                        height=40,
                        font=ctk.CTkFont(size=14),
                        fg_color="#34495E",
                        hover_color="#5D6D7E",
                        corner_radius=8
                    )
                    btn.pack(pady=3, fill="x", padx=40)
                else:
                    # 10문제가 넘으면 분할 버튼 생성
                    num_blocks = (n + 9) // 10
                    grid_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                    grid_frame.pack(fill="x", padx=40, pady=3)
                    
                    label = ctk.CTkLabel(grid_frame, text=f"{btn_txt_base} ({n}문제)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#BDC3C7")
                    label.pack(anchor="w")
                    
                    buttons_container = ctk.CTkFrame(grid_frame, fg_color="transparent")
                    buttons_container.pack(fill="x")
                    
                    # 10문제 단위 버튼
                    ctk.CTkLabel(buttons_container, text="10문항:", font=ctk.CTkFont(size=11), text_color="#7F8C8D").pack(side="left", padx=(0, 5))
                    for i in range(num_blocks):
                        btn = ctk.CTkButton(
                            buttons_container, 
                            text=f"{i+1}", 
                            width=35,
                            height=30,
                            command=lambda s=sub, b=i: self.start_quiz(s, b),
                            fg_color="#34495E",
                            hover_color="#5D6D7E",
                            font=ctk.CTkFont(size=11)
                        )
                        btn.pack(side="left", padx=1)
                    
                    # 20/40/전체 옵션 추가
                    opt_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
                    opt_frame.pack(fill="x", pady=(2, 0))
                    
                    if n >= 20:
                        ctk.CTkButton(opt_frame, text="20문항 랜덤", width=85, height=25, font=ctk.CTkFont(size=11), 
                                      command=lambda s=sub: self.start_quiz(s, limit=20), fg_color="#2E4053").pack(side="left", padx=2)
                    if n >= 40:
                        ctk.CTkButton(opt_frame, text="40문항 랜덤", width=85, height=25, font=ctk.CTkFont(size=11), 
                                      command=lambda s=sub: self.start_quiz(s, limit=40), fg_color="#2E4053").pack(side="left", padx=2)
                    
                    ctk.CTkButton(opt_frame, text="소주제 전체", width=85, height=25, font=ctk.CTkFont(size=11), 
                                  command=lambda s=sub: self.start_quiz(s), fg_color="#1F618D").pack(side="left", padx=2)
        
        # 추가적인 기타 카테고리 자동 감지 (정의되지 않은 것들)
        existing_subs = []
        for s_list in categories.values(): existing_subs.extend(s_list)
        
        other_subjects = sorted(list(set(q.get("subject", "미분류") for q in self.all_questions if q.get("subject") not in existing_subs and q.get("subject"))))
        
        if other_subjects:
            ctk.CTkLabel(scroll_frame, text="■ 기타/신규 주제", font=ctk.CTkFont(size=18, weight="bold"), text_color="#3498DB").pack(anchor="w", pady=(15, 5))
            for sub in other_subjects:
                btn = ctk.CTkButton(
                    scroll_frame, 
                    text=sub, 
                    command=lambda s=sub: self.start_quiz(s),
                    height=40,
                    font=ctk.CTkFont(size=14),
                    fg_color="#34495E",
                    hover_color="#5D6D7E",
                    corner_radius=8
                )
                btn.pack(pady=3, fill="x", padx=40)

    def start_quiz(self, subject, block_index=None, limit=None):
        self.selected_subject = subject
        self.questions = []
        
        if subject == "전체":
            self.questions = list(self.all_questions)
        elif " > " in subject:
            # 세부 과목 필터링
            full_list = [q for q in self.all_questions if q.get("subject") == subject]
            
            if block_index is not None:
                # 10문제 단위 분할 모드
                self.questions = full_list[block_index*10 : (block_index+1)*10]
                self.selected_subject = f"{subject} ({block_index+1}번 묶음)"
            elif limit is not None:
                # 20/40문제 랜덤 추출 모드
                self.questions = list(full_list)
                random.shuffle(self.questions)
                self.questions = self.questions[:limit]
                self.selected_subject = f"{subject} ({len(self.questions)}문항 학습)"
            else:
                # 소주제 전체
                self.questions = full_list
                self.selected_subject = f"{subject} (전체 {len(self.questions)}문항)"
        else:
            # 메인 과목 필터링 (해당 메인 과목으로 시작하는 모든 세부 과목 포함)
            self.questions = [q for q in self.all_questions if q.get("subject", "").startswith(subject)]
        
        if not self.questions:
            self.questions = [{"id": 0, "exam_info": "-", "subject": subject, "question": f"'{subject}' 과목에 문제가 없습니다.", "answer": "", "commentary": ""}]
        
        # 섞기 (블록 모드 아닐 때만 전체 섞기)
        if block_index is None:
            random.shuffle(self.questions)
            
        self.current_index = 0
        self.setup_quiz_ui()
        self.show_question()

    def setup_quiz_ui(self):
        self.clear_container()

        # 상단 바 (홈 버튼 및 제목, 회차 정보)
        top_bar = ctk.CTkFrame(self.container, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(top_bar, text="🏠", width=40, command=self.show_subject_selection, fg_color="#5D6D7E").pack(side="left")
        
        self.info_label = ctk.CTkLabel(top_bar, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="#E74C3C")
        self.info_label.pack(side="right")
        
        ctk.CTkLabel(self.container, text=f"과목: {self.selected_subject}", font=ctk.CTkFont(size=13), text_color="#7F8C8D").pack(anchor="w")

        # 퀴즈 카드
        self.card = ctk.CTkFrame(self.container, corner_radius=20, fg_color="#2C3E50", border_width=2, border_color="#34495E")
        self.card.pack(fill="both", expand=True, pady=10)

        self.q_label = ctk.CTkLabel(self.card, text="", wraplength=550, font=ctk.CTkFont(size=19, weight="normal"), justify="center")
        self.q_label.pack(expand=True, padx=30, pady=40)

        # 정답 및 해설 영역
        self.ans_frame = ctk.CTkFrame(self.card, fg_color="#1A252F", corner_radius=15)
        self.ans_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.ans_label = ctk.CTkLabel(self.ans_frame, text="", text_color="#3498DB", font=ctk.CTkFont(size=22, weight="bold"))
        self.ans_label.pack(pady=(15, 5))

        self.com_label = ctk.CTkLabel(self.ans_frame, text="", wraplength=550, font=ctk.CTkFont(size=14), text_color="#BDC3C7")
        self.com_label.pack(pady=(0, 15), padx=30)

        # 하단 버튼
        self.btn_action = ctk.CTkButton(
            self.container, 
            text="정답 확인", 
            command=self.handle_action, 
            height=55, 
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            corner_radius=12
        )
        self.btn_action.pack(fill="x", pady=20, padx=20)

        # 진행도 표시
        self.progress_label = ctk.CTkLabel(self.container, text="", font=ctk.CTkFont(size=13), text_color="#7F8C8D")
        self.progress_label.pack()

    def show_question(self):
        q_data = self.questions[self.current_index]
        self.info_label.configure(text=f"📌 {q_data.get('exam_info', '기출 정보 없음')}")
        self.q_label.configure(text=f"Q. {q_data['question']}")
        self.ans_label.configure(text="")
        self.com_label.configure(text="")
        self.btn_action.configure(text="정답 확인", fg_color="#3498DB")
        self.progress_label.configure(text=f"Progress: {self.current_index + 1} / {len(self.questions)}")
        self.show_answer_mode = False

    def handle_action(self):
        if not self.show_answer_mode:
            q_data = self.questions[self.current_index]
            self.ans_label.configure(text=f"정답: {q_data['answer']}")
            self.com_label.configure(text=q_data['commentary'])
            self.btn_action.configure(text="다음 문제", fg_color="#27AE60", hover_color="#219150")
            self.show_answer_mode = True
        else:
            self.current_index = (self.current_index + 1) % len(self.questions)
            if self.current_index == 0:
                random.shuffle(self.questions)
            self.show_question()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
