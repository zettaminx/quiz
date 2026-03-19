import json
import sys

def analyze_subjects():
    json_path = "questions.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    all_subjects = {}
    for q in data:
        subj = q.get('subject', '미분류')
        all_subjects[subj] = all_subjects.get(subj, 0) + 1

    with open("subject_analysis.txt", "w", encoding="utf-8") as out:
        out.write("--- 모든 주제 리스트 ---\n")
        for s, c in sorted(all_subjects.items()):
            out.write(f"{s} ({c}개)\n")

        out.write("\n--- '대주제 > 소주제' 형식이 아닌 단일 주제들 ---\n")
        for s, c in sorted(all_subjects.items()):
            if ">" not in s:
                out.write(f"- {s} ({c}개)\n")

        out.write("\n--- 소주제가 포함된 대주제 그룹 분석 ---\n")
        groups = {}
        for s in all_subjects:
            if ">" in s:
                parts = s.split(">")
                main_cat = parts[0].strip()
                sub_cat = ">".join(parts[1:]).strip()
                if main_cat not in groups:
                    groups[main_cat] = []
                groups[main_cat].append(sub_cat)
        
        for main, subs in sorted(groups.items()):
            out.write(f"[{main}] 에 속한 소주제들:\n")
            for sub in sorted(subs):
                out.write(f"  * {sub}\n")

if __name__ == "__main__":
    analyze_subjects()
