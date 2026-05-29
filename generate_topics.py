import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv


POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")

EXAMPLES = [
    "Przygoda małego smoka, który bał się ognia, ale nauczył się latać",
    "Wróżka gwiazd, która spadła z nieba pewnego letniego wieczoru",
    "Podróż kropli wody od źródła aż do oceanu",
    "Tajemnica ogrodu, który kwitł tylko nocą",
    "Jak mała chmurka stała się piękną tęczą",
    "Smok, który wolał czytać książki niż ziać ogniem",
    "Zaczarowany klucz, który otwierał drzwi do snów",
    "Legenda o kryształowej górze, która świeciła w świetle księżyca"
]


def generate_polish_kids_topics(num_topics=100):
    """Generate beautiful, imaginative Polish children's story topics."""

    system = (
        "Jesteś autorem bajek dla dzieci z niezwykłą wyobraźnią. "
        "Generuj MAGICZNE i POETYCKIE tytuły bajek dla dzieci (3-8 lat) po polsku. "
        "Każdy tytuł ma przywoływać cudowny świat pełen przygód, magii i czułości. "
        "Różnicuj początek: 'Mały/Mała... który/która...', 'Jak...', 'Przygoda...', "
        "'Podróż...', 'Tajemnica...', 'Legenda...', 'Opowieść o...' "
        "Bez numerów. Każdy tytuł w nowej linii. "
        "Bądź poetycki i oryginalny - unikaj schematów typu 'Pies uczy się...'"
    )

    prompt = (
        f"Wygeneruj {num_topics} unikalnych i pięknych tytułów bajek dla dzieci po polsku."
        f"\n\nPrzykłady pożądanego stylu:"
        f"\n" + "\n".join(f"- {ex}" for ex in EXAMPLES) +
        "\n\nTematy do wykorzystania (różnorodność!):"
        "\n- Magia i fantazja (smoki, wróżki, jednorożce, czarodzieje)"
        "\n- Przygody w naturze (zaczarowane lasy, oceany, góry)"
        "\n- Magiczne przedmioty ożywające (zabawki, książki, instrumenty)"
        "\n- Podróże wyobraźni (do gwiazd, pod wodę, do wnętrza Ziemi)"
        "\n- Przyjaźń i uczucia (odwaga, dobroć, dzielenie się)"
        "\n- Małe codzienne cuda (pory roku, rośliny, zwierzęta)"
        "\n\nWAŻNE: Każdy tytuł ma być niepowtarzalny, poetycki i zachęcać do wysłuchania."
        "\nTylko tytuły, jeden w linii, bez numeracji."
    )

    url = f"https://gen.pollinations.ai/v1/chat/completions"
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
        "temperature": 1.3
    }

    print(f"[topics] Generowanie {num_topics} pięknych polskich tematów bajek...")

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"].strip()

        topics = [line.strip() for line in text.split('\n') if line.strip()]

        cleaned_topics = []
        for topic in topics:
            topic = topic.lstrip('0123456789.-) ')
            if len(topic) > 15 and not topic.startswith('['):
                cleaned_topics.append(topic)

        if len(cleaned_topics) < num_topics:
            print(f"[topics] {len(cleaned_topics)} wygenerowano, uzupełnianie lokalnymi...")
            fallback_needed = num_topics - len(cleaned_topics)
            cleaned_topics.extend(get_fallback_topics()[:fallback_needed])

        return cleaned_topics[:num_topics]

    except Exception as e:
        print(f"[topics] Błąd API: {e}. Używam tematów lokalnych.")
        return get_fallback_topics()[:num_topics]


