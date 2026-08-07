import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")

EXAMPLES = [
    "Siła małych kroków",
    "Miłość do siebie",
    "Jak radzić sobie ze stresem",
    "Techniki relaksacji",
    "Zdrowe granice w relacjach",
    "Rozwój emocjonalnej inteligencji",
    "Budowanie motywacji wewnętrznej",
    "Terapia poznawczo-behawioralna dla początkujących",
    "Mindfulness w codziennym życiu",
    "Jak przebaczyć sobie i innym",
    "Asertywność a agresja",
    "Radzenie sobie z lękiem",
    "Budowanie poczucia własnej wartości",
    "Komunikacja bez przemocy",
    "Zarządzanie emocjami w pracy",
    "Psychologia pozytywna w praktyce",
    "Jak tworzyć zdrowe nawyki",
    "Rozpoznawanie manipulacji",
    "Współczucie dla siebie (self-compassion)",
    "Jak budować trwałe relacje"
]


def generate_polish_psychology_topics(num_topics=100):
    """Generate Polish psychology/self-improvement topics using Pollinations AI."""

    system = (
        "You are a psychology expert generating topics in Polish. "
        "Do NOT generate children's stories. Do NOT generate animal topics. "
        "Generate topics about: self-help, psychology, mindfulness, emotional intelligence, "
        "motivation, self-compassion, healthy boundaries, personal growth, mental health, "
        "cognitive behavioral therapy, resilience, stress management, communication skills, "
        "emotional regulation, trauma healing, attachment styles, positive psychology. "
        "Topics must be in Polish. One topic per line, no numbering. "
        "Each topic should be 3-8 words, inspiring and specific."
    )

    prompt = (
        f"Generate {num_topics} Polish psychology and self-improvement topics.\n\n"
        f"Examples of good topics:\n"
        + "\n".join(f"- {ex}" for ex in EXAMPLES) +
        "\n\nTopics should cover:\n"
        "- Self-help and personal development (rozwój osobisty)\n"
        "- Mindfulness and meditation (medytacja, uważność)\n"
        "- Emotional intelligence (inteligencja emocjonalna)\n"
        "- Healthy relationships and boundaries (zdrowe granice)\n"
        "- Stress and anxiety management (zarządzanie stresem)\n"
        "- Self-compassion and self-love (miłość do siebie)\n"
        "- Communication and assertiveness (asertywność)\n"
        "- Trauma and healing (leczenie ran)\n"
        "- Positive psychology (psychologia pozytywna)\n"
        "- Motivation and habits (motywacja, nawyki)\n\n"
        "IMPORTANT: Each topic must be unique, specific, and in Polish. "
        "One topic per line, no numbering. No children's stories, no animals."
    )

    url = "https://gen.pollinations.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.2
    }

    print(f"[topics] Generating {num_topics} Polish psychology topics...")

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"].strip()

        topics = [line.strip() for line in text.split('\n') if line.strip()]

        cleaned_topics = []
        for topic in topics:
            topic = topic.lstrip('0123456789.-) ')
            if len(topic) > 5 and not topic.startswith('['):
                cleaned_topics.append(topic)

        if len(cleaned_topics) < num_topics:
            print(f"[topics] {len(cleaned_topics)} generated, supplementing with fallback...")
            fallback_needed = num_topics - len(cleaned_topics)
            cleaned_topics.extend(get_fallback_topics()[:fallback_needed])

        return cleaned_topics[:num_topics]

    except Exception as e:
        print(f"[topics] API error: {e}. Using local topics.")
        return get_fallback_topics()[:num_topics]


