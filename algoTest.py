import json
import re
import unicodedata
from pathlib import Path

import ftfy
import pdfplumber
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent


class AlgoTest:
    SPECIAL_WORDS = ["&"]

    SMALL_LINE_MAX_WORDS = 5
    CHILD_COLUMN_SPLIT_OFFSET_X = 100
    HEADER_REPLACE_OFFSET_X = 100
    WORD_LINE_TOLERANCE = 3.0

    EXPERIENCE_MIN_DESCRIPTION_ITEMS = 3

    YEARS = [str(year) for year in range(1950, datetime.now().year + 1)]

    SECTION_HEADERS = {
        "informations_personnelles": {
            "oneWord": [
                "coordonnees", "Coordonnees", "COORDONNEES",
                "coordonnÃ©es", "CoordonnÃ©es", "COORDONNÃ‰ES",
                "contact", "Contact", "CONTACT",
                "profil", "Profil", "PROFIL",
            ],
            "aLotOfWords": [
                "informations personnelles", "Informations Personnelles", "INFORMATIONS PERSONNELLES",
                "information personnelle", "Information Personnelle", "INFORMATION PERSONNELLE",
                "personal information", "Personal Information", "PERSONAL INFORMATION",
                "about me", "About Me", "ABOUT ME",
            ],
        },
        "competences": {
            "oneWord": [
                "competences", "Competences", "COMPETENCES",
                "compÃ©tences", "CompÃ©tences", "COMPÃ‰TENCES",
                "competence", "Competence", "COMPETENCE",
                "compÃ©tence", "CompÃ©tence", "COMPÃ‰TENCE",
                "skills", "Skills", "SKILLS",
                "expertise", "Expertise", "EXPERTISE",
                "technologies", "Technologies", "TECHNOLOGIES",
            ],
            "aLotOfWords": [
                "competences techniques", "Competences Techniques", "COMPETENCES TECHNIQUES",
                "compÃ©tences techniques", "CompÃ©tences Techniques", "COMPÃ‰TENCES TECHNIQUES",
                "competences fonctionnelles", "Competences Fonctionnelles", "COMPETENCES FONCTIONNELLES",
                "technical skills", "Technical Skills", "TECHNICAL SKILLS",
            ],
        },
        "langues": {
            "oneWord": [
                "langues", "Langues", "LANGUES",
                "langue", "Langue", "LANGUE",
                "languages", "Languages", "LANGUAGES",
            ],
            "aLotOfWords": [
                "language skills", "Language Skills", "LANGUAGE SKILLS",
            ],
        },
        "formation": {
            "oneWord": [
                "formation", "Formation", "FORMATION",
                "formations", "Formations", "FORMATIONS",
                "education", "Education", "EDUCATION",
                "Ã©ducation", "Ã‰ducation", "Ã‰DUCATION",
                "diplomes", "Diplomes", "DIPLOMES",
                "diplÃ´mes", "DiplÃ´mes", "DIPLÃ”MES",
                "etudes", "Etudes", "ETUDES",
                "Ã©tudes", "Ã‰tudes", "Ã‰TUDES",
                "cursus", "Cursus", "CURSUS",
            ],
            "aLotOfWords": [
                "formations & certifications", "Formations & Certifications", "FORMATIONS & CERTIFICATIONS",
            ],
        },
        "experience": {
            "oneWord": [
                "experience", "Experience", "EXPERIENCE",
                "expÃ©rience", "ExpÃ©rience", "EXPÃ‰RIENCE",
                "experiences", "Experiences", "EXPERIENCES",
                "expÃ©riences", "ExpÃ©riences", "EXPÃ‰RIENCES",
            ],
            "aLotOfWords": [
                "experiences professionnelles", "Experiences Professionnelles", "EXPERIENCES PROFESSIONNELLES",
                "expÃ©riences professionnelles", "ExpÃ©riences Professionnelles", "EXPÃ‰RIENCES PROFESSIONNELLES",
                "experience professionnelle", "Experience Professionnelle", "EXPERIENCE PROFESSIONNELLE",
                "expÃ©rience professionnelle", "ExpÃ©rience Professionnelle", "EXPÃ‰RIENCE PROFESSIONNELLE",
                "detail des experiences professionnelles", "Detail Des Experiences Professionnelles",
                "DETAIL DES EXPERIENCES PROFESSIONNELLES",
                "dÃ©tail des expÃ©riences professionnelles", "DÃ©tail Des ExpÃ©riences Professionnelles",
                "DÃ‰TAIL DES EXPÃ‰RIENCES PROFESSIONNELLES",
                "work experience", "Work Experience", "WORK EXPERIENCE",
                "professional experience", "Professional Experience", "PROFESSIONAL EXPERIENCE",
                "parcours professionnel", "Parcours Professionnel", "PARCOURS PROFESSIONNEL",
            ],
        },
        "projets": {
            "oneWord": [
                "projets", "Projets", "PROJETS",
                "projet", "Projet", "PROJET",
                "projects", "Projects", "PROJECTS",
                "project", "Project", "PROJECT",
                "realisations", "Realisations", "REALISATIONS",
                "rÃ©alisations", "RÃ©alisations", "RÃ‰ALISATIONS",
                "portfolio", "Portfolio", "PORTFOLIO",
            ],
            "aLotOfWords": [],
        },
        "centres_interet": {
            "oneWord": [
                "loisirs", "Loisirs", "LOISIRS",
                "hobbies", "Hobbies", "HOBBIES",
                "interets", "Interets", "INTERETS",
                "intÃ©rÃªts", "IntÃ©rÃªts", "INTÃ‰RÃŠTS",
                "interests", "Interests", "INTERESTS",
            ],
            "aLotOfWords": [
                "centres d'interet", "Centres D'Interet", "CENTRES D'INTERET",
                "centres dâ€™intÃ©rÃªt", "Centres Dâ€™intÃ©rÃªt", "CENTRES Dâ€™INTÃ‰RÃŠT",
                "centre d'interet", "Centre D'Interet", "CENTRE D'INTERET",
                "centre dâ€™intÃ©rÃªt", "Centre Dâ€™intÃ©rÃªt", "CENTRE Dâ€™INTÃ‰RÃŠT",
            ],
        },
        "certifications": {
            "oneWord": [
                "certifications", "Certifications", "CERTIFICATIONS",
                "certification", "Certification", "CERTIFICATION",
                "certificats", "Certificats", "CERTIFICATS",
                "certificat", "Certificat", "CERTIFICAT",
                "certificates", "Certificates", "CERTIFICATES",
            ],
            "aLotOfWords": [],
        },
    }

    MONTH_NAMES = [
        "janvier", "Janvier", "JANVIER",
        "jan", "Jan", "JAN",

        "février", "Février", "FÉVRIER",
        "fevrier", "Fevrier", "FEVRIER",
        "fév", "Fév", "FÉV",
        "fev", "Fev", "FEV",

        "mars", "Mars", "MARS",
        "mar", "Mar", "MAR",

        "avril", "Avril", "AVRIL",
        "avr", "Avr", "AVR",

        "mai", "Mai", "MAI",

        "juin", "Juin", "JUIN",
        "jun", "Jun", "JUN",

        "juillet", "Juillet", "JUILLET",
        "juil", "Juil", "JUIL",
        "jul", "Jul", "JUL",

        "août", "Août", "AOÛT",
        "aout", "Aout", "AOUT",
        "aoû", "Aoû", "AOÛ",

        "septembre", "Septembre", "SEPTEMBRE",
        "sep", "Sep", "SEP",
        "sept", "Sept", "SEPT",

        "octobre", "Octobre", "OCTOBRE",
        "oct", "Oct", "OCT",

        "novembre", "Novembre", "NOVEMBRE",
        "nov", "Nov", "NOV",

        "décembre", "Décembre", "DÉCEMBRE",
        "decembre", "Decembre", "DECEMBRE",
        "déc", "Déc", "DÉC",
        "dec", "Dec", "DEC",
    ]
    COUNTRY_NAMES = [
        "tunisie", "Tunisie", "TUNISIE",
        "tunis", "Tunis", "TUNIS",

        "france", "France", "FRANCE",
        "allemagne", "Allemagne", "ALLEMAGNE",
        "italie", "Italie", "ITALIE",
        "espagne", "Espagne", "ESPAGNE",
        "portugal", "Portugal", "PORTUGAL",
        "belgique", "Belgique", "BELGIQUE",
        "suisse", "Suisse", "SUISSE",
        "luxembourg", "Luxembourg", "LUXEMBOURG",
        "pays-bas", "Pays-Bas", "PAYS-BAS",
        "hollande", "Hollande", "HOLLANDE",

        "royaume-uni", "Royaume-Uni", "ROYAUME-UNI",
        "angleterre", "Angleterre", "ANGLETERRE",
        "écosse", "Écosse", "ÉCOSSE",
        "ecosse", "Ecosse", "ECOSSE",
        "irlande", "Irlande", "IRLANDE",

        "maroc", "Maroc", "MAROC",
        "algérie", "Algérie", "ALGÉRIE",
        "algerie", "Algerie", "ALGERIE",
        "libye", "Libye", "LIBYE",
        "égypte", "Égypte", "ÉGYPTE",
        "egypte", "Egypte", "EGYPTE",

        "canada", "Canada", "CANADA",
        "états-unis", "États-Unis", "ÉTATS-UNIS",
        "etats-unis", "Etats-Unis", "ETATS-UNIS",
        "usa", "Usa", "USA",

        "chine", "Chine", "CHINE",
        "japon", "Japon", "JAPON",
        "inde", "Inde", "INDE",
        "turquie", "Turquie", "TURQUIE",
        "émirats arabes unis", "Émirats Arabes Unis", "ÉMIRATS ARABES UNIS",
        "emirats arabes unis", "Emirats Arabes Unis", "EMIRATS ARABES UNIS",
        "arabie saoudite", "Arabie Saoudite", "ARABIE SAOUDITE",
    ]
    SECTION_CHILD_OUTPUT_FIELDS = {
        "competences": {
            "root_text": "nomCOMPETENCES",
            "child_text": "descriptionCOMPETENCES",
            "fields": [
                "nomCOMPETENCES",
                "descriptionCOMPETENCES",
            ],
        },

        "experience": {
            "root_text": "nomPoste",
            "child_text": "descriptionPoste",
            "fields": [
                "nomPoste",
                "datePoste",
                "lieuPost",
                "paysPoste",
                "descriptionPoste",
            ],
        },

        "formation": {
            "root_text": "nomFormations",
            "child_text": "descriptionFormation",
            "fields": [
                "nomFormations",
                "LieuFormations",
                "DateFormation",
                "descriptionFormation",
            ],
        },

        "centres_interet": {
            "root_text": "nomCentreInteret",
            "child_text": "descriptionCentreInteret",
            "fields": [
                "nomCentreInteret",
                "descriptionCentreInteret",
            ],
        },

        "langues": {
            "root_text": "nomLangue",
            "child_text": "DescriptionLangue",
            "fields": [
                "nomLangue",
                "DescriptionLangue",
            ],
        },
    }

    DATE_CONTEXT_WORDS = [
        "depuis", "Depuis", "DEPUIS",
        "de", "De", "DE",
        "à", "À",
        "a", "A",
        "au", "Au", "AU",
        "du", "Du", "DU",
        "jusqu'à", "Jusqu'à", "JUSQU'À",
        "jusqua", "Jusqua", "JUSQUA",
        "présent", "Présent", "PRÉSENT",
        "present", "Present", "PRESENT",
        "actuel", "Actuel", "ACTUEL",
        "actuelle", "Actuelle", "ACTUELLE",
        "aujourd'hui", "Aujourd'hui", "AUJOURD'HUI",
        "aujourd hui", "Aujourd Hui", "AUJOURD HUI",
    ]


    DESCRIPTION_ITEM_START_PATTERNS = [
        "-",
        "*",
        "â€¢",
        "â€“",
        "â€”",
    ]

    LANGUAGE_NAMES = [
        "anglais", "Anglais", "ANGLAIS",
        "ang", "Ang", "ANG",

        "français", "Français", "FRANÇAIS",
        "francais", "Francais", "FRANCAIS",
        "fr", "Fr", "FR",

        "arabe", "Arabe", "ARABE",
        "ar", "Ar", "AR",
    ]
    MERGE_SAME_STYLE_TITLE_LINES = True
    MERGE_SAME_STYLE_TITLE_SEPARATOR = " "

    def writeResultatJson(self, resultat: dict) -> int:
        try:
            output_path = BASE_DIR / "resultat.json"
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(resultat, file, ensure_ascii=False, indent=4)
            return 1
        except Exception:
            return 0

    def ReadFilePDF(self, PdfName: str) -> int:
        try:
            pdf_path = BASE_DIR / PdfName
            if not pdf_path.exists():
                return 0

            with pdfplumber.open(str(pdf_path)) as pdf:
                if len(pdf.pages) == 0:
                    return 0

            return 1
        except Exception:
            return 0

    def hedhiFixPdfFileLPointO(self, PdfName: str) -> dict:
        try:
            pdf_path = BASE_DIR / PdfName

            if self.ReadFilePDF(PdfName) == 0:
                return {
                    "success": False,
                    "error": "PDF_READ_ERROR",
                    "message": f"Cannot read PDF file: {pdf_path}",
                    "pdf_file": str(pdf_path),
                    "pages": [],
                }

            pages = []

            with pdfplumber.open(str(pdf_path)) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    width = float(page.width)
                    height = float(page.height)

                    pages.append({
                        "page": page_number,
                        "width": round(width, 2),
                        "height": round(height, 2),
                        "origin": {
                            "name": "O",
                            "x": 0.0,
                            "y": 0.0,
                            "old_x": round(width / 2, 2),
                            "old_y": round(height / 2, 2),
                        },
                        "rectangle": {
                            "left": round(-width / 2, 2),
                            "right": round(width / 2, 2),
                            "top": round(height / 2, 2),
                            "bottom": round(-height / 2, 2),
                        },
                    })

            return {
                "success": True,
                "error": None,
                "message": "PDF read successfully and point O fixed",
                "pdf_file": str(pdf_path),
                "coordinate_system": "center_origin",
                "unit": "PDF point",
                "pages": pages,
            }

        except Exception as e:
            return {
                "success": False,
                "error": type(e).__name__,
                "message": str(e),
                "pdf_file": PdfName,
                "pages": [],
            }

    def _center_pdf_point(self, x: float, y: float, page_width: float, page_height: float) -> tuple[float, float]:
        new_x = x - page_width / 2
        new_y = page_height / 2 - y
        return round(new_x, 2), round(new_y, 2)

    def _fix_text(self, text: str) -> str:
        text = text or ""
        return ftfy.fix_text(text)

    def _normalize_text(self, text: str) -> str:
        text = self._fix_text(text).strip()

        if text in self.SPECIAL_WORDS:
            return text

        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        text = text.lower().strip()

        return re.sub(r"[^a-z0-9]+", "", text)

    def _split_phrase_to_parts(self, text: str) -> list[str]:
        text = self._fix_text(text)

        for special_word in self.SPECIAL_WORDS:
            text = text.replace(special_word, f" {special_word} ")

        return text.split()

    def _normalize_phrase_to_words(self, text: str) -> list[str]:
        words = []

        for part in self._split_phrase_to_parts(text):
            clean = self._normalize_text(part)
            if clean:
                words.append(clean)

        return words

    def _word_color(self, word: dict):
        return word.get("non_stroking_color") or word.get("stroking_color") or None

    def _word_size(self, word: dict) -> float:
        return round(float(word.get("size", 0)), 2)

    def _is_bold_font(self, fontname: str | None) -> bool:
        fontname = (fontname or "").lower()
        return "bold" in fontname or "black" in fontname or "semibold" in fontname

    def _style_signature(self, word: dict) -> tuple:
        return (
            self._word_size(word),
            str(self._word_color(word)),
            str(word.get("fontname")),
            self._is_bold_font(word.get("fontname")),
            str(word.get("adv")),
            str(word.get("upright")),
        )

    def _same_style(self, word1: dict, word2: dict) -> bool:
        return self._style_signature(word1) == self._style_signature(word2)

    def _group_words_by_line(self, words: list[dict], tolerance: float = 3.0) -> list[list[dict]]:
        lines = []
        sorted_words = sorted(words, key=lambda word: (float(word["top"]), float(word["x0"])))

        for word in sorted_words:
            added = False
            word_top = float(word["top"])

            for line in lines:
                line_top = float(line[0]["top"])
                if abs(word_top - line_top) <= tolerance:
                    line.append(word)
                    added = True
                    break

            if not added:
                lines.append([word])

        for line in lines:
            line.sort(key=lambda word: float(word["x0"]))

        return lines

    def _build_header_indexes(self, section_headers: dict) -> dict:
        indexes = {}

        for section_name, data in section_headers.items():
            one_words = set()
            multi_words = []

            for header in data.get("oneWord", []):
                parts = self._normalize_phrase_to_words(header)
                if len(parts) == 1:
                    one_words.add(parts[0])

            for header in data.get("aLotOfWords", []):
                parts = self._normalize_phrase_to_words(header)
                if len(parts) > 1:
                    multi_words.append({
                        "header": self._fix_text(header),
                        "parts": parts,
                    })

            indexes[section_name] = {
                "oneWord": one_words,
                "aLotOfWords": multi_words,
            }

        return indexes

    def _find_one_word_candidate(self, word: dict, header_indexes: dict) -> dict | None:
        word_text = self._normalize_text(word.get("text", ""))

        for section_name, data in header_indexes.items():
            if word_text in data["oneWord"]:
                return {
                    "section": section_name,
                    "header_type": "oneWord",
                    "header": self._fix_text(word.get("text", "")),
                    "parts": [word_text],
                }

        return None

    def _find_multi_word_candidate_at(self, line_words: list[dict], index: int, header_indexes: dict) -> dict | None:
        line_norm_words = [
            self._normalize_text(word.get("text", ""))
            for word in line_words
        ]

        for section_name, data in header_indexes.items():
            for header_data in data["aLotOfWords"]:
                parts = header_data["parts"]
                end_index = index + len(parts)

                if end_index > len(line_words):
                    continue

                current_parts = line_norm_words[index:end_index]

                if current_parts == parts:
                    return {
                        "section": section_name,
                        "header_type": "aLotOfWords",
                        "header": header_data["header"],
                        "parts": parts,
                    }

        return None

    def _find_candidate_at(self, line_words: list[dict], index: int, header_indexes: dict) -> dict | None:
        multi_word_candidate = self._find_multi_word_candidate_at(line_words, index, header_indexes)

        if multi_word_candidate:
            multi_word_candidate["start_index"] = index
            multi_word_candidate["end_index"] = index + len(multi_word_candidate["parts"])
            return multi_word_candidate

        one_word_candidate = self._find_one_word_candidate(line_words[index], header_indexes)

        if one_word_candidate:
            one_word_candidate["start_index"] = index
            one_word_candidate["end_index"] = index + 1
            return one_word_candidate

        return None

    def _find_raw_candidates_in_line(self, line_words: list[dict], header_indexes: dict) -> list[dict]:
        candidates = []
        index = 0

        while index < len(line_words):
            candidate = self._find_candidate_at(line_words, index, header_indexes)

            if candidate:
                candidates.append(candidate)
                index = candidate["end_index"]
            else:
                index += 1

        return candidates

    def _candidate_words(self, line_words: list[dict], candidate: dict) -> list[dict]:
        return line_words[candidate["start_index"]:candidate["end_index"]]

    def _candidate_indexes(self, candidate: dict) -> set[int]:
        return set(range(candidate["start_index"], candidate["end_index"]))

    def _candidate_text(self, line_words: list[dict], candidate: dict) -> str:
        words = self._candidate_words(line_words, candidate)
        return " ".join(self._fix_text(word.get("text", "")) for word in words)

    def _candidate_box(self, line_words: list[dict], candidate: dict) -> dict:
        words = self._candidate_words(line_words, candidate)

        x0 = min(float(word["x0"]) for word in words)
        x1 = max(float(word["x1"]) for word in words)
        top = min(float(word["top"]) for word in words)
        bottom = max(float(word["bottom"]) for word in words)

        return {
            "x0": x0,
            "x1": x1,
            "top": top,
            "bottom": bottom,
            "x": (x0 + x1) / 2,
            "y": (top + bottom) / 2,
        }

    def _candidate_has_one_style(self, line_words: list[dict], candidate: dict) -> bool:
        words = self._candidate_words(line_words, candidate)

        if not words:
            return False

        first_style = self._style_signature(words[0])

        for word in words[1:]:
            if self._style_signature(word) != first_style:
                return False

        return True

    def _candidate_differs_from_words(self, line_words: list[dict], candidate: dict, normal_words: list[dict]) -> bool:
        candidate_words = self._candidate_words(line_words, candidate)

        for candidate_word in candidate_words:
            for normal_word in normal_words:
                if self._same_style(candidate_word, normal_word):
                    return False

        return True

    def _line_has_same_style_as_candidate(self, line_words: list[dict], candidate: dict) -> bool:
        candidate_words = self._candidate_words(line_words, candidate)

        if not candidate_words:
            return False

        candidate_style = self._style_signature(candidate_words[0])

        for word in line_words:
            if self._style_signature(word) != candidate_style:
                return False

        return True

    def _candidate_passes_style_conditions(
            self,
            line_words: list[dict],
            candidate: dict,
            normal_words_in_line: list[dict],
            raw_candidates_count: int,
    ) -> bool:
        if not self._candidate_has_one_style(line_words, candidate):
            return False

        if self._candidate_differs_from_words(line_words, candidate, normal_words_in_line):
            return True

        if raw_candidates_count >= 2 and len(line_words) <= self.SMALL_LINE_MAX_WORDS:
            return self._line_has_same_style_as_candidate(line_words, candidate)

        return False

    def _build_detected_item(
            self,
            line_words: list[dict],
            candidate: dict,
            page_number: int,
            line_number: int,
            page_width: float,
            page_height: float,
            normal_words_in_line: list[dict],
    ) -> dict:
        box = self._candidate_box(line_words, candidate)

        fixed_x, fixed_y = self._center_pdf_point(box["x"], box["y"], page_width, page_height)
        fixed_x0, fixed_top = self._center_pdf_point(box["x0"], box["top"], page_width, page_height)
        fixed_x1, fixed_bottom = self._center_pdf_point(box["x1"], box["bottom"], page_width, page_height)

        first_word = self._candidate_words(line_words, candidate)[0]

        return {
            "section": candidate["section"],
            "header_type": candidate["header_type"],
            "header": candidate["header"],
            "CLWord": self._candidate_text(line_words, candidate),

            "page": page_number,
            "line_number": line_number,
            "line_text": " ".join(self._fix_text(word.get("text", "")) for word in line_words),

            "x": fixed_x,
            "y": fixed_y,
            "x0": fixed_x0,
            "x1": fixed_x1,
            "top": fixed_top,
            "bottom": fixed_bottom,

            "font_size": self._word_size(first_word),
            "fontname": first_word.get("fontname"),
            "color": self._word_color(first_word),

            "normal_words_in_line_checked": [
                {
                    "word": self._fix_text(word.get("text", "")),
                    "font_size": self._word_size(word),
                    "color": self._word_color(word),
                }
                for word in normal_words_in_line
            ],
        }

    def hedhiTrajaaliCoorAsemiCle(self, x1: dict, x2: dict) -> list:
        try:
            if not x1:
                return []

            if not x1.get("success"):
                return []

            if not x2:
                return []

            pdf_file = x1.get("pdf_file")
            if not pdf_file:
                return []

            pdf_path = Path(pdf_file)
            if not pdf_path.exists():
                return []

            pages_info = {
                page["page"]: page
                for page in x1.get("pages", [])
            }

            header_indexes = self._build_header_indexes(x2)
            resultat = []

            with pdfplumber.open(str(pdf_path)) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_info = pages_info.get(page_number)

                    if not page_info:
                        continue

                    page_width = float(page_info["width"])
                    page_height = float(page_info["height"])

                    words = page.extract_words(
                        extra_attrs=[
                            "size",
                            "fontname",
                            "non_stroking_color",
                            "stroking_color",
                        ]
                    )

                    lines = self._group_words_by_line(words, self.WORD_LINE_TOLERANCE)

                    for line_number, line_words in enumerate(lines, start=1):
                        raw_candidates = self._find_raw_candidates_in_line(line_words, header_indexes)

                        raw_candidate_indexes = set()
                        for candidate in raw_candidates:
                            raw_candidate_indexes.update(self._candidate_indexes(candidate))

                        accepted_indexes = set()

                        for candidate in raw_candidates:
                            candidate_indexes = self._candidate_indexes(candidate)

                            if candidate_indexes & accepted_indexes:
                                continue

                            normal_words_in_line = [
                                word
                                for index, word in enumerate(line_words)
                                if index not in raw_candidate_indexes
                            ]

                            if not self._candidate_passes_style_conditions(
                                    line_words,
                                    candidate,
                                    normal_words_in_line,
                                    len(raw_candidates),
                            ):
                                continue

                            detected = self._build_detected_item(
                                line_words,
                                candidate,
                                page_number,
                                line_number,
                                page_width,
                                page_height,
                                normal_words_in_line,
                            )

                            resultat.append(detected)
                            accepted_indexes.update(candidate_indexes)

            return resultat

        except Exception:
            return []

    def _convert_line_words_to_center_words(
            self,
            line_words: list[dict],
            page_number: int,
            line_number: int,
            page_width: float,
            page_height: float,
    ) -> list[dict]:
        children = []

        for word in line_words:
            x0 = float(word["x0"])
            x1 = float(word["x1"])
            top = float(word["top"])
            bottom = float(word["bottom"])

            center_x = (x0 + x1) / 2
            center_y = (top + bottom) / 2

            fixed_x, fixed_y = self._center_pdf_point(center_x, center_y, page_width, page_height)
            fixed_x0, fixed_top = self._center_pdf_point(x0, top, page_width, page_height)
            fixed_x1, fixed_bottom = self._center_pdf_point(x1, bottom, page_width, page_height)

            children.append({
                "text": self._fix_text(word.get("text", "")),
                "page": page_number,
                "line_number": line_number,
                "x": fixed_x,
                "y": fixed_y,
                "x0": fixed_x0,
                "x1": fixed_x1,
                "top": fixed_top,
                "bottom": fixed_bottom,
                "font_size": self._word_size(word),
                "fontname": word.get("fontname"),
                "color": self._word_color(word),
            })

        return children









    def _same_line_words_after_header(
            self,
            line_children: list[dict],
            header: dict,
            next_header: dict | None = None,
    ) -> list[dict]:
        left_limit = header["x1"]
        right_limit = next_header["x0"] if next_header else None

        result = []

        for word in line_children:
            if word["x0"] <= left_limit:
                continue

            if right_limit is not None and word["x1"] >= right_limit:
                continue

            result.append(word)

        return result
















    def _find_owner_section_by_x(self, word_x: float, active_sections: list[dict]) -> dict:
        active_sections = sorted(active_sections, key=lambda section: section["x"])

        if len(active_sections) == 1:
            return active_sections[0]

        for index, section in enumerate(active_sections):
            if index == 0:
                next_section = active_sections[index + 1]
                right_limit = next_section["x"] - self.CHILD_COLUMN_SPLIT_OFFSET_X

                if word_x < right_limit:
                    return section

            elif index == len(active_sections) - 1:
                left_limit = section["x"] - self.CHILD_COLUMN_SPLIT_OFFSET_X

                if word_x >= left_limit:
                    return section

            else:
                left_limit = section["x"] - self.CHILD_COLUMN_SPLIT_OFFSET_X
                next_section = active_sections[index + 1]
                right_limit = next_section["x"] - self.CHILD_COLUMN_SPLIT_OFFSET_X

                if left_limit <= word_x < right_limit:
                    return section

        return active_sections[-1]

    def _make_section_node_from_header(self, header: dict) -> dict:
        return {
            "section": header["section"],
            "header": header["header"],
            "CLWord": header["CLWord"],
            "page": header["page"],
            "line_number": header["line_number"],
            "x": header["x"],
            "y": header["y"],
            "x0": header["x0"],
            "x1": header["x1"],
            "top": header["top"],
            "bottom": header["bottom"],
            "children": [],
        }

    def _last_child_x_range(self, section: dict) -> tuple[float, float] | None:
        children = section.get("children", [])

        if not children:
            return None

        last_child = children[-1]
        words = last_child.get("_words", [])

        if not words:
            return None

        x_values = [word["x"] for word in words]

        return min(x_values), max(x_values)

    def _find_section_by_last_child_range(self, active_sections: list[dict], header_x: float) -> dict | None:
        for section in active_sections:
            x_range = self._last_child_x_range(section)

            if not x_range:
                continue

            x_left, x_right = x_range

            x_left = x_left - self.HEADER_REPLACE_OFFSET_X
            x_right = x_right - self.HEADER_REPLACE_OFFSET_X

            if x_left <= header_x <= x_right:
                return section

        return None

    def _replace_section_object(self, active_sections: list[dict], old_section: dict, new_section: dict) -> list[dict]:
        updated = []

        for section in active_sections:
            if section is old_section:
                updated.append(new_section)
            else:
                updated.append(section)

        return sorted(updated, key=lambda section: section["x"])

    def _add_or_replace_by_last_child_range(self, active_sections: list[dict], new_section: dict) -> list[dict]:
        if not active_sections:
            return [new_section]

        old_section = self._find_section_by_last_child_range(
            active_sections,
            new_section["x"],
        )

        if old_section:
            return self._replace_section_object(
                active_sections,
                old_section,
                new_section,
            )

        active_sections.append(new_section)

        return sorted(active_sections, key=lambda section: section["x"])

    def _child_word_style_signature(self, word: dict) -> tuple:
        return (
            round(float(word.get("font_size", 0)), 2),
            str(word.get("color")),
            str(word.get("fontname")),
            self._is_bold_font(word.get("fontname")),
        )

    def _child_line_style_signature(self, words: list[dict]) -> tuple | None:
        if not words:
            return None

        first_word = words[0]
        return self._child_word_style_signature(first_word)

    def _build_child_line(self, words: list[dict]) -> dict | None:
        if not words:
            return None

        words = sorted(words, key=lambda word: word["x0"])
        text = " ".join(word["text"] for word in words).strip()

        return {
            "text": text,
            "_words": words,
            "_style": self._child_line_style_signature(words),
        }

    def _clean_children_to_text_only(self, sections: list[dict]) -> list[dict]:
        for section in sections:
            clean_children = []

            for child in section.get("children", []):
                if isinstance(child, dict):
                    clean_children.append(child.get("text", ""))
                elif isinstance(child, str):
                    clean_children.append(child)

            section["children"] = clean_children

        return sections

    def _make_tree_child_node(self, child: dict) -> dict:
        return {
            "valeur": child.get("text", ""),
            "children": [],
            "_style": child.get("_style"),
        }













    def _empty_section_child_output(self, section_name: str) -> dict:
        config = self.SECTION_CHILD_OUTPUT_FIELDS.get(section_name)

        if not config:
            return {
                "valeur": "",
            }

        output = {
            field_name: ""
            for field_name in config["fields"]
        }

        description_field = config["child_text"]
        output[description_field] = []

        return output


















    def _text_contains_keyword_from_list(self, text: str, keywords: list[str]) -> bool:
        text_words = self._normalize_phrase_to_words(text)

        if not text_words:
            return False

        for keyword in keywords:
            keyword_words = self._normalize_phrase_to_words(keyword)

            if not keyword_words:
                continue

            if len(keyword_words) == 1:
                if keyword_words[0] in text_words:
                    return True

                continue

            for index in range(0, len(text_words) - len(keyword_words) + 1):
                if text_words[index:index + len(keyword_words)] == keyword_words:
                    return True

        return False























    def _get_description_field_name(self, section_name: str) -> str:
        config = self.SECTION_CHILD_OUTPUT_FIELDS.get(section_name)

        if not config:
            return "valeur"

        return config["child_text"]







    def _is_date_context_word(self, text: str) -> bool:
        text_norm = self._normalize_text(text)

        for word in self.DATE_CONTEXT_WORDS:
            if text_norm == self._normalize_text(word):
                return True

        return False








    def _is_date_word(self, text: str) -> bool:
        text_norm = self._normalize_text(text)

        if text_norm in [self._normalize_text(year) for year in self.YEARS]:
            return True

        for month in self.MONTH_NAMES:
            if text_norm == self._normalize_text(month):
                return True

        return False


    def _extract_date_part_from_text(self, text: str) -> str:
        parts = self._split_phrase_to_parts(text)

        if not parts:
            return ""

        first_date_index = None
        last_date_index = None

        for index, part in enumerate(parts):
            if self._is_date_word(part):
                if first_date_index is None:
                    first_date_index = index

                last_date_index = index

        if first_date_index is None or last_date_index is None:
            return ""

        while first_date_index > 0 and self._is_date_context_word(parts[first_date_index - 1]):
            first_date_index -= 1

        while last_date_index + 1 < len(parts) and self._is_date_context_word(parts[last_date_index + 1]):
            last_date_index += 1

        return " ".join(
            self._fix_text(part)
            for part in parts[first_date_index:last_date_index + 1]
        ).strip()










    def _is_country_word(self, text: str) -> bool:
        text_norm = self._normalize_text(text)

        for country in self.COUNTRY_NAMES:
            if text_norm == self._normalize_text(country):
                return True

        return False


    def _extract_words_by_checker(self, text: str, checker) -> tuple[str, str]:
        parts = self._split_phrase_to_parts(text)

        if not parts:
            return "", ""

        selected_parts = []
        rest_parts = []

        for part in parts:
            fixed_part = self._fix_text(part)

            if checker(part):
                selected_parts.append(fixed_part)
            else:
                rest_parts.append(fixed_part)

        selected_text = " ".join(selected_parts).strip()
        rest_text = " ".join(rest_parts).strip()

        return selected_text, rest_text


    def _remove_date_part_from_text(self, text: str) -> str:
        date_part = self._extract_date_part_from_text(text)

        if not date_part:
            return text

        return self._fix_text(text).replace(date_part, "").strip()


    def _clean_lieu_poste_text(self, text: str) -> str:
        text = self._fix_text(text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"^[\s\-–—|,/]+", "", text)
        text = re.sub(r"[\s\-–—|,/]+$", "", text)
        text = re.sub(r"\s+([\-–—|,/])", r" \1", text)
        return text.strip()













    def _detect_specific_output_fields(self, section_name: str, text: str) -> dict:
        detected = {}

        has_date = (
                self._text_contains_keyword_from_list(text, self.YEARS)
                or self._text_contains_keyword_from_list(text, self.MONTH_NAMES)
        )

        has_country = self._text_contains_keyword_from_list(text, self.COUNTRY_NAMES)

        if section_name == "experience":
            rest_text = text

            if has_date:
                date_part = self._extract_date_part_from_text(rest_text)

                if date_part:
                    detected["datePoste"] = date_part
                    rest_text = self._remove_date_part_from_text(rest_text)

            if has_country:
                country_part, rest_text = self._extract_words_by_checker(
                    rest_text,
                    self._is_country_word,
                )

                if country_part:
                    detected["paysPoste"] = country_part

            nom_poste = self._clean_lieu_poste_text(rest_text)

            if nom_poste:
                detected["nomPoste"] = nom_poste

        elif section_name == "formation":
            if has_date:
                detected["DateFormation"] = text

            if has_country:
                detected["LieuFormations"] = text

        return detected



















    def _first_real_char(self, text: str) -> str:
        text = self._fix_text(text).strip()

        if not text:
            return ""

        return text[0]


    def _description_item_start_key(self, text: str) -> str:
        text = self._fix_text(text).strip()

        if not text:
            return ""

        for pattern in self.DESCRIPTION_ITEM_START_PATTERNS:
            if text.startswith(pattern):
                return pattern

        first_char = self._first_real_char(text)

        if first_char and first_char.isalpha() and first_char.isupper():
            return "UPPERCASE_FIRST_LETTER"

        return "OTHER"





























    def _append_to_description(self, clean_node: dict, section_name: str, value) -> None:
        description_field = self._get_description_field_name(section_name)

        if description_field not in clean_node:
            clean_node[description_field] = []

        if not isinstance(clean_node[description_field], list):
            old_value = clean_node[description_field]
            clean_node[description_field] = []

            if old_value:
                clean_node[description_field].append(old_value)

        values = value if isinstance(value, list) else [value]

        for item in values:
            if not item:
                continue

            item = str(item).strip()

            if not item:
                continue

            if not clean_node[description_field]:
                clean_node[description_field].append(item)
                continue

            first_key = self._description_item_start_key(clean_node[description_field][0])
            current_key = self._description_item_start_key(item)

            if current_key == first_key:
                clean_node[description_field].append(item)
            else:
                clean_node[description_field][-1] = (
                        str(clean_node[description_field][-1]).rstrip()
                        + " "
                        + item
                )














    def _tree_node_to_description_text(self, node: dict) -> list:
        result = []

        text = node.get("valeur", "")
        if text:
            result.append(text)

        for child in node.get("children", []):
            result.extend(
                self._tree_node_to_description_text(child)
            )

        return result



















    def _set_output_field_value(self, clean_node: dict, field_name: str, value: str) -> None:
        if field_name not in clean_node:
            return

        if not value:
            return

        value = str(value).strip()

        if not value:
            return

        current_value = clean_node[field_name]

        # Description fields are lists. They have their own logic in _append_to_description.
        if isinstance(current_value, list):
            return

        if not current_value:
            clean_node[field_name] = value
            return

        if value not in str(current_value):
            clean_node[field_name] = (
                    str(current_value).rstrip()
                    + self.MERGE_SAME_STYLE_TITLE_SEPARATOR
                    + value
            )






    def _is_language_name(self, text: str) -> bool:
        text_norm = self._normalize_text(text)

        for language in self.LANGUAGE_NAMES:
            if text_norm == self._normalize_text(language):
                return True

        return False


    def _split_langue_text(self, text: str) -> dict | None:
        parts = self._split_phrase_to_parts(text)

        if not parts:
            return None

        first_word = self._fix_text(parts[0])

        if not self._is_language_name(first_word):
            return None

        description = " ".join(
            self._fix_text(part)
            for part in parts[1:]
        ).strip()

        return {
            "nomLangue": first_word,
            "DescriptionLangue": description,
        }











    def _fill_first_level_child_output(self, node: dict, section_name: str) -> dict:
        config = self.SECTION_CHILD_OUTPUT_FIELDS.get(section_name)

        if not config:
            return self._tree_node_to_description_text(node)

        clean_node = self._empty_section_child_output(section_name)

        text = node.get("valeur", "")

        if section_name == "langues":
            langue_data = self._split_langue_text(text)

            if langue_data:
                self._set_output_field_value(
                    clean_node,
                    "nomLangue",
                    langue_data["nomLangue"],
                )

                if langue_data["DescriptionLangue"]:
                    self._append_to_description(
                        clean_node,
                        section_name,
                        langue_data["DescriptionLangue"],
                    )

                for child in node.get("children", []):
                    self._append_to_description(
                        clean_node,
                        section_name,
                        self._tree_node_to_description_text(child),
                    )

                return clean_node

        detected_fields = self._detect_specific_output_fields(section_name, text)

        if detected_fields:
            for field_name, field_value in detected_fields.items():
                self._set_output_field_value(clean_node, field_name, field_value)
        else:
            root_field = config["root_text"]
            self._set_output_field_value(clean_node, root_field, text)

        for child in node.get("children", []):
            child_text = child.get("valeur", "")
            child_detected_fields = self._detect_specific_output_fields(section_name, child_text)

            if child_detected_fields:
                for field_name, field_value in child_detected_fields.items():
                    self._set_output_field_value(clean_node, field_name, field_value)

                for grand_child in child.get("children", []):
                    self._append_to_description(
                        clean_node,
                        section_name,
                        self._tree_node_to_description_text(grand_child),
                    )
            else:
                self._append_to_description(
                    clean_node,
                    section_name,
                    self._tree_node_to_description_text(child),
                )

        return clean_node




















    def _clean_tree_child_node(self, node: dict, section_name: str, level: int = 0):
        if level == 0:
            return self._fill_first_level_child_output(node, section_name)

        return self._tree_node_to_description_text(node)















    def _merge_tree_node_text(self, old_node: dict, new_node: dict) -> None:
        old_text = str(old_node.get("valeur", "")).strip()
        new_text = str(new_node.get("valeur", "")).strip()

        if old_text and new_text:
            old_node["valeur"] = old_text + self.MERGE_SAME_STYLE_TITLE_SEPARATOR + new_text
        elif new_text:
            old_node["valeur"] = new_text

        for child in new_node.get("children", []):
            old_node.setdefault("children", []).append(child)





















    def _children_lines_to_tree(self, children: list[dict]) -> list[dict]:
        roots = []
        stack = []

        for child in children:
            if not isinstance(child, dict):
                continue

            new_node = self._make_tree_child_node(child)
            new_style = new_node.get("_style")

            if not stack:
                roots.append(new_node)
                stack = [new_node]
                continue

            same_level_found = False

            for level in range(len(stack) - 1, -1, -1):
                old_node = stack[level]

                if old_node.get("_style") == new_style:
                    if level == 0:
                        if (
                                self.MERGE_SAME_STYLE_TITLE_LINES
                                and roots
                                and roots[-1] is old_node
                                and not old_node.get("children")
                                and not new_node.get("children")
                        ):
                            self._merge_tree_node_text(old_node, new_node)
                            stack = [old_node]
                        else:
                            roots.append(new_node)
                            stack = [new_node]
                    else:
                        stack[level - 1]["children"].append(new_node)
                        stack = stack[:level] + [new_node]

                    same_level_found = True
                    break

            if not same_level_found:
                stack[-1]["children"].append(new_node)
                stack.append(new_node)

        return roots










    def _merge_same_style_empty_root_titles(self, roots: list[dict]) -> list[dict]:
        merged = []

        for node in roots:
            if not merged:
                merged.append(node)
                continue

            previous_node = merged[-1]

            previous_has_children = bool(previous_node.get("children"))
            same_style = previous_node.get("_style") == node.get("_style")

            if (
                    self.MERGE_SAME_STYLE_TITLE_LINES
                    and same_style
                    and not previous_has_children
            ):
                previous_text = str(previous_node.get("valeur", "")).strip()
                current_text = str(node.get("valeur", "")).strip()

                if previous_text and current_text:
                    node["valeur"] = (
                            previous_text
                            + self.MERGE_SAME_STYLE_TITLE_SEPARATOR
                            + current_text
                    )
                elif previous_text:
                    node["valeur"] = previous_text

                merged[-1] = node
                continue

            merged.append(node)

        return merged

















    def _sections_to_hierarchy_tree(self, sections: list[dict]) -> list[dict]:
        clean_sections = []

        for section in sections:
            clean_section = {}

            hidden_output_keys = {
                "page",
                "line_number",
                "x",
                "y",
                "x0",
                "x1",
                "top",
                "bottom",
            }

            for key, value in section.items():
                if key == "children":
                    continue

                if key in hidden_output_keys:
                    continue

                clean_section[key] = value





            raw_tree_children = self._children_lines_to_tree(
                section.get("children", [])
            )

            raw_tree_children = self._merge_same_style_empty_root_titles(raw_tree_children)

            clean_section["children"] = [
                self._clean_tree_child_node(child, section["section"])
                for child in raw_tree_children
            ]






            clean_sections.append(clean_section)

        return clean_sections

    def _get_or_create_unique_section(
            self,
            final_sections: list[dict],
            section_node: dict,
    ) -> dict:
        for existing_section in final_sections:
            if existing_section["section"] == section_node["section"]:
                existing_section["header"] = section_node["header"]
                existing_section["CLWord"] = section_node["CLWord"]
                existing_section["page"] = section_node["page"]
                existing_section["line_number"] = section_node["line_number"]
                existing_section["x"] = section_node["x"]
                existing_section["y"] = section_node["y"]
                existing_section["x0"] = section_node["x0"]
                existing_section["x1"] = section_node["x1"]
                existing_section["top"] = section_node["top"]
                existing_section["bottom"] = section_node["bottom"]

                return existing_section

        final_sections.append(section_node)
        return section_node

    def _replace_active_section_by_x_owner(self, active_sections: list[dict], new_section: dict) -> list[dict]:
        if not active_sections:
            return [new_section]

        owner = self._find_owner_section_by_x(
            new_section["x"],
            active_sections,
        )

        updated = []

        for section in active_sections:
            if section is owner:
                updated.append(new_section)
            else:
                updated.append(section)

        return sorted(updated, key=lambda section: section["x"])

    def hedhiTrajaaliChildrenMotCle(self, result: dict, liste: list, as_tree: bool = False) -> dict:
        try:
            if not result or not result.get("success"):
                return {
                    "success": False,
                    "error": "BAD_RESULT",
                    "message": "PDF result is empty or not successful",
                    "data": [],
                }

            if not liste:
                return {
                    "success": False,
                    "error": "EMPTY_HEADERS",
                    "message": "No detected keywords found",
                    "data": [],
                }

            pdf_file = result.get("pdf_file")
            if not pdf_file:
                return {
                    "success": False,
                    "error": "PDF_FILE_MISSING",
                    "message": "pdf_file not found in result",
                    "data": [],
                }

            pdf_path = Path(pdf_file)
            if not pdf_path.exists():
                return {
                    "success": False,
                    "error": "PDF_NOT_FOUND",
                    "message": f"PDF not found: {pdf_path}",
                    "data": [],
                }

            pages_info = {
                page["page"]: page
                for page in result.get("pages", [])
            }

            headers_by_page_line = {}
            for header in liste:
                key = (header["page"], header["line_number"])
                headers_by_page_line.setdefault(key, []).append(header)

            final_sections = []
            active_sections = []

            with pdfplumber.open(str(pdf_path)) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_info = pages_info.get(page_number)

                    if not page_info:
                        continue

                    page_width = float(page_info["width"])
                    page_height = float(page_info["height"])

                    words = page.extract_words(
                        extra_attrs=[
                            "size",
                            "fontname",
                            "non_stroking_color",
                            "stroking_color",
                        ]
                    )

                    lines = self._group_words_by_line(words, self.WORD_LINE_TOLERANCE)

                    for line_number, line_words in enumerate(lines, start=1):
                        current_headers = headers_by_page_line.get((page_number, line_number), [])



















                        if current_headers:
                            current_headers = sorted(current_headers, key=lambda item: item["x"])

                            line_children = self._convert_line_words_to_center_words(
                                line_words,
                                page_number,
                                line_number,
                                page_width,
                                page_height,
                            )

                            if len(current_headers) > 1:
                                active_sections = []

                                for index, header in enumerate(current_headers):
                                    section_node = self._make_section_node_from_header(header)

                                    section_node = self._get_or_create_unique_section(
                                        final_sections,
                                        section_node,
                                    )

                                    active_sections.append(section_node)

                                    next_header = (
                                        current_headers[index + 1]
                                        if index + 1 < len(current_headers)
                                        else None
                                    )

                                    same_line_words = self._same_line_words_after_header(
                                        line_children,
                                        header,
                                        next_header,
                                    )

                                    child_line = self._build_child_line(same_line_words)

                                    if child_line:
                                        section_node["children"].append(child_line)

                                active_sections = sorted(active_sections, key=lambda section: section["x"])
                                continue






















                            header = current_headers[0]
                            section_node = self._make_section_node_from_header(header)

                            section_node = self._get_or_create_unique_section(
                                final_sections,
                                section_node,
                            )

                            if active_sections:
                                old_owner = self._find_owner_section_by_x(
                                    section_node["x"],
                                    active_sections,
                                )

                                new_active_sections = []

                                for active in active_sections:
                                    if active is old_owner:
                                        new_active_sections.append(section_node)
                                    else:
                                        new_active_sections.append(active)

                                active_sections = sorted(new_active_sections, key=lambda section: section["x"])














                            else:
                                active_sections = [section_node]

                            same_line_words = self._same_line_words_after_header(
                                line_children,
                                header,
                            )

                            child_line = self._build_child_line(same_line_words)

                            if child_line:
                                section_node["children"].append(child_line)

                            continue














                        if not active_sections:
                            continue

                        line_children = self._convert_line_words_to_center_words(
                            line_words,
                            page_number,
                            line_number,
                            page_width,
                            page_height,
                        )

                        if len(active_sections) == 1:
                            child_line = self._build_child_line(line_children)

                            if child_line:
                                active_sections[0]["children"].append(child_line)

                            continue

                        words_by_section = {}

                        for word in line_children:
                            owner = self._find_owner_section_by_x(
                                word["x"],
                                active_sections,
                            )

                            if owner is None:
                                continue

                            owner_id = id(owner)
                            words_by_section.setdefault(owner_id, {
                                "section": owner,
                                "words": [],
                            })
                            words_by_section[owner_id]["words"].append(word)

                        for item in words_by_section.values():
                            child_line = self._build_child_line(item["words"])

                            if child_line:
                                item["section"]["children"].append(child_line)

            data = (
                self._sections_to_hierarchy_tree(final_sections)
                if as_tree
                else self._clean_children_to_text_only(final_sections)
            )

            return {
                "success": True,
                "error": None,
                "message": "Children assigned successfully",
                "data": data,
            }

        except Exception as e:
            return {
                "success": False,
                "error": type(e).__name__,
                "message": str(e),
                "data": [],
            }
