def get_fallback_topics():
    """200 beautiful Polish story topics (fallback when API is unavailable)."""
    return [
        "Mały smok, który bał się ognia, ale marzył o lataniu",
        "Gwiazdowa wróżka, która spadła z nieba pewnego letniego wieczoru",
        "Podróż kropli wody od źródła aż do oceanu",
        "Tajemnica ogrodu, który rozkwitał tylko nocą",
        "Jak mała chmurka stała się piękną tęczą",
        "Zaczarowana pozytywka, która grała melodię wspomnień",
        "Przygoda papierowego łódeczka, które przepłynęło ocean",
        "Tajemnica starego zegara, który potrafił zatrzymać czas",
        "Legenda o kryształowej górze, która lśniła w blasku księżyca",
        "Kotek, który odkrył ukryte miasto w chmurach",
        "Niezwykła podróż piórka niesionego przez wiatr",
        "Jak mały płatek śniegu nauczył się być wyjątkowym",
        "Tajemnica lasu, w którym drzewa szeptały sekrety",
        "Mała gwiazdka, która chciała bawić się ze świetlikami",
        "Przygoda zaczarowanej książki, której historie ożywały",
        "Magiczne ziarenko, które urosło aż do nieba",
        "Odbicie w wodzie, które stało się najlepszym przyjacielem",
        "Jak kawałek księżyca wpadł do zaczarowanego stawu",
        "Jednorożec, który szukał źródła wszystkich kolorów",
        "Niezwykła podróż jesiennego liścia dookoła świata",
        "Mała czarownica, która warzyła eliksir wiecznej przyjaźni",
        "Miś, który postanowił tańczyć jak motyl",
        "Tajemnica skrzypiec, które roztańczyły leśne zwierzęta",
        "Rakieta zbudowana z zabawek, która poleciała na Marsa",
        "Jak zagubiony uśmiech odnaleziono w studni życzeń",
        "Świetlik, który szukał najpiękniejszego światła na świecie",
        "Latawiec, który wzniósł się tak wysoko, że dotknął gwiazd",
        "Róża, która rozkwitała tylko w srebrnym świetle księżyca",
        "Przygoda bałwanka, który chciał zobaczyć wiosnę",
        "Tajemnica złotego klucza, który otwierał drzwi snów",
        "Mała syrenka, która oddała swój głos za skrzydła do latania",
        "Mały robot, który nauczył się czuć ciepło słońca",
        "Jak Słońce i Księżyc zostali strażnikami nieba",
        "Ukryta grota, w której kryształy śpiewały kołysanki",
        "Dziecko, które rozmawiało ze zwierzętami i rozumiało ich język",
        "Leniwy obłoczek, który nie chciał padać deszczem",
        "Jak zwykły kamyk stał się najcenniejszym skarbem",
        "Wróżka wiosny, która budziła uśpione kwiaty",
        "Stoletnie drzewo, które przechowywało pamięć świata",
        "Podróż promienia słońca przez pory roku",
        "Mała niedźwiedzica, która nauczyła się świecić na nocnym niebie",
        "Tajemnica piasku, który przechowywał ślady stóp",
        "Jak płatek śniegu odnalazł swoją sześciu zagubionych braci",
        "Wydra, która zbudowała najpiękniejszą tamę na rzece",
        "Wiatr, który uczył liście tańczyć",
        "Przygoda butelki z wiadomością, która opłynęła pół świata",
        "Motyl, który na grzbiecie wieloryba przepłynął ocean",
        "Jak małe nasionko mniszka lekarskiego nauczyło się podróżować",
        "Spadająca gwiazda, która szukała przyjaciela na Ziemi",
        "Tajemnica pływającej wyspy ukrytej za mgłą",
        "Mały duszek, który bał się ciemności, ale kochał przytulanie",
        "Jak tęcza nauczyła się, że jest piękna nawet bez swoich kolorów",
        "Zegarek, który cofał czas i należał do dziadka",
        "Podróż łzy radości, która wszędzie wyhodowała kwiaty",
        "Kotka, która tkała kocyki z księżycowych nici",
        "Jak wolny, ale wytrwały ślimak wygrał wielki wyścig",
        "Zwierzęcy jarmark, na którym każdy był mile widziany",
        "Tajemnica lustra, które pokazywało nie twarz, ale serce",
        "Mały pingwin, który chciał nauczyć się latać jak albatros",
        "Jak biedronka z siedmioma kropkami znalazła swoją ósmą kropkę",
        "Legenda latarni morskiej, która prowadziła sny do krainy spokoju",
        "Sowa, która kolekcjonowała historie z całego świata",
        "Żółta drogą z cegieł, która prowadziła do krainy przytulania",
        "Jak uśmiech narysowany na karteczce podróżował z rąk do rąk",
        "Wieloryb, który śpiewał kołysanki dzieciom oceanu",
        "Mały konik na biegunach, który galopował przez dziecięce sny",
        "Magiczna latarnia, która oświetlała ścieżki w ciemności",
        "Jak pluszowy miś nauczył się leczyć smutne serca",
        "Tajemnica fontanny życzeń, która działała tylko o świcie",
        "Przygoda różowej nitki wełny, która zrobiła koc przyjaźni",
        "Dinozaur, który wolał jeść kwiaty niż mięso",
        "Jak kolory jesieni nauczyły się spadać z wdziękiem",
        "Tajemnica domku na drzewie, który co noc zmieniał kraj",
        "Mała filiżanka herbaty, która ogrzewała zimne serca",
        "Podróż świeczki, która oświetliła drogę do domu",
        "Jak kolczasty jeż znalazł miękkich przyjaciół",
        "Opuszczone pianino, które po stu latach znów zagrało",
        "Cień, który chciał być przyjacielem, a nie straszyć",
        "Jak dziura w drzewie stała się drzwiami do zaczarowanego świata",
        "Mały wewnętrzny głos, który nauczył dziecko kochać siebie",
        "Podróż czerwonego szalika przez pory roku i kraje",
        "Waran z Komodo, który marzył o tym, by być łagodnym jak kotek",
        "Jak plama atramentu na kartce stała się arcydziełem",
        "Strażniczka snów, która oddzielała koszmary od pięknych marzeń",
        "Mała lokomotywa, która bała się wyjechać z tunelu",
        "Jak potłuczone lustro nauczyło się, że jego kawałki wciąż są piękne",
        "Przygoda ziarenka ryżu, które chciało nakarmić świat",
        "Wróżka zębuszka, która zgubiła swój magiczny pył",
        "Tajemnica rogu narwala, który spełniał życzenia",
        "Jak stary dąb i młody żołądź dzielili się mądrością",
        "Złodziej kolorów, który uczynił świat szarym i smutnym",
        "Mały płomyk, który bał się świecić z obawy, że zgaśnie",
        "Jak odcisk łapy na śniegu stał się mapą skarbów",
        "Tajemnica zamarzniętego jeziora, na którym tańczyły zorze polarne",
        "Mały groszek, który nie chciał być zupą, ale marzył o podróżach",
        "Legenda kolibra, który przyniósł ogień ludziom",
        "Jak deszczowy patyk nauczył się robić muzykę",
        "Dziecko, które każdej nocy sadziło gwiazdy w swoim ogrodzie",
        "Sekretny przepis na ciasteczka, które dawały skrzydła",
        "Podróż anielskiego piórka, które spadło z nieba",
        "Jak burczący brzuch stał się zabawną symfonią",
        "Mała wędrująca biblioteka, która podróżowała po wsiach",
        "Słowik, który nauczył ptaki śpiewać chórem",
        "Jak rondo stało się najweselszym miejscem na świecie",
        "Przygoda kabla elektrycznego, który chciał być girlandą",
        "Tajemnica strychu, na którym zapomniane zabawki ożywały",
        "Jak mała dziewczynka oswoiła swój cień i stała się odważna",
        "Magiczny lodziarz, który robił lody ze wspomnień",
        "Konstelacja, która się nudziła i zstąpiła na Ziemię",
        "Podróż mydlanej bańki, która chciała dotknąć słońca",
        "Jak muszelka przechowała szum oceanu przez tysiąc lat",
        "Kukułka z zegara, która chciała śpiewać coś innego niż godziny",
        "Potwór pod łóżkiem, który tak naprawdę bał się dzieci",
        "Jak magiczne okulary ukazały ukryte piękno świata",
        "Mała pszczółka, która uratowała ostatni kwiat na świecie",
        "Tajemnica porannej mgły, która skrywała równoległy świat",
        "Jak telefon bezprzewodowy przekazał najważniejsze słowo świata",
        "Przygoda kasztana, który rzucał kasztany jak wiadomości",
        "Pisklę, które bało się wyjść ze skorupki",
        "Jak pieg na nosie stał się mapą skarbów twarzy",
        "Legenda świetlików, które strzegą tajemnic lasu",
        "Mała choinka, która marzyła o tym, by być drzewkiem bożonarodzeniowym",
        "Jak słowo 'na zawsze' stało się najpiękniejszym słowem świata",
        "Podróż madlenki, która przenosiła wspomnienia z dzieciństwa",
        "Ptak, który zbudował gniazdo z nici marzeń",
        "Jak robaczek świętojański nauczył się, że jego wewnętrzne światło jest wyjątkowe",
        "Tajemnica porannej rosy, która orzeźwiała zmęczone serca",
        "Zaczarowana zupa babci, która leczyła wszystkie smutki",
        "Jak zwykła szyszka stała się najpiękniejszym drzewem",
        "Ścieżka z białych kamyków, która zawsze prowadziła do domu",
        "Przygoda miłego słowa, które wędrowało od ucha do ucha",
        "Koala, który chciał odkrywać świat bez opuszczania swojego drzewa",
        "Jak burza nauczyła się grzmieć łagodnie, by nie straszyć",
        "Mała syrenka, która wolała chodzić po lądzie niż pływać",
        "Tajemnica pierwszego śniegu, który ucisza wszystko i jest piękny",
        "Jak czerwony balonik odnalazł drogę z powrotem do nieba",
        "Podróż zapachu kwiatu przez pory roku",
        "Świecący grzyb, który oświetlał ścieżki w lesie",
        "Legenda tęczowego mostu, który łączył dwa światy",
        "Jak fala nauczyła się nie zalewać, ale pieścić brzeg",
        "Mały Czerwony Kapturek, który nie bał się wilka, ale ciemności",
        "Tajemnica pisanek, które nigdy nie zostały znalezione",
        "Chmurka w kształcie serca, która unosiła się nad miastem",
        "Jak zatrzymany zegarek wskazał najlepszy moment na miłość",
        "Podróż płatka róży na wiosennym wietrze",
        "Świerszcz, który grał na skrzypcach, by uśpić księżyc",
        "Jak sterta jesiennych liści stała się zamkiem pełnym wspomnień",
        "Mała kropla deszczu, która bała się spaść",
        "Tajemnica ostatniego jesiennego liścia, który nie chciał opaść",
        "Przygoda kawałka kredy, który rysował magiczne drzwi",
        "Jak patyk stał się najpiękniejszą czarodziejską różdżką świata",
        "Podróż rozgwiazdy, która chciała zobaczyć gwiazdy na niebie",
        "Jak węzeł na szaliku pomógł nie zapomnieć o najważniejszym",
        "Jeż, który szukał kogoś do przytulenia",
        "Tajemnica stogu siana, gdzie sny dojrzewały łagodnie",
        "Przygoda znaczka pocztowego, który okrążył cały świat",
        "Jak westchnienie ulgi stało się lekkim powiewem wiatru",
        "Małe pudełko sekretów, które zawierało najpiękniejsze wspomnienia",
        "Podróż nasionka mniszka lekarskiego niesionego letnim wiatrem",
        "Jak deszcz nauczył się padać w rytm muzyki",
        "Tajemnica drzwi, które pojawiały się tylko podczas pełni księżyca",
        "Okrągły kamyk, który potoczył się tak daleko, że ujrzał ocean",
        "Jak głęboki oddech ukoił cały gniew świata",
        "Podróż całusa wysłanego pocztą przez kontynenty",
        "Mała kałuża, która chciała stać się oceanem",
        "Tajemnica ciepłego piasku, który przechowywał ślady stóp",
        "Przygoda słomki, która chciała wyssać gwiazdy",
        "Jak puste pudełko nauczyło się, że może być wypełnione miłością",
        "Mały mól książkowy, który mieszkał między stronami książek",
        "Tajemnica kraciastego koca, który chronił przed koszmarami",
        "Przygoda kromki chleba, która chciała stać się złocistym tostem",
        "Jak drabina sznurowa pomogła sięgnąć najskrytszych marzeń",
        "Skarbonka, która zbierała nie pieniądze, ale uśmiechy",
        "Podróż magicznego słowa, które otwierało wszystkie drzwi",
        "Ptasie gniazdo utkane z nici czułości i źdźbeł cierpliwości",
        "Kałuża po deszczu, która odbijała cały wszechświat",
        "Skrzat, który nocą naprawiał zepsute zabawki",
        "Tajemnica słoika z dżemem, który przechowywał smak lata",
        "Przygoda kredki, która chciała narysować nieskończoność",
        "Jak garnek zupy ogrzał całą wioskę",
        "Podróż pestki jabłka, która stała się najpiękniejszym drzewem w sadzie",
        "Pocałunek na dobranoc, który podróżował do krainy snów",
        "Legenda łyżew, które tańczyły same pod księżycem",
        "Jak kraciasty kocyk pomógł przetrwać wszystkie burze",
        "Mała owieczka, która liczyła dzieci do snu",
        "Tajemnica budki lęgowej, do której ptaki składały swoje piosenki",
        "Przygoda kuli śniegowej, która zawierała całą zimę",
        "Jak szalik zrobiony z miłością ogrzał serce świata",
        "Zaczarowany flet, który roztańczył nawet kamienie",
        "Podróż kawałka kory, który przepłynął siedem mórz",
        "Płatek kwiatu, który posłużył zmęczonej biedronce za łóżko",
        "Jak lawendowe pole ukoiło wszystkie troski",
        "Mały teatr cieni, w którym cienie opowiadały historie",
        "Tajemnica wiecznej zabawy w chowanego między Słońcem a Księżycem",
        "Przygoda kociego wąsa, który stał się magicznym pędzlem",
        "Jak znoszony latający dywan odzyskał zdolność szybowania",
        "Przepis na spokój na dni wewnętrznej burzy",
        "Podróż dziecięcego śmiechu, który okrążył całą galaktykę",
    ]


