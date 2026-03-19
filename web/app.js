class SecurityQuizApp {
    constructor() {
        this.allQuestions = [];
        this.currentQuestions = [];
        this.currentIndex = 0;
        this.isShowingAnswer = false;

        this.elements = {
            selectionScreen: document.getElementById('selection-screen'),
            quizScreen: document.getElementById('quiz-screen'),
            categoryList: document.getElementById('category-list'),
            questionText: document.getElementById('question-text'),
            answerArea: document.getElementById('answer-area'),
            answerText: document.getElementById('answer-text'),
            commentaryText: document.getElementById('commentary-text'),
            actionBtn: document.getElementById('action-btn'),
            homeBtn: document.getElementById('home-btn'),
            examInfo: document.getElementById('exam-info'),
            progressText: document.getElementById('progress-text'),
            subjectLabel: document.getElementById('subject-label'),
            loading: document.getElementById('loading'),
            shareBtn: document.getElementById('share-btn')
        };

        this.init();
    }

    async init() {
        try {
            // 로컬 파일 접근 시 보안 정책(CORS) 문제를 피하기 위해 data.js에서 로드된 전역 변수 사용
            this.allQuestions = window.QUIZ_DATA;
            
            if (!this.allQuestions || this.allQuestions.length === 0) {
                throw new Error('Data not found in window.QUIZ_DATA');
            }

            this.renderCategories();
            this.hideLoading();
            this.attachGlobalEvents();
        } catch (error) {
            console.error('Failed to load questions:', error);
            alert('질문 데이터를 불러오는 데 실패했습니다. (CORS 또는 파일 누락)');
        }
    }

    hideLoading() {
        this.elements.loading.style.opacity = '0';
        setTimeout(() => this.elements.loading.classList.add('hidden'), 500);
    }

    renderCategories() {
        const categories = {
            "전체": ["전체"],
            "시스템 보안": ["시스템 보안 > 리눅스/유닉스", "시스템 보안 > 윈도우", "시스템 보안 > 시스템 관리"],
            "네트워크 보안": ["네트워크 보안 > 프로토콜", "네트워크 보안 > 네트워크 공격/방어"],
            "애플리케이션 보안": ["애플리케이션 보안 > 웹 보안", "애플리케이션 보안 > DB 보안", "애플리케이션 보안 > 암호학"],
            "정보보호 관리 및 법규": ["정보보호 관리 및 법규 > 관리체계", "정보보호 관리 및 법규 > 법령"]
        };

        const icons = {
            "전체": "🔥",
            "시스템 보안": "💻",
            "네트워크 보안": "🌐",
            "애플리케이션 보안": "📱",
            "정보보호 관리 및 법규": "⚖️",
            "기타/신규 주제": "🆕"
        };

        this.elements.categoryList.innerHTML = '';

        for (const [mainCat, subs] of Object.entries(categories)) {
            const mainIcon = icons[mainCat] || "📁";

            if (mainCat === "전체") {
                const btn = this.createCategoryBtn("모든 문제 풀기", "전체", true, mainIcon);
                this.elements.categoryList.appendChild(btn);
                continue;
            }

            const header = document.createElement('div');
            header.className = 'group-header';
            header.innerText = mainCat;
            this.elements.categoryList.appendChild(header);

            // 메인 카테고리 전체 버튼
            const allBtn = this.createCategoryBtn(`${mainCat} 전체`, mainCat, true, mainIcon);
            this.elements.categoryList.appendChild(allBtn);

            subs.forEach(sub => {
                if (sub === mainCat) return;
                const subTitle = sub.includes(' > ') ? sub.split(' > ').pop() : sub;
                const btn = this.createCategoryBtn(subTitle, sub, false, mainIcon);
                this.elements.categoryList.appendChild(btn);
            });
        }

        // 기타 카테고리 자동 감지
        const otherSubjects = [...new Set(this.allQuestions.map(q => q.subject))]
            .filter(s => s && !Object.values(categories).flat().includes(s))
            .sort();

        if (otherSubjects.length > 0) {
            const header = document.createElement('div');
            header.className = 'group-header';
            header.innerText = '기타/신규 주제';
            this.elements.categoryList.appendChild(header);

            otherSubjects.forEach(sub => {
                const btn = this.createCategoryBtn(sub, sub, false, icons["기타/신규 주제"]);
                this.elements.categoryList.appendChild(btn);
            });
        }
    }

    createCategoryBtn(text, subject, isPrimary = false, icon = "📁") {
        const btn = document.createElement('button');
        btn.className = `category-btn ${isPrimary ? 'primary-category' : ''}`;
        
        const count = subject === "전체" 
            ? this.allQuestions.length 
            : this.allQuestions.filter(q => q.subject === subject || q.subject?.startsWith(subject)).length;

        btn.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.4rem;">${icon}</span>
                <span>${text}</span>
            </div>
            <span>${count}</span>
        `;
        btn.onclick = () => this.startQuiz(subject);
        return btn;
    }

    startQuiz(subject) {
        if (subject === "전체") {
            this.currentQuestions = [...this.allQuestions];
        } else {
            this.currentQuestions = this.allQuestions.filter(q => 
                q.subject === subject || q.subject?.startsWith(subject)
            );
        }

        if (this.currentQuestions.length === 0) {
            alert('해당 카테고리에 문제가 없습니다.');
            return;
        }

        this.shuffle(this.currentQuestions);
        this.currentIndex = 0;
        this.showScreen('quiz');
        this.showQuestion();
    }

    shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    showQuestion() {
        const q = this.currentQuestions[this.currentIndex];
        this.isShowingAnswer = false;

        this.elements.questionText.innerText = q.question;
        this.elements.subjectLabel.innerText = q.subject || '일반';
        this.elements.examInfo.innerText = q.exam_info || '핵심 기출';
        this.elements.progressText.innerText = `${this.currentIndex + 1} / ${this.currentQuestions.length}`;
        
        this.elements.answerArea.classList.add('hidden');
        this.elements.actionBtn.innerText = '정답 확인';
        this.elements.actionBtn.classList.remove('next-mode');
        
        // 스크롤 초기화
        document.getElementById('quiz-card').scrollTop = 0;
    }

    handleAction() {
        if (!this.isShowingAnswer) {
            const q = this.currentQuestions[this.currentIndex];
            this.elements.answerText.innerText = q.answer;
            this.elements.commentaryText.innerText = q.commentary;
            
            this.elements.answerArea.classList.remove('hidden');
            this.elements.actionBtn.innerText = '다음 문제';
            this.elements.actionBtn.classList.add('next-mode');
            this.isShowingAnswer = true;
        } else {
            this.currentIndex = (this.currentIndex + 1) % this.currentQuestions.length;
            if (this.currentIndex === 0) this.shuffle(this.currentQuestions);
            this.showQuestion();
        }
    }

    showScreen(screenType) {
        if (screenType === 'selection') {
            this.elements.selectionScreen.classList.remove('hidden');
            this.elements.quizScreen.classList.add('hidden');
        } else {
            this.elements.selectionScreen.classList.add('hidden');
            this.elements.quizScreen.classList.remove('hidden');
        }
    }

    attachGlobalEvents() {
        this.elements.actionBtn.onclick = () => this.handleAction();
        this.elements.homeBtn.onclick = () => this.showScreen('selection');
        this.elements.shareBtn.onclick = () => this.handleShare();
        
        // Enter 키 지원
        window.onkeydown = (e) => {
            if (e.key === 'Enter' && !this.elements.quizScreen.classList.contains('hidden')) {
                this.handleAction();
            }
        };
    }
    async handleShare() {
        const shareData = {
            title: '정보보안기사 Master - 퀴즈 앱',
            text: '28개년 정보보안기사 실기 단답형 전수 퀴즈! 지금 학습해 보세요.',
            url: window.location.href
        };

        try {
            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                await navigator.clipboard.writeText(window.location.href);
                alert('링크가 클립보드에 복사되었습니다. 다른 사람에게 공유해 보세요!');
            }
        } catch (err) {
            console.error('Share failed:', err);
        }
    }
}

// 앱 실행 및 PWA 서비스 워커 등록
document.addEventListener('DOMContentLoaded', () => {
    new SecurityQuizApp();

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js')
            .then(reg => console.log('SW Registered'))
            .catch(err => console.error('SW Registration Failed', err));
    }
});