def get_fallback_topics():
    """200 Polish psychology/self-improvement topics (fallback when API is unavailable)."""
    return [
        "Siła małych kroków",
        "Miłość do siebie",
        "Jak radzić sobie ze stresem",
        "Techniki relaksacji",
        "Zdrowe granice w relacjach",
        "Rozwój emocjonalnej inteligencji",
        "Budowanie motywacji wewnętrznej",
        "Mindfulness w codziennym życiu",
        "Jak przebaczyć sobie i innym",
        "Asertywność a agresja",
        "Radzenie sobie z lękiem",
        "Budowanie poczucia własnej wartości",
        "Komunikacja bez przemocy",
        "Zarządzanie emocjami w pracy",
        "Psychologia pozytywna w praktyce",
        "Jak tworzyć zdrowe nawyki",
        "Rozpoznawanie manipulacji",
        "Współczucie dla siebie",
        "Jak budować trwałe relacje",
        "Oddychanie jako narzędzie uspokajania",
        "Akceptacja niepewności",
        "Praca z inner child",
        "Rozpoznawanie emocji w ciele",
        "Technika PET",
        "Zasada 5 sekund",
        "Cykl stresu i regeneracji",
        "Radzenie sobie z perfekcjonizmem",
        "Empatia a współczucie",
        "Jak mówić nie bez poczucia winy",
        "Terapia akceptacji i zaangażowania",
        "Budowanie odporności psychicznej",
        "Rozpoznawanie triggers",
        "Self-compassion w trudnych chwilach",
        "Jak radzić sobie z odrzuceniem",
        "Techniki grounding",
        "Praca z przekonaniami ograniczającymi",
        "Zdrowe wyrażanie złości",
        "Jak budować pewność siebie",
        "Psychologia zmiany nawyków",
        "Rozpoznawanie toksycznych relacji",
        "Technika mindful eating",
        "Jak radzić sobie z krytyką",
        "Budowanie poczucia bezpieczeństwa",
        "Praca z cieniem osobowości",
        "Jak tworzyć rutynę poranną",
        "Technika EFT na stres",
        "Empatia wobec siebie",
        "Rozpoznawanie emocji u dzieci",
        "Jak budować zaufanie",
        "Praca z traumą",
        "Technika body scan",
        "Zdrowe granice z rodziną",
        "Jak radzić sobie z żałobą",
        "Mindful communication",
        "Praca z inner critic",
        "Jak tworzyć przestrzeń dla siebie",
        "Technika progressive muscle relaxation",
        "Budowanie samoświadomości",
        "Rozpoznawanie schematów",
        "Jak przełamywać prokrastynację",
        "Technika journaling",
        "Zdrowe podejście do sukcesu",
        "Praca z lękiem przed odrzuceniem",
        "Jak budować wsparcie społeczne",
        "Technika cognitive restructuring",
        "Rozwojowe podejście do porażek",
        "Jak radzić sobie z wypaleniem zawodowym",
        "Mindful parenting",
        "Praca z emocjonalnymi wzorcami",
        "Jak budować odporność na stres",
        "Technika VALUES exercise",
        "Zdrowe granice w związku",
        "Jak tworzyć pozytywną atmosferę",
        "Praca z przeszłością",
        "Jak rozwijać inteligencję emocjonalną",
        "Technika opposite action",
        "Budowanie poczucia sensu",
        "Rozpoznawanie potrzeb",
        "Jak radzić sobie z samotnością",
        "Praca z internalized beliefs",
        "Technika 5-4-3-2-1 na lęk",
        "Zdrowe wyrażanie potrzeb",
        "Jak budować pewność w relacjach",
        "Mindful movement",
        "Praca z inner child w dorosłości",
        "Jak przełamywać strach przed zmianą",
        "Technika ACT na niepokój",
        "Budowanie samoakceptacji",
        "Rozpoznawanie granic",
        "Jak radzić sobie z krytykiem wewnętrznym",
        "Praca z przekonaniami",
        "Technika self-compassion break",
        "Zdrowe podejście do sukcesu",
        "Jak budować pozytywne nawyki",
        "Mindful listening",
        "Praca z emocjami w ciele",
        "Jak tworzyć harmonię w życiu",
        "Technika STOP na stres",
        "Budowanie relaksu",
        "Rozpoznawanie emocjonalnych triggerów",
        "Jak radzić sobie z niepewnością",
        "Praca z lękiem o przyszłość",
        "Technika radical acceptance",
        "Zdrowe granice w przyjaźni",
        "Jak budować poczucie własnej wartości",
        "Mindful technology use",
        "Praca z internal critic",
        "Jak tworzyć zdrowe relacje",
        "Technika DBT distress tolerance",
        "Budowanie odporności emocjonalnej",
        "Rozpoznawanie potrzeb emocjonalnych",
        "Jak radzić sobie z żalem",
        "Praca z przeszłością w terapii",
        "Technika positive self-talk",
        "Zdrowe podejście do ciała",
        "Jak budować pewność siebie",
        "Mindful walking",
        "Praca z emocjami w relacjach",
        "Jak tworzyć balance w życiu",
        "Technika gratitude journal",
        "Budowanie samoświadomości",
        "Rozpoznawanie schematów relacyjnych",
        "Jak radzić sobie z poczuciem winy",
        "Praca z traumą relational",
        "Technika grounding 5 senses",
        "Zdrowe granice w pracy",
        "Jak budować zaufanie do siebie",
        "Mindful breathing",
        "Praca z emocjonalnymi blokadami",
        "Jak przełamywać lęk przed odrzuceniem",
        "Technika interoception awareness",
        "Budowanie kompetencji emocjonalnej",
        "Rozpoznawanie cykli emocjonalnych",
        "Jak radzić sobie z zazdrością",
        "Praca z potrzebą kontroli",
        "Technika self-soothing",
        "Zdrowe wyrażanie granic",
        "Jak budować bliskość emocjonalną",
        "Mindful eating na co dzień",
        "Praca z emocjonalnymi wzorcami rodzinnymi",
        "Jak tworzyć zmianę w życiu",
        "Technika behavioral activation",
        "Budowanie odporności psychicznej",
        "Rozpoznawanie emocji w relacjach",
        "Jak radzić sobie z samotnością w związku",
        "Praca z lękiem społecznym",
        "Technika exposure therapy",
        "Zdrowe podejście do konfliktów",
        "Jak budować asertywność",
        "Mindful movement exercise",
        "Praca z inner child wounds",
        "Jak przełamywać nawyk unikania",
        "Technika acceptance and commitment",
        "Budowanie stabilności emocjonalnej",
        "Rozpoznawanie potrzeb partnera",
        "Jak radzić sobie z traumą",
        "Praca z emocjonalną odpornością",
        "Technika emotional regulation skills",
        "Zdrowe granice z rodzicami",
        "Jak budować niezależność emocjonalną",
        "Mindful communication skills",
        "Praca z internalized shame",
        "Jak tworzyć pozytywne relacje",
        "Technika distress tolerance skills",
        "Budowanie samoakceptacji w relacjach",
        "Rozpoznawanie emocjonalnych potrzeb",
        "Jak radzić sobie z odrzuceniem",
        "Praca z przekonaniami o sobie",
        "Technika radical self-care",
        "Zdrowe podejście do emocji",
        "Jak budować odporność na krytykę",
        "Mindful stress management",
        "Praca z emocjonalnymi ranami",
        "Jak przełamywać lęk przed zmianą",
        "Technika emotional freedom technique",
        "Budowanie zdrowych nawyków relacyjnych",
        "Rozpoznawanie schematów unikania",
        "Jak radzić sobie z żałobą",
        "Praca z lękiem separacyjnym",
        "Technika body-based regulation",
        "Zdrowe wyrażanie emocji",
        "Jak budować poczucie przynależności",
        "Mindful relationships",
        "Praca z emocjonalnymi blokadami",
        "Jak tworzyć zmianę nawyków",
        "Technika cognitive defusion",
        "Budowanie stabilności psychicznej",
        "Rozpoznawanie emocjonalnych triggerów",
        "Jak radzić sobie z poczuciem winy",
        "Praca z internalized beliefs",
        "Technika values clarification",
        "Zdrowe granice w rodzinie",
        "Jak budować odporność emocjonalną",
        "Mindful self-care",
        "Praca z inner critic voices",
        "Jak przełamywać nawyk kontrolowania",
        "Technika dialectical behavior therapy",
        "Budowanie samoświadomości relacyjnej",
        "Rozpoznawanie potrzeb emocjonalnych",
        "Jak radzić sobie z stresem",
        "Praca z emocjonalnymi wzorcami",
        "Technika window of tolerance",
        "Zdrowe podejście do zmian",
        "Jak budować poczucie sensu",
        "Mindful awareness",
        "Praca z emocjonalnymi ranami",
        "Jak tworzyć zdrowe relacje",
        "Technika self-regulation",
        "Budowanie odporności na stres",
        "Rozpoznawanie emocjonalnych potrzeb",
        "Jak radzić sobie z lękiem o przyszłość",
        "Praca z przeszłością",
        "Technika emotional agility",
        "Zdrowe wyrażanie granic",
        "Jak budować bliskość",
        "Mindful emotional awareness",
    ]


def save_topics_to_file(topics, filename="topics.txt"):
    """Save topics to file."""
    with open(filename, "w", encoding="utf-8") as f:
        for topic in topics:
            f.write(f"{topic}\n")
    print(f"[topics] Saved {len(topics)} topics to {filename}")


def main():
    """Check if topics.txt has < 50 topics and generate more if needed."""
    load_dotenv()

    topics_file = "topics.txt"

    if os.path.exists(topics_file):
        with open(topics_file, "r", encoding="utf-8") as f:
            existing_topics = [line.strip() for line in f if line.strip()]
    else:
        existing_topics = []

    print(f"[topics] Current topics: {len(existing_topics)}")

    if len(existing_topics) >= 50:
        print(f"[topics] Enough topics available ({len(existing_topics)})")
        return

    print(f"[topics] Low on topics! Generating 100 more...")
    new_topics = generate_polish_psychology_topics(100)

    all_topics = existing_topics + new_topics
    unique_topics = []
    seen = set()
    for topic in all_topics:
        if topic.lower() not in seen:
            unique_topics.append(topic)
            seen.add(topic.lower())

    save_topics_to_file(unique_topics)
    print(f"[topics] Total topics now: {len(unique_topics)}")


if __name__ == '__main__':
    main()
