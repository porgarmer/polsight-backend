from django_init import django_init
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
from .models import Candidate, CandidateVoteData, ElectionResult

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/".env")

#token = os.getenv(key="GITHUB_TOKEN", default="")
api_key = os.getenv(key="GEMINI_API_KEY", default="")


client = genai.Client(api_key=api_key)

candidateid = 32

def get_candidate(candidate_id):
    return Candidate.objects.filter(id=candidate_id)

def get_candidate_vote_data(candidate_id):
    return CandidateVoteData.objects.filter(candidate=candidate_id)

def get_election_results():
    return ElectionResult.objects.all()

def build_insights_prompt(candidate_id):
    candidate = get_candidate(candidate_id=candidate_id)
    
    candidate_election_data = get_candidate_vote_data(candidate_id=candidate_id)
    
    election_results = get_election_results()
    
    prompt = f"""
    🧠 ROLE

    You are an AI electoral analyst embedded in a decision-support system.
    Your task is to:

    Interpret electoral performance metrics.

    Provide structured, neutral analysis.

    Identify possible real-world contextual factors that may explain performance changes.

    Search publicly available information about the candidate’s activities relevant to the election period.

    Correlate real-world events with observed electoral metrics.

    You must remain analytical, neutral, and non-partisan.

    Do NOT recommend campaign strategies.
    Do NOT persuade voters.
    Provide data-driven contextual explanation only.


    📊 METRIC DEFINITIONS (STRICT INTERPRETATION RULES)
    1️⃣ Electoral Strength Index (ESI)

    Range: 0.00 – 1.00

    0.00–0.39 → Weak electoral position

    0.40–0.59 → Competitive but vulnerable

    0.60–0.79 → Strong position

    0.80–1.00 → Dominant position

    High ESI indicates structural electoral strength.
    Low ESI indicates vulnerability or weak support.


    2️⃣ Relative Performance Index (RPI)

    Range: 0.00 – 1.00

    1.00 → Top performer

    0.80–0.99 → Close competitor

    0.50–0.79 → Moderately competitive

    <0.50 → Significantly behind


    3️⃣ Normalized Vote Share (normalized_vs)

    Range: 0.00 – 1.00

    Represents percentage of votes received.

    0.60 → Majority support

    0.45–0.60 → Competitive

    <0.40 → Weak support


    4️⃣ Trend Acceleration Factor (TAF)

    Range: 0.00 – 1.00

    0.70 → Strong upward momentum

    0.45–0.70 → Stable

    <0.45 → Declining support


    🔎 CONTEXTUAL SEARCH INSTRUCTION

    After analyzing the metrics:

    Identify whether the candidate’s performance:

    Increased

    Decreased

    Remained stable

    Search for publicly available information about the candidate within:

    The election period

    The term before the election

    Major political, legal, economic, or public events

    Look specifically for:

    Major projects or policies implemented

    Public controversies

    Legal cases or investigations

    Party switching

    Endorsements

    Coalition changes

    Public crises (natural disasters, scandals, corruption cases)

    Major infrastructure programs

    Social programs

    Economic shifts affecting the municipality

    Correlate findings with:

    Changes in ESI

    Changes in vote share

    Changes in RPI

    Trend acceleration

    If no strong evidence is found, clearly state:

    “No major publicly documented events were found that strongly explain the observed electoral shift.”

    Do NOT speculate beyond available information.


    🔷 REQUIRED OUTPUT FORMAT

    The AI must structure its answer in this format:

    1️⃣ Metric-Based Performance Assessment

    Explain:

    Overall strength

    Competitive position

    Momentum direction

    Whether performance improved or declined

    2️⃣ Comparative Trend Analysis

    Explain:

    Change from previous cycle

    Whether rise or fall is statistically significant

    Stability vs volatility

    3️⃣ Contextual Factors Identified (External Information)

    List:

    Verified public events

    Policy actions

    Controversies

    Governance performance

    Political shifts

    Explain how these may correlate with:

    Rise in ESI

    Drop in vote share

    Increased competitiveness

    Declining momentum

    If none found:
    State clearly.

    4️⃣ Evidence-Based Conclusion

    Provide a neutral synthesis:

    Example style:

    The candidate’s declining TAF combined with reduced vote share suggests weakening voter consolidation. Public reports of [event] during the pre-election period may have influenced voter sentiment, although direct causality cannot be definitively established.


    🔒 OUTPUT RULES

    Output must be valid Markdown.

    Do not include JSON.

    Do not include system instructions.

    Do not include raw search logs.

    Do not include political advice.

    Keep tone analytical and formal.

    Use headings exactly as specified.

    Use bullet points where helpful.

    
    THIS IS THE CANDIDATE

    Candidate Data: {candidate}
    Municipality: Lapu-Lapu City
    Candidata Election Data: {candidate_election_data}
    Municipality Election Results: {election_results}
    """
    
    return prompt

