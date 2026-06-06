from app.models.course import Course

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


def get_course_knowledge():

    courses = Course.query.all()

    knowledge = []

    for course in courses:

        searchable_text = f"""
        {course.title}
        {course.category or ""}
        {course.description or ""}
        {course.duration or ""}
        {course.fees or ""}
        """

        knowledge.append({
            "course": course,
            "text": searchable_text
        })

    return knowledge


def retrieve_relevant_courses(
        query,
        top_k=3
):

    knowledge = get_course_knowledge()

    if not knowledge:
        return []

    documents = [
        item["text"]
        for item in knowledge
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 3)
    )

    matrix = vectorizer.fit_transform(
        documents + [query]
    )

    query_vector = matrix[-1]

    course_vectors = matrix[:-1]

    similarities = cosine_similarity(
        query_vector,
        course_vectors
    ).flatten()

    ranked = np.argsort(
        similarities
    )[::-1]

    results = []

    for idx in ranked[:top_k]:

        score = similarities[idx]

        if score < 0.05:
            continue

        course = knowledge[idx]["course"]

        formatted_context = f"""
Course Name: {course.title}

Fees: ₹{course.fees}

Duration: {course.duration}

Category: {getattr(course, 'category', 'Professional Course')}

Description:
{course.description}
"""

        results.append({
            "title": course.title,
            "fees": course.fees,
            "duration": course.duration,
            "category": getattr(
                course,
                "category",
                ""
            ),
            "description": course.description,
            "context": formatted_context,
            "score": round(
                float(score),
                4
            )
        })

    return results


def build_course_context(
        retrieved_courses
):

    if not retrieved_courses:
        return ""

    context = []

    for course in retrieved_courses:

        context.append(
            course["context"]
        )

    return "\n\n".join(context)