def save_topics_to_file(topics, filename="topics.txt"):
    """Save topics to file."""
    with open(filename, "w", encoding="utf-8") as f:
        for topic in topics:
            f.write(f"{topic}\n")
    print(f"[topics] Zapisano {len(topics)} tematów do {filename}")


def check_and_update_topics():
    """Check topics.txt and add more if needed."""
    from pathlib import Path
    
    load_dotenv()
    
    topics_file = Path('topics.txt')
    
    if topics_file.exists():
        with open(topics_file, 'r', encoding='utf-8') as f:
            existing_topics = [line.strip() for line in f if line.strip()]
    else:
        existing_topics = []
    
    print(f"[topics] Current topics: {len(existing_topics)}")
    
    if len(existing_topics) < 50:
        print(f"[topics] Low on topics! Generating 100 more...")
        new_topics = generate_polish_kids_topics(100)
        with open(topics_file, 'a', encoding='utf-8') as f:
            for topic in new_topics:
                f.write(f"{topic}\n")
        print(f"[topics] Added {len(new_topics)} new topics!")
        print(f"[topics] Total topics now: {len(existing_topics) + len(new_topics)}")
    else:
        print(f"[topics] Enough topics available ({len(existing_topics)})")


def main():
    """Generate and save beautiful Polish kids story topics."""
    print("=" * 60)
    print("=== Generator Pięknych Polskich Bajek dla Dzieci ===")
    print("=" * 60)
    
    try:
        with open("topics.txt", "r", encoding="utf-8") as f:
            existing_topics = [line.strip() for line in f if line.strip()]
        
        if len(existing_topics) >= 50:
            print(f"[topics] Znaleziono {len(existing_topics)} tematów. Nie trzeba generować nowych.")
            return
        else:
            print(f"[topics] Znaleziono tylko {len(existing_topics)} tematów. Generowanie nowych...")
    except FileNotFoundError:
        print("[topics] Plik topics.txt nie istnieje. Generowanie nowych tematów...")
        existing_topics = []
    
    num_to_generate = 100
    new_topics = generate_polish_kids_topics(num_to_generate)
    
    all_topics = existing_topics + new_topics
    unique_topics = []
    seen = set()
    for topic in all_topics:
        if topic.lower() not in seen:
            unique_topics.append(topic)
            seen.add(topic.lower())
    
    save_topics_to_file(unique_topics)
    
    print("=" * 60)
    print(f"✅ Wygenerowano {len(unique_topics)} unikalnych i pięknych tematów!")
    print("=" * 60)


if __name__ == '__main__':
    check_and_update_topics()
