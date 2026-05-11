import math
from collections import Counter
from resumedataset import resumedata
from jobdescriptiondataset import jobdescriptiondata
from skillaliases import skillaliases

def normalizeskills(rawskills):
    skills = []
    for skill in raw_skills.split(","):
        skill = skill.strip().lower()
        if skill in skill_aliases:
            skills.append(skill_aliases[skill])
    return skills

def deduplicate_skills(skills):
    return list(set(skills))

def buildvocabulary(resumedata):
    vocabulary = set()
    for resume in resume_data:
        skills = normalizeskills(resume["rawskills"])
        vocabulary.update(skills)
    return sorted(list(vocabulary))

def computetfidf(resume_data, vocabulary):
    tfidfvectors = []
    for resume in resume_data:
        skills = normalizeskills(resume["rawskills"])
        tfidfvector = []
        for skill in vocabulary:
            tf = skills.count(skill) / len(skills)
            idf = math.log(10 / sum(1 for r in resumedata if skill in normalizeskills(r["raw_skills"])))
            tfidfvector.append(tf * idf)
        tfidfvectors.append(tfidfvector)
    return tfidfvectors

def buildjdvectors(jobdescriptiondata, vocabulary):
    jd_vectors = []
    for jd in jobdescriptiondata:
        requiredskills = [skill.lower() for skill in jd["requiredskills"]]
        preferredskills = [skill.lower() for skill in jd["preferredskills"]]
        jd_vector = []
        for skill in vocabulary:
            if skill in requiredskills or skill in preferredskills:
                jd_vector.append(1)
            else:
                jd_vector.append(0)
        jdvectors.append(jdvector)
    return jd_vectors

def computecosinesimilarity(tfidfvectors, jd_vectors):
    similarities = []
    for tfidfvector in tfidfvectors:
        similarities.append([])
        for jdvector in jdvectors:
            dotproduct = sum(a * b for a, b in zip(tfidfvector, jdvector))
            magnitudea = math.sqrt(sum(a  2 for a in tfidf_vector))
            magnitudeb = math.sqrt(sum(b  2 for b in jdvector))
            similarity = dotproduct / (magnitudea * magnitude_b)
            similarities[-1].append(similarity)
    return similarities

def rank_candidates(similarities):
    ranked_candidates = []
    for i, similarity in enumerate(similarities):
        rankedcandidates.append((resumedata[i]["candidate"], similarity))
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    return ranked_candidates

def main():
    vocabulary = buildvocabulary(resumedata)
    tfidfvectors = computetfidf(resume_data, vocabulary)
    jdvectors = buildjdvectors(jobdescription_data, vocabulary)
    similarities = computecosinesimilarity(tfidfvectors, jd_vectors)
    rankedcandidates = rankcandidates(similarities)
    for jdid, jd in enumerate(jobdescription_data):
        print(f"JD-{jd_id+1} — {jd['company']} ({jd['role']})")
        for candidate, similarity in rankedcandidates[jdid][:3]:
            print(f"{candidate} ({similarity:.2f})")

if name == "main":
    main()