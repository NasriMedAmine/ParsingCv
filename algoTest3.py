import json
import re
import unicodedata
from pathlib import Path

import ftfy
import pdfplumber


BASE_DIR = Path(__file__).resolve().parent


class AlgoTest:

    #hedhi bech kelma yahsebha 3 mots ; exemple A & B  twali 3 mots
    SPECIAL_WORDS = [
        "&",
    ]

    #1 cm = 28.35 PDF points
    CHILD_LINE_Y_TOLERANCE = 3.0
    COLUMN_OFFSET_X = 100
    WORD_LINE_TOLERANCE = 3.0

    SECTION_HEADERS = {
        "informations_personnelles": {
            "oneWord": [
                "coordonnees", "Coordonnees", "COORDONNEES",
                "coordonnées", "Coordonnées", "COORDONNÉES",
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
                "compétences", "Compétences", "COMPÉTENCES",
                "competence", "Competence", "COMPETENCE",
                "compétence", "Compétence", "COMPÉTENCE",
                "skills", "Skills", "SKILLS",
                "expertise", "Expertise", "EXPERTISE",
                "technologies", "Technologies", "TECHNOLOGIES",
            ],
            "aLotOfWords": [
                "competences techniques", "Competences Techniques", "COMPETENCES TECHNIQUES",
                "compétences techniques", "Compétences Techniques", "COMPÉTENCES TECHNIQUES",
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
                "éducation", "Éducation", "ÉDUCATION",
                "diplomes", "Diplomes", "DIPLOMES",
                "diplômes", "Diplômes", "DIPLÔMES",
                "etudes", "Etudes", "ETUDES",
                "études", "Études", "ÉTUDES",
                "cursus", "Cursus", "CURSUS",
            ],
            "aLotOfWords": [
                "formations & certifications", "Formations & Certifications", "FORMATIONS & CERTIFICATIONS",
            ],
        },
        "experience": {
            "oneWord": [
                "experience", "Experience", "EXPERIENCE",
                "expérience", "Expérience", "EXPÉRIENCE",
                "experiences", "Experiences", "EXPERIENCES",
                "expériences", "Expériences", "EXPÉRIENCES",
            ],
            "aLotOfWords": [
                "experiences professionnelles", "Experiences Professionnelles", "EXPERIENCES PROFESSIONNELLES",
                "expériences professionnelles", "Expériences Professionnelles", "EXPÉRIENCES PROFESSIONNELLES",
                "experience professionnelle", "Experience Professionnelle", "EXPERIENCE PROFESSIONNELLE",
                "expérience professionnelle", "Expérience Professionnelle", "EXPÉRIENCE PROFESSIONNELLE",
                "detail des experiences professionnelles", "Detail Des Experiences Professionnelles", "DETAIL DES EXPERIENCES PROFESSIONNELLES",
                "détail des expériences professionnelles", "Détail Des Expériences Professionnelles", "DÉTAIL DES EXPÉRIENCES PROFESSIONNELLES",
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
                "réalisations", "Réalisations", "RÉALISATIONS",
                "portfolio", "Portfolio", "PORTFOLIO",
            ],
            "aLotOfWords": [],
        },
        "centres_interet": {
            "oneWord": [
                "loisirs", "Loisirs", "LOISIRS",
                "hobbies", "Hobbies", "HOBBIES",
                "interets", "Interets", "INTERETS",
                "intérêts", "Intérêts", "INTÉRÊTS",
                "interests", "Interests", "INTERESTS",
            ],
            "aLotOfWords": [
                "centres d'interet", "Centres D'Interet", "CENTRES D'INTERET",
                "centres d’intérêt", "Centres D’intérêt", "CENTRES D’INTÉRÊT",
                "centre d'interet", "Centre D'Interet", "CENTRE D'INTERET",
                "centre d’intérêt", "Centre D’intérêt", "CENTRE D’INTÉRÊT",
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

    def writeResultatJson(self, resultat: dict) -> int:
        try:
            output_path = BASE_DIR / "resultat.json"

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(resultat, file, ensure_ascii=False, indent=4)

            return 1

        except Exception:
            return 0

        # hedhom Wahadhom Khati Hesba
    # ******************************************************
    # ******************************************************
    # ******************************************************
    # ******************************************************

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



    # hedhom tebiin baathom
    # hedhom bech nfix pdf file aala ases houwa rectangle w aandou point centre (0, 0)
    # ******************************************************
    # ******************************************************
    # ******************************************************
    # ******************************************************








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

    def _style_signature(self, word: dict) -> tuple:
        return self._word_size(word), str(self._word_color(word))

    def _same_style(self, word1: dict, word2: dict) -> bool:
        return self._style_signature(word1) == self._style_signature(word2)

    def _group_words_by_line(self, words: list[dict], tolerance: float = 3.0) -> list[list[dict]]:
        lines = []
        sorted_words = sorted(words, key=lambda w: (float(w["top"]), float(w["x0"])))

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
            line.sort(key=lambda w: float(w["x0"]))

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

        fixed_x, fixed_y = self._center_pdf_point(
            box["x"],
            box["y"],
            page_width,
            page_height,
        )

        fixed_x0, fixed_top = self._center_pdf_point(
            box["x0"],
            box["top"],
            page_width,
            page_height,
        )

        fixed_x1, fixed_bottom = self._center_pdf_point(
            box["x1"],
            box["bottom"],
            page_width,
            page_height,
        )

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

    def _candidate_passes_style_conditions(
            self,
            line_words: list[dict],
            candidate: dict,
            normal_words_in_line: list[dict],
    ) -> bool:
        if not self._candidate_has_one_style(line_words, candidate):
            return False

        if not self._candidate_differs_from_words(line_words, candidate, normal_words_in_line):
            return False

        return True

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

                    lines = self._group_words_by_line(words)

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



# hedhom tebiin baathom
#  BAAED MAAMALT ==> hedhom bech nfix pdf file aala ases houwa rectangle w aandou point centre (0, 0)
# Hedhom bech ndetecti kol mot cle win blastou bithabet f page depent de centre de page
# ******************************************************
# ******************************************************
# ******************************************************
# ******************************************************


























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



    def _find_owner_section_by_x(self, word_x: float, active_sections: list[dict]) -> dict:
        active_sections = sorted(active_sections, key=lambda section: section["x"])

        if len(active_sections) == 1:
            return active_sections[0]

        for index, section in enumerate(active_sections):
            if index == 0:
                next_section = active_sections[index + 1]
                right_limit = next_section["x"] - self.COLUMN_OFFSET_X

                if word_x < right_limit:
                    return section

            elif index == len(active_sections) - 1:
                left_limit = section["x"] - self.COLUMN_OFFSET_X

                if word_x >= left_limit:
                    return section

            else:
                left_limit = section["x"] - self.COLUMN_OFFSET_X
                next_section = active_sections[index + 1]
                right_limit = next_section["x"] - self.COLUMN_OFFSET_X

                if left_limit <= word_x < right_limit:
                    return section

        return active_sections[-1]







    def _replace_or_add_active_section(self, active_sections: list[dict], section_node: dict) -> list[dict]:
        updated_sections = []
        replaced = False

        for active in active_sections:
            if active["section"] == section_node["section"]:
                updated_sections.append(section_node)
                replaced = True
            else:
                updated_sections.append(active)

        if not replaced:
            updated_sections.append(section_node)

        return sorted(updated_sections, key=lambda section: section["x"])














    def _section_interval_owner(
            self,
            word_x: float,
            active_sections: list[dict],
            page_left: float,
            page_right: float,
    ) -> dict | None:
        if not active_sections:
            return None

        active_sections = sorted(active_sections, key=lambda section: section["x"])

        if len(active_sections) == 1:
            return active_sections[0]

        for index, section in enumerate(active_sections):
            left_limit = page_left
            right_limit = page_right

            if index > 0:
                left_limit = section["x"] - self.COLUMN_OFFSET_X

            if index < len(active_sections) - 1:
                next_section = active_sections[index + 1]
                right_limit = next_section["x"] - self.COLUMN_OFFSET_X

            if left_limit <= word_x < right_limit:
                return section

        return active_sections[-1]


    def _replace_active_section_by_interval(
            self,
            active_sections: list[dict],
            new_section: dict,
            page_left: float,
            page_right: float,
    ) -> list[dict]:
        if not active_sections:
            return [new_section]

        old_owner = self._section_interval_owner(
            new_section["x"],
            active_sections,
            page_left,
            page_right,
        )

        updated = []

        for section in active_sections:
            if section is old_owner:
                updated.append(new_section)
            else:
                updated.append(section)

        return sorted(updated, key=lambda section: section["x"])


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


























    def _clean_internal_words_from_result(self, sections: list[dict]) -> list[dict]:
        for section in sections:
            for child in section.get("children", []):
                child.pop("_words", None)

        return sections










    def hedhiTrajaaliChildrenMotCle(self, result: dict, liste: list) -> dict:
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

                    page_left = float(page_info["rectangle"]["left"])
                    page_right = float(page_info["rectangle"]["right"])

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

                            for header in current_headers:
                                section_node = self._make_section_node_from_header(header)
                                final_sections.append(section_node)

                                if active_sections:
                                    active_sections = self._replace_active_section_by_interval(
                                        active_sections,
                                        section_node,
                                        page_left,
                                        page_right,
                                    )
                                else:
                                    active_sections.append(section_node)
                                    active_sections = sorted(active_sections, key=lambda section: section["x"])

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
                            owner = self._section_interval_owner(
                                word["x"],
                                active_sections,
                                page_left,
                                page_right,
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

            return {
                "success": True,
                "error": None,
                "message": "Children assigned successfully",
                "data": final_sections,
            }

        except Exception as e:
            return {
                "success": False,
                "error": type(e).__name__,
                "message": str(e),
                "data": [],
            }



























    def _build_child_line(self, words: list[dict]) -> dict | None:
        if not words:
            return None

        words = sorted(words, key=lambda word: word["x0"])
        text = " ".join(word["text"] for word in words).strip()

        return {
            "text": text,
            "_words": words,
        }