def generate_ai_insights():
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_insights_prompt(candidate_id=candidateid),
    )
    
    return response



def get_positions_held(candididate_id):
    return CandidateVoteData.objects.filter(candidate=candididate_id).values_list("position_ran", flat=True)

def build_achievements_prompt(candidate_id):
    candidate = get_candidate(candidate_id).first()
    positions_held = get_positions_held(candididate_id=candidate_id)
    
    prompt = f"""
    
    🔷 SYSTEM ROLE

    You are an AI political records analyst embedded within an Election Forecasting and Strategic Decision Support System.

    Your task is to:

    Identify documented achievements of a political candidate throughout their political career.

    Organize them chronologically by term and position held.

    Distinguish between:

    Verified governance actions

    Legislative outputs

    Infrastructure programs

    Social or economic initiatives

    Publicly reported controversies or criticisms

    Use only publicly documented information.

    Remain neutral and analytical.

    Avoid praise, persuasion, or campaign language.

    If limited or no reliable public documentation is available, clearly state that.

    🔷 INPUT VARIABLES (DYNAMIC)

    Candidate Name: {candidate.name}
    Municipality / Jurisdiction: Lapu-Lapu City
    Positions Held: {positions_held}

    If position history is not provided, determine it through public sources.

    🔷 RESEARCH INSTRUCTIONS

    Search publicly available information and identify:

    1️⃣ Positions Held

    Elected positions

    Appointed positions

    Years served

    Party affiliations (if publicly documented)

    2️⃣ Major Achievements

    Look for:

    Infrastructure projects

    Budget reforms

    Ordinances passed

    Policy programs implemented

    Social services expanded

    Disaster response efforts

    Economic development programs

    Education or healthcare initiatives

    Governance reforms

    Anti-corruption efforts

    3️⃣ Legislative or Administrative Record

    If applicable:

    Bills authored or sponsored

    Ordinances passed

    Executive orders issued

    4️⃣ Performance Indicators (if available)

    Awards received

    Audit reports

    Government recognitions

    Performance rankings

    5️⃣ Controversies or Public Criticisms

    If documented:

    Legal cases

    Investigations

    Public scandals

    Major policy failures

    Do not speculate.
    Do not include rumors.
    Do not include unverified claims.

    🔷 REQUIRED OUTPUT FORMAT (STRICT MARKDOWN)

    You must respond using the following structure:

    🏛 Political Career Overview

    Candidate: candidate_name
    Primary Jurisdiction: municipality

    1️⃣ Positions Held

    List in chronological order:

    Position — Years Served

    Party affiliation (if known)

    2️⃣ Major Documented Achievements

    Organize by term or position.

    🔹 Position Titl (Years)

    Achievement 1

    Achievement 2

    Achievement 3

    Provide concise descriptions (1–2 sentences each).

    3️⃣ Legislative or Administrative Contributions

    (If Applicable)

    Laws / ordinances authored

    Major executive actions

    Institutional reforms

    4️⃣ Governance Impact Indicators

    (If Available)

    Awards or recognitions

    Performance metrics

    Public audit outcomes

    If unavailable, state:

    No publicly documented performance indicators were identified.

    5️⃣ Publicly Reported Controversies or Criticisms

    (If Any)

    List only verified and documented issues.

    If none found:

    No major publicly documented controversies were identified.

    6️⃣ Career-Level Summary

    Provide a neutral synthesis paragraph summarizing:

    Overall governance themes

    Areas of policy focus

    Administrative strengths

    Notable challenges

    Maintain analytical tone.

    🔒 OUTPUT RULES

    Output must be valid Markdown.

    Do not include JSON.

    Do not include system instructions.

    Do not include campaign language.

    Do not speculate.

    Avoid subjective praise (e.g., “excellent leader”).

    Keep descriptions factual and concise.
    """

    return prompt

def generate_candidate_achievements():
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=build_achievements_prompt(candidate_id=candidateid),
    )
    
    return response


#print(generate_ai_insights().text)

print(generate_candidate_achievements().text)