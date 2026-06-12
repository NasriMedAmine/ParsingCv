import json
import re
import unicodedata
from pathlib import Path
from collections import Counter
import ftfy
import pdfplumber


BASE_DIR = Path(__file__).resolve().parent


class AlgoTest:
    SPECIAL_WORDS = [
        "&",
    ]

    SECTION_HEADERS = {
        "informations_personnelles": {
            "oneWord": [
                "coordonnees",
                "contact",
                "profil",
            ],
            "aLotOfWords": [
                "informations personnelles",
                "information personnelle",
                "personal information",
                "about me",
            ],
        },
        "competences": {
            "oneWord": [
                "competences",
                "competence",
                "skills",
                "expertise",
                "technologies",
            ],
            "aLotOfWords": [
                "competences techniques",
                "competences fonctionnelles",
                "technical skills",
            ],
        },
        "langues": {
            "oneWord": [
                "langues",
                "langue",
                "languages",
            ],
            "aLotOfWords": [
                "language skills",
            ],
        },
        "formation": {
            "oneWord": [
                "formation",
                "formations",
                "education",
                "diplomes",
                "etudes",
                "cursus",
            ],
            "aLotOfWords": [
                "formations & certifications",
            ],
        },
        "experience": {
            "oneWord": [
                "experience",
                "experiences",
            ],
            "aLotOfWords": [
                "experiences professionnelles",
                "experience professionnelle",
                "detail des experiences professionnelles",
                "work experience",
                "professional experience",
                "parcours professionnel",
            ],
        },
        "projets": {
            "oneWord": [
                "projets",
                "projet",
                "projects",
                "project",
                "realisations",
                "portfolio",
            ],
            "aLotOfWords": [],
        },
        "centres_interet": {
            "oneWord": [
                "loisirs",
                "hobbies",
                "interets",
                "interests",
            ],
            "aLotOfWords": [
                "centres d'interet",
                "centre d'interet",
            ],
        },
        "certifications": {
            "oneWord": [
                "certifications",
                "certification",
                "certificats",
                "certificat",
                "certificates",
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

    def _normalize_text(self, text: str) -> str:
        text = text or ""

        if text in self.SPECIAL_WORDS:
            return text

        # ftfy yصلح encoding problems (ExpÃ©riences → Expériences)
        text = ftfy.fix_text(text)

        # NFD يشيل accents (Expériences → Experiences)
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        text = text.lower().strip()
        return re.sub(r"[^a-z0-9]+", "", text)

    def _split_phrase_to_parts(self, text: str) -> list[str]:
        text = text or ""

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
                    normalized_key = tuple(parts)
                    if normalized_key not in {tuple(m["parts"]) for m in multi_words}:
                        multi_words.append({
                            "header": header,
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
                    "header": word.get("text", ""),
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
        one_word_candidate = self._find_one_word_candidate(line_words[index], header_indexes)

        if one_word_candidate:
            one_word_candidate["start_index"] = index
            one_word_candidate["end_index"] = index + 1
            return one_word_candidate

        multi_word_candidate = self._find_multi_word_candidate_at(line_words, index, header_indexes)

        if multi_word_candidate:
            multi_word_candidate["start_index"] = index
            multi_word_candidate["end_index"] = index + len(multi_word_candidate["parts"])
            return multi_word_candidate

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
        return " ".join(word.get("text", "") for word in words)

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

    def _candidate_differs_from_words(
            self,
            line_words: list[dict],
            candidate: dict,
            normal_words: list[dict],
            dominant_style: tuple | None = None,
    ) -> bool:
        candidate_words = self._candidate_words(line_words, candidate)

        if not candidate_words:
            return False

        candidate_style = self._style_signature(candidate_words[0])

        if not normal_words:
            if dominant_style is None:
                return True
            return candidate_style != dominant_style

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
            "line_text": " ".join(word.get("text", "") for word in line_words),

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
                    "word": word.get("text", ""),
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
            dominant_style: tuple | None = None,
    ) -> bool:
        if not self._candidate_has_one_style(line_words, candidate):
            return False

        if not self._candidate_differs_from_words(
                line_words, candidate, normal_words_in_line, dominant_style
        ):
            return False

        return True

    def _compute_dominant_style(self, all_words: list[dict]) -> tuple | None:
        if not all_words:
            return None

        counter = Counter()
        for word in all_words:
            sig = self._style_signature(word)
            counter[sig] += 1

        return counter.most_common(1)[0][0]

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

            # Pass 1: dominant style
            all_document_words = []

            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    words = page.extract_words(
                        extra_attrs=[
                            "size",
                            "fontname",
                            "non_stroking_color",
                            "stroking_color",
                        ]
                    )
                    all_document_words.extend(words)

            dominant_style = self._compute_dominant_style(all_document_words)

            # Pass 2: detect headers
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
                                    dominant_style,
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