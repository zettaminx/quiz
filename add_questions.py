import json
import os

def add_new_questions():
    json_path = r"c:\ys_start\GE\questions.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    existing_ids = {q['id'] for q in data}
    
    new_data = [
        # 네트워크 보안
        {"id": 401, "exam_info": "최신 빈출", "subject": "네트워크 보안 > 프로토콜", "question": "TCP의 3-way Handshake 과정에서 클라이언트가 서버로 보내는 첫 번째 패킷의 플래그는?", "answer": "SYN", "commentary": "연결 요청을 위해 Sequence Number를 동기화하는 단계입니다."},
        {"id": 402, "exam_info": "최신 빈출", "subject": "네트워크 보안 > 프로토콜", "question": "서버가 클라이언트의 SYN에 대해 응답하며 보내는 패킷의 플래그 조합은?", "answer": "SYN, ACK", "commentary": "요청 수락과 동시에 자신의 일련번호를 전송합니다."},
        {"id": 403, "exam_info": "최신 빈출", "subject": "네트워크 보안 > 네트워크 공격", "question": "TCP 연결 수립 과정에서 마지막 ACK를 보내지 않아 서버의 대기 큐를 가득 채우는 DoS 공격은?", "answer": "SYN Flooding", "commentary": "Half-Open 상태를 이용하여 서버 자원을 고갈시킵니다."},
        {"id": 404, "exam_info": "최신 빈출", "subject": "네트워크 보안 > 프로토콜", "question": "IP 헤더에서 패킷이 네트워크 상에 머무를 수 있는 시간을 제한하는 필드는?", "answer": "TTL (Time To Live)", "commentary": "라우터를 거칠 때마다 1씩 감소하며 0이 되면 패킷이 폐기됩니다."},
        {"id": 405, "exam_info": "최신 빈출", "subject": "네트워크 보안 > 네트워크 공격", "question": "ICMP Echo Request를 보낼 때 출발지 IP를 대상 서버로 변조하여 응답이 대상에게 쏟아지게 하는 공격은?", "answer": "Smurf 공격", "commentary": "증폭 네트워크(Amp Network)를 이용한 반사형 DoS 공격입니다."},
        
        # 시스템 보안
        {"id": 406, "exam_info": "최신 빈출", "subject": "시스템 보안 > 리눅스/유닉스", "question": "리눅스에서 파일의 권한 중 실행 시 파일 소유자의 권한을 일시적으로 획득하게 하는 특수 권한은?", "answer": "SetUID", "commentary": "8진수로 4000번에 해당하며, passwd 명령어 등이 대표적입니다."},
        {"id": 407, "exam_info": "최신 빈출", "subject": "시스템 보안 > 리눅스/유닉스", "question": "리눅스에서 특정 디렉터리에 설정하여 소유자만이 파일을 삭제할 수 있게 제한하는 권한은?", "answer": "Sticky Bit", "commentary": "8진수로 1000번에 해당하며, /tmp 디렉터리 등에 쓰입니다."},
        {"id": 408, "exam_info": "최신 빈출", "subject": "시스템 보안 > 리눅스/유닉스", "question": "사용자의 패스워드 암호화 해시값이 실제로 저장되는 리눅스 파일 경로는?", "answer": "/etc/shadow", "commentary": "일반 사용자는 읽을 수 없도록 설정하여 보안을 강화합니다."},
        {"id": 409, "exam_info": "최신 빈출", "subject": "시스템 보안 > 윈도우", "question": "윈도우에서 시스템의 부팅, 로그인, 서비스 실행 등 모든 이벤트를 기록하는 로그 관리 도구는?", "answer": "이벤트 뷰어 (Event Viewer)", "commentary": "보안 로그, 시스템 로그, 응용 프로그램 로그 등을 확인합니다."},
        {"id": 410, "exam_info": "최신 빈출", "subject": "시스템 보안 > 윈도우", "question": "윈도우 보안 로그에서 성공적인 로그온 이벤트를 나타내는 이벤트 ID는?", "answer": "4624", "commentary": "로그인 기록 추적 시 가장 먼저 확인해야 할 ID입니다."},

        # 애플리케이션 보안
        {"id": 411, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 웹 보안", "question": "OWASP Top 10 중 입력값 검증 미흡으로 인해 서버의 쿼리나 명령어가 실행되는 취약점군의 명칭은?", "answer": "인젝션 (Injection)", "commentary": "SQL, OS 명령, NoSQL 인젝션 등이 포함됩니다."},
        {"id": 412, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 웹 보안", "question": "웹 페이지에 악성 스크립트를 삽입하여 사용자의 세션을 탈취하는 공격은?", "answer": "XSS (Cross-Site Scripting)", "commentary": "Stored, Reflected, DOM 기반 XSS로 나뉩니다."},
        {"id": 413, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 웹 보안", "question": "사용자가 로그인된 상태에서 의도치 않게 공격자가 원하는 요청(비밀번호 변경 등)을 보내게 하는 공격은?", "answer": "CSRF (Cross-Site Request Forgery)", "commentary": "사용자의 브라우저 신뢰를 악용하는 공격입니다."},
        {"id": 414, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 웹 보안", "question": "서버가 외부의 자원을 요청할 때 이를 가로채서 내부망으로 접근하게 하는 공격은?", "answer": "SSRF (Server-Side Request Forgery)", "commentary": "클라우드 메타데이터 조회 등에 악용되기도 합니다."},
        {"id": 415, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 웹 보안", "question": "HTTP 헤더 중 하나로, 브라우저에게 현재 페이지가 동일한 출처에서만 프레임 내에 표시되도록 설정하는 것은?", "answer": "X-Frame-Options", "commentary": "클릭재킹(Clickjacking) 공격을 방지하기 위해 사용합니다."},

        # 암호학
        {"id": 416, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 암호학", "question": "평문과 암호문의 관계를 복잡하게 하여 통계적으로 유추하기 어렵게 만드는 성질은?", "answer": "혼돈 (Confusion)", "commentary": "S-Box 치환 등을 통해 구현합니다."},
        {"id": 417, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 암호학", "question": "평문의 각 비트가 여러 암호문 비트에 영향을 주게 하여 패턴을 숨기는 성질은?", "answer": "확산 (Diffusion)", "commentary": "P-Box 전치(Permutation) 등을 통해 구현합니다."},
        {"id": 418, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 암호학", "question": "임의의 길이를 가진 메시지를 고정된 길이의 값으로 변환하는 일방향 함수는?", "answer": "해시 함수 (Hash Function)", "commentary": "무결성 검증, 패스워드 저장 등에 사용됩니다."},
        {"id": 419, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 암호학", "question": "해시 함수에서 서로 다른 두 입력이 같은 출력값을 내놓는 현상을 무엇이라 하는가?", "answer": "충돌 (Collision)", "commentary": "보안 해시 함수는 이 충돌을 찾기 어려워야 합니다."},
        {"id": 420, "exam_info": "최신 빈출", "subject": "애플리케이션 보안 > 암호학", "question": "수신자의 공개키로 암호화하고 수신자의 개인키로 복호화하는 방식의 명칭은?", "answer": "공개키 암호 (비대칭키 암호)", "commentary": "키 분배 문제를 해결하기 위해 고안되었습니다."},

        # 정보보호 관리 및 법규
        {"id": 421, "exam_info": "최신 빈출", "subject": "정보보호 관리 및 법규 > 관리체계", "question": "국내 정보보호 및 개인정보보호 관리체계 인증 제도의 통합 명칭은?", "answer": "ISMS-P", "commentary": "KISA에서 주관하며 정보보호와 개인정보보호를 아우릅니다."},
        {"id": 422, "exam_info": "최신 빈출", "subject": "정보보호 관리 및 법규 > 관리체계", "question": "자산, 위협, 취약점을 분석하여 위험 수준을 결정하는 일련의 과정을 무엇이라 하는가?", "answer": "위험 평가 (Risk Assessment)", "commentary": "위험 식별, 분석, 평가 단계로 구성됩니다."},
        {"id": 423, "exam_info": "최신 빈출", "subject": "정보보호 관리 및 법규 > 법령", "question": "개인정보보호법상 정보주체의 동의 없이 수집할 수 있는 불가피한 사유 중 첫 번째는?", "answer": "법률에 특별한 규정이 있거나 법령상 의무 준수를 위해 불가피한 경우", "commentary": "동의가 원칙이나 법적 근거가 있을 시 예외가 인정됩니다."},
        {"id": 424, "exam_info": "최신 빈출", "subject": "정보보호 관리 및 법규 > 법령", "question": "사고 발생 시 정보주체에게 알려야 하는 사항 중 유출된 항목과 발생 시점 외에 반드시 포함해야 하는 것은?", "answer": "정부 신고 기관 및 상담처", "commentary": "피해 확산 방지를 위한 대응 절차 안내가 필요합니다."},
        {"id": 425, "exam_info": "최신 빈출", "subject": "정보보호 관리 및 법규 > 관리체계", "question": "사고 발생 후 핵심 업무를 복구하기까지 허용되는 최대 시간을 의미하는 용어는?", "answer": "RTO (Recovery Time Objective)", "commentary": "복구 목표 시간을 의미합니다."},

        # 426~500번까지 대량 추가를 위한 자동 생성 템플릿 기반 데이터
        {"id": 426, "exam_info": "기출 주요 키워드", "subject": "네트워크 보안 > 프로토콜", "question": "UDP 프로토콜의 상위 계층에서 신뢰성을 보장하기 위해 주로 사용하는 방식은?", "answer": "애플리케이션 계층에서 자체 제어", "commentary": "UDP 자체는 비연결형이므로 상위에서 확인 응답을 구현해야 합니다."},
        {"id": 427, "exam_info": "기출 주요 키워드", "subject": "네트워크 보안 > 네트워크 공격", "question": "무선 공유기(AP)를 변조하여 정보를 탈취하는 가짜 AP 공격을 무엇이라 하는가?", "answer": "Evil Twin 공격", "commentary": "동일한 SSID를 사용하여 접속을 유도합니다."},
        {"id": 428, "exam_info": "기출 주요 키워드", "subject": "시스템 보안 > 시스템 관리", "question": "파일이나 데이터의 원본임을 증명하고 변조 여부를 확인하는 디지털 증거 수집 원칙은?", "answer": "무결성의 원칙", "commentary": "해시값 등을 통해 원본과 동일함을 보증해야 합니다."},
        {"id": 429, "exam_info": "기출 주요 키워드", "subject": "애플리케이션 보안 > 암호학", "question": "해시 함수의 안정성을 높이기 위해 매번 다른 무작위 값을 추가하는 기법은?", "answer": "솔팅 (Salting)", "commentary": "레인보우 테이블 공격을 방어하는 효과적인 방법입니다."},
        {"id": 430, "exam_info": "기출 주요 키워드", "subject": "정보보호 관리 및 법규 > 법령", "question": "개인정보보호법에서 만 14세 미만 아동의 정보를 처리할 때 반드시 받아야 하는 것은?", "answer": "법정대리인의 동의", "commentary": "아동의 권리 보호를 위한 필수 사항입니다."},
        {"id": 431, "exam_info": "기출 주요 키워드", "subject": "네트워크 보안 > 보안 장비", "question": "웹 트래픽(HTTP/HTTPS)을 전문적으로 검사하고 차단하는 보안 장비는?", "answer": "WAF (Web Application Firewall)", "commentary": "웹 애플리케이션 방화벽입니다."},
        {"id": 432, "exam_info": "기출 주요 키워드", "subject": "시스템 보안 > 악성코드", "question": "정상적인 프로그램처럼 위장하여 시스템에 침투한 뒤 백도어를 설치하는 악성코드는?", "answer": "트로이 목마 (Trojan Horse)", "commentary": "자기 복제 기능은 없으나 치명적인 사회공학적 공격 도구입니다."},
        {"id": 433, "exam_info": "기출 주요 키워드", "subject": "애플리케이션 보안 > 웹 보안", "question": "브라우저에 저장되어 사용자 인증 정보를 유지하며, 스크립트 접근을 막기 위해 HttpOnly 설정을 하는 대상은?", "answer": "쿠키 (Cookie)", "commentary": "세션 관리 및 사용자 추적에 사용됩니다."},
        {"id": 434, "exam_info": "기출 주요 키워드", "subject": "정보보호 관리 및 법규 > 관리체계", "question": "위험 처리 방안 중, 위험을 아예 제거하거나 발생 원인을 없애는 방식은?", "answer": "위험 회피 (Risk Avoidance)", "commentary": "해당 서비스를 중단하거나 자산을 처분하는 방식입니다."},
        {"id": 435, "exam_info": "기출 주요 키워드", "subject": "암호학", "question": "일회용 패스워드를 생성하여 고정된 비밀번호의 취약점을 보완하는 기술은?", "answer": "OTP (One-Time Password)", "commentary": "시간 동기화 방식과 챌린지 및 응답 방식이 있습니다."},
        {"id": 436, "exam_info": "기출 주요 키워드", "subject": "네트워크 보안 > 프로토콜", "question": "데이터 링크 계층에서 루프(Loop)를 방지하기 위해 사용되는 프로토콜은?", "answer": "STP (Spanning Tree Protocol)", "commentary": "가장 효율적인 경로만 남기고 나머지는 차단합니다."},
        {"id": 437, "exam_info": "기출 주요 키워드", "subject": "시스템 보안 > 리눅스/유닉스", "question": "리눅스에서 현재 실행 중인 프로세스의 트리 구조를 보여주는 명령어는?", "answer": "pstree", "commentary": "부모-자식 관계를 한눈에 파악하기 좋습니다."},
        {"id": 438, "exam_info": "기출 주요 키워드", "subject": "애플리케이션 보안 > 웹 보안", "question": "사용자가 입력한 경로를 통해 서버 내부의 파일을 읽어오는 취약점은?", "answer": "LFI (Local File Inclusion)", "commentary": "/etc/passwd 등의 민감 정보 유출로 이어질 수 있습니다."},
        {"id": 439, "exam_info": "기출 주요 키워드", "subject": "정보보호 관리 및 법규 > 법령", "question": "정보통신망법상 광고성 정보를 전송할 때 반드시 명시해야 하는 문구는?", "answer": "(광고)", "commentary": "제목 시작 부분에 표시해야 합니다."},
        {"id": 440, "exam_info": "기출 주요 키워드", "subject": "암호학", "question": "메시지의 해시값을 송신자의 개인키로 암호화한 것은?", "answer": "전자서명 (Digital Signature)", "commentary": "인증, 무결성, 부인방지를 제공합니다."},
        {"id": 441, "exam_info": "공통 핵심", "subject": "네트워크 보안", "question": "IPsec의 두 가지 보안 프로토콜 중 하나로, 무결성만 제공하며 암호화 기능은 없는 것은?", "answer": "AH (Authentication Header)", "commentary": "ESP와 대비되는 프로토콜입니다."},
        {"id": 442, "exam_info": "공통 핵심", "subject": "네트워크 보안", "question": "전송 구간 전체를 보호하기 위해 IP 패킷 전체를 캡슐화하는 IPsec 동작 모드는?", "answer": "터널 모드 (Tunnel Mode)", "commentary": "VPN 게이트웨이 간 통신에 주로 쓰입니다."},
        {"id": 443, "exam_info": "공통 핵심", "subject": "시스템 보안", "question": "윈도우에서 사용자 인증 정보를 담고 있는 메모리 상의 프로세스 명칭은?", "answer": "lsass.exe", "commentary": "덤프를 통해 비밀번호를 유출하는 공격의 대상이 됩니다."},
        {"id": 444, "exam_info": "공통 핵심", "subject": "애플리케이션 보안", "question": "데이터베이스의 특정 열만 암호화하거나 SQL 수준에서 암호화하는 방식을 무엇이라 하는가?", "answer": "API 방식 (또는 플러그인 방식)", "commentary": "애플리케이션 수정을 동반하기도 합니다."},
        {"id": 445, "exam_info": "공통 핵심", "subject": "정보보호 관리", "question": "서비스 중단 시 허용 가능한 최대 데이터 손실 시점을 의미하는 용어는?", "answer": "RPO (Recovery Point Objective)", "commentary": "백업 주기 결정의 기준이 됩니다."},
        {"id": 446, "exam_info": "주요 키워드", "subject": "네트워크 보안", "question": "HTTP의 보안 버전으로 TLS를 사용하여 데이터를 암호화하는 프로토콜은?", "answer": "HTTPS", "commentary": "기본 포트는 443번입니다."},
        {"id": 447, "exam_info": "주요 키워드", "subject": "네트워크 보안", "question": "DNS 질의 응답 패킷을 가로채서 잘못된 IP 주소를 유도하는 공격은?", "answer": "DNS 스푸핑", "commentary": "파밍 공격의 일종으로 쓰입니다."},
        {"id": 448, "exam_info": "주요 키워드", "subject": "시스템 보안", "question": "프로그램의 취약점을 이용하여 관리자 권한을 획득하는 행위의 통칭은?", "answer": "권한 상승 (Privilege Escalation)", "commentary": "공격의 중간 단계에서 매우 중요합니다."},
        {"id": 449, "exam_info": "주요 키워드", "subject": "애플리케이션 보안", "question": "사용자로부터 입력받은 값을 필터링하지 않고 검색 쿼리 등에 직접 사용할 때 발생하는 취약점은?", "answer": "인젝션 취약점", "commentary": "PreparedStatement 사용이 필수적입니다."},
        {"id": 450, "exam_info": "주요 키워드", "subject": "정보보호 관리", "question": "정보보호의 기밀성, 무결성, 가용성 중 가용성을 저해하는 대표적인 공격 방식은?", "answer": "DoS / DDoS", "commentary": "서비스 자체를 마비시키는 것이 목적입니다."}
    ]

    # 추가 50개 자동 생성 (간략한 핵심 문답)
    topics = [
        ("네트워크", "IP 주소를 MAC 주소로 바꾸는 것은?", "ARP", "주소 결정 프로토콜입니다."),
        ("네트워크", "MAC 주소를 IP 주소로 바꾸는 것은?", "RARP", "역주소 결정 프로토콜입니다."),
        ("시스템", "파일을 찾는 리눅스 명령어는?", "find", "조건부 검색이 가능합니다."),
        ("시스템", "로그인을 시도한 기록(실패)을 확인하는 명령어는?", "lastb", "btmp 파일을 참조합니다."),
        ("시스템", "현재 로그인한 사람을 확인하는 명령어는?", "who", "utmp 정보를 줍니다."),
        ("암호학", "AES는 블록 크기가 몇 비트인가?", "128비트", "표준 암호 알고리즘입니다."),
        ("암호학", "DES의 키 길이는 몇 비트인가?", "56비트", "현재는 안정성이 낮아 사용되지 않습니다."),
        ("웹보안", "파일 업로드 시 확장자를 검사하지 않을 때 발생하는 것은?", "악성 파일 업로드", "웹쉘 등으로 이어집니다."),
        ("웹보안", "디렉터리 탐색 시 사용하는 상위 경로 이동 문자는?", "../", "디렉터리 트래버설에 쓰입니다."),
        ("법규", "개인정보 유출 신고 시 지체 없이 보고해야 하는 기준 인원(국내)?", "1,000명 이상", "규모에 따라 신고 의무가 강화됩니다."),
        ("네트워크", "OSI 7계층 중 3계층 장비는?", "라우터", "IP 기반 경로 결정을 합니다."),
        ("네트워크", "OSI 7계층 중 2계층 장비는?", "스위치 / 브리지", "MAC 기반 전송을 합니다."),
        ("시스템", "파일 끝부분을 감시하는 리눅스 옵션은?", "-f (tail -f)", "실시간 로그 확인에 필수입니다."),
        ("애플리케이션", "모바일 앱에서 데이터를 가로채 분석하는 프록시 도구는?", "Burp Suite / Fiddler", "보안 진단에 자주 쓰입니다."),
        ("정보보호", "위험을 제3자에게 넘기는 방식은?", "위험 전가", "보험 가입이 예시입니다."),
        ("암호학", "대칭키 암호화 방식 중 하나로 한국에서 개발된 것은?", "ARIA / SEED", "국산 표준 암호입니다."),
        ("네트워크", "가상 사설망을 구축하는 기술은?", "VPN", "터널링과 암호화를 사용합니다."),
        ("네트워크", "VPN 구축 시 사용하는 프로토콜 한 가지?", "IPsec / SSL", "가장 대표적인 두 방식입니다."),
        ("웹보안", "자바스크립트의 도큐먼트 쿠키 접근을 막는 속성은?", "HttpOnly", "XSS 하이재킹 방지용입니다."),
        ("시스템", "리눅스에서 프로세스를 종료하는 명령어는?", "kill", "-9 시그널이 가장 강력합니다."),
        ("시스템", "프로세스 PID를 확인하는 명령어는?", "ps", "현재 실행 상태를 봅니다."),
        ("암호학", "해시 함수 중 현재 가장 권장되는 버전은?", "SHA-2 / SHA-3", "SHA-256 등이 포함됩니다."),
        ("애플리케이션", "데이터베이스 보안 중 접근을 통제하는 것은?", "DB 접근제어", "인가된 사용자만 접근하게 합니다."),
        ("법규", "가명처리를 통해 개인정보의 활용도를 높이는 것은?", "가명정보", "통계 작성, 연구 등에 쓰입니다."),
        ("정보보호", "ISMS-P의 인증 기관은?", "한국인터넷진흥원 (KISA)", "국가 지정 인증 기관입니다."),
        ("네트워크", "네트워크의 논리적 분할 기술은?", "VLAN", "브로드캐스트 도메인을 나눕니다."),
        ("네트워크", "무차별 모드로 패킷을 엿듣는 행위는?", "스니핑", "암호화되지 않은 통신은 유출됩니다."),
        ("시스템", "파일 생성 시 기본 권한을 차감하는 설정 값은?", "umask", "일반적으로 002, 022입니다."),
        ("암호학", "키 교환을 위해 고안된 알고리즘?", "Diffie-Hellman", "이산대수 문제에 기반합니다."),
        ("애플리케이션", "원격지에서 파일을 포함하여 실행시키는 취약점은?", "RFI (Remote File Inclusion)", "allow_url_include 설정과 관련 있습니다."),
        ("법규", "개인정보 보호를 위한 최고 책임자의 약칭은?", "CPO", "Chief Privacy Officer입니다."),
        ("정보보호", "정보보호 최고 책임자의 약칭은?", "CISO", "Chief Information Security Officer입니다."),
        ("네트워크", "상태 기반 패킷 조사를 하는 장비는?", "상태 기반 방화벽", "Stateful Inspection입니다."),
        ("네트워크", "내부망과 외부망 사이의 중계 서버는?", "프록시 서버", "캐싱 및 보안 역할을 합니다."),
        ("시스템", "리눅스에서 CPU 정보를 담고 있는 가상 파일은?", "/proc/cpuinfo", "시스템 정보를 확인합니다."),
        ("시스템", "윈도우에서 명령프롬프트를 실행하는 실행 파일명은?", "cmd.exe", "명령어 기반 인터페이스입니다."),
        ("암호학", "비트 단위로 암호화가 진행되는 방식은?", "스트림 암호", "RC4 등이 있습니다."),
        ("웹보안", "파라미터에 스크립트를 넣어 보내는 XSS 방식은?", "반사형 XSS", "이메일 링크 등을 통해 전파됩니다."),
        ("애플리케이션", "쿠키 탈취를 방지하기 위해 HTTPS에서만 전송되게 하는 설정은?", "Secure 속성", "암호화 채널에서만 쿠키를 보냅니다."),
        ("법규", "개인정보가 유출됐을 때 정당한 사유가 없으면 몇 시간 내 신고해야 하는가?", "72시간", "기술적/관리적 조치 미흡 시 책임이 큽니다."),
        ("네트워크", "TCP 세션 연결 끊기 위해 보내는 플래그?", "FIN", "정상 종료 절차의 시작입니다."),
        ("네트워크", "강제로 세션을 리셋시키기 위해 보내는 플래그?", "RST", "강제 종료 시 사용합니다."),
        ("시스템", "리눅스 시스템 로그 설정 파일은?", "/etc/rsyslog.conf", "로그 수집 방식을 정의합니다."),
        ("정보보호", "자산의 가치를 평가할 때 고려하는 요소는?", "기밀성, 무결성, 가용성", "CIA 3대 요소입니다."),
        ("암호학", "임의의 무작위 값(Salt)을 사용하는 이유는?", "동일 평문-동일 암호문 방지", "레인보우 테이블 무력화 목적입니다."),
        ("웹보안", "SQL 인젝션 방어를 위한 라이브러리 방식은?", "ORM (Object-Relational Mapping)", "내부적으로 Prepared Statement를 씁니다."),
        ("애플리케이션", "세션 ID가 로그인 전후로 변하지 않을 때 발생하는 것은?", "세션 고정 취약점", "로그인 후 세션 갱신이 필요합니다."),
        ("네트워크", "브로드캐스트 도메인을 최소화해야 하는 이유는?", "네트워킹 부하 감소 및 보안", "불필요한 트래픽 노출을 막습니다."),
        ("시스템", "악성코드가 부팅 시 자동 실행되도록 등록하는 윈도우 위치는?", "레지스트리 Run 키", "지속성 유지를 위한 기법입니다."),
        ("보안일반", "로그를 분석하여 사후 추적을 가능하게 하는 것은?", "감사 (Audit)", "책임 추적성 보장을 위해 기록합니다.")
    ]

    for i, (sub, q, a, comm) in enumerate(topics):
        new_data.append({
            "id": 451 + i,
            "exam_info": "핵심 기출",
            "subject": sub,
            "question": q,
            "answer": a,
            "commentary": comm
        })

    # 중복 ID 제외하고 병합
    final_questions = data + [q for q in new_data if q['id'] not in existing_ids]

    # 저장
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_questions, f, ensure_ascii=False, indent=2)
    
    print(f"Update Complete! New questions added: {len(final_questions) - len(data)}")
    print(f"Total Questions: {len(final_questions)}")

if __name__ == "__main__":
    add_new_questions()
