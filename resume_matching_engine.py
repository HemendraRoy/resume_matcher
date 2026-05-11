import math
from collections import Counter
from resume_dataset import resume_data
from job_description_dataset import jobdescriptiondata
from skill_aliases import skill_aliases

def normalize_skills(raw_skills):
    skills = []
    for skill in raw_skills.split(","):
        skill = skill.strip().lower()
        if skill in skill_aliases:
            skills.append(skill_aliases[skill])
    return skills

def deduplicate_skills(skills):
    return list(set(skills))

def build_vocabulary(resume_data):
    vocabulary = set()
    for resume in resume_data:
        skills = normalize_skills(resume["raw_skills"])
        vocabulary.update(skills)
    return sorted(list(vocabulary))

def compute_tfidf(resume_data, vocabulary):
    tfidf_vectors = []
    for resume in resume_data:
        skills = normalize_skills(resume["raw_skills"])
        tfidf_vector = []
        for skill in vocabulary:
            tf = skills.count(skill) / len(skills) if skills else 0
            idf = math.log(10 / sum(1 for r in resume_data if skill in normalize_skills(r["raw_skills"])))
            tfidf_vector.append(tf * idf)
        tfidf_vectors.append(tfidf_vector)
    return tfidf_vectors

def build_jd_vectors(jobdescriptiondata, vocabulary):
    jd_vectors = []
    for jd in jobdescriptiondata:
        required_skills = [skill.lower() for skill in jd["required_skills"]]
        preferred_skills = [skill.lower() for skill in jd["preferred_skills"]]
        jd_vector = []
        for skill in vocabulary:
            if skill in required_skills or skill in preferred_skills:
                jd_vector.append(1)
            else:
                jd_vector.append(0)
        jd_vectors.append(jd_vector)
    return jd_vectors

def compute_cosine_similarity(tfidf_vectors, jd_vectors):
    similarities = []
    for tfidf_vector in tfidf_vectors:
        similarities.append([])
        for jd_vector in jd_vectors:
            dot_product = sum(a * b for a, b in zip(tfidf_vector, jd_vector))
            magnitude_a = math.sqrt(sum(a**2 for a in tfidf_vector))
            magnitude_b = math.sqrt(sum(b**2 for b in jd_vector))
            similarity = dot_product / (magnitude_a * magnitude_b) if magnitude_a * magnitude_b != 0 else 0
            similarities[-1].append(similarity)
    return similarities

def rank_candidates(similarities, resume_data):
    ranked_candidates = []
    for i, similarity in enumerate(similarities):
        ranked_candidates.append((resume_data[i]["candidate"], similarity))
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    return ranked_candidates

def main():
    vocabulary = build_vocabulary(resume_data)
    tfidf_vectors = compute_tfidf(resume_data, vocabulary)
    jd_vectors = build_jd_vectors(jobdescriptiondata, vocabulary)
    similarities = compute_cosine_similarity(tfidf_vectors, jd_vectors)
    for jdid, jd in enumerate(jobdescriptiondata):
        print(f"JD-{jdid+1} — {jd['company']} ({jd['role']})")
        ranked_candidates = rank_candidates([s[jdid] for s in similarities], resume_data)
        for candidate, similarity in ranked_candidates[:3]:
            print(f"{candidate} ({similarity:.2f})")

if __name__ == "__main__":
    main()
