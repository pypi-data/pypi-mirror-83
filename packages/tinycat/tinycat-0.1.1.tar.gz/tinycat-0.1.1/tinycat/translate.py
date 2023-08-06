from typing import List, Callable, Dict


def paragraph_parser(source: str) -> List[str]:
    current_paragraph: str = ""
    paragraph_list: List[str] = []
    for line in source.split("\n"):
        if line.strip():
            current_paragraph += line + "\n"
        elif current_paragraph:
            paragraph_list.append(current_paragraph.strip())
            current_paragraph = ""
    if current_paragraph:
        paragraph_list.append(current_paragraph.strip())
    return paragraph_list


def generate_task(source: str, translator: Callable[[str], str], dictionary: Dict[str, str],
                  parser: Callable[[str], List[str]]) -> str:
    task: str = ""
    pieces: List[str] = parser(source)
    for piece in pieces:
        if piece in dictionary:
            task += dictionary[piece] + "\n\n"
        else:
            translation = translator(piece)
            task += '-' * 64 + "\n"
            task += piece + "\n\n"
            task += translation + "\n"
            task += '-' * 64 + "\n\n"
    return task


def process_translation(source: str, dictionary: Dict[str, str]) -> None:
    in_translation: bool = False
    in_source_text: bool = True
    original: str = ""
    translation: str = ""
    for line in source.split("\n"):
        if line.startswith('-' * 64):
            if in_translation:
                dictionary[original.strip()] = translation.strip()
                original = ""
                translation = ""
            in_translation = not in_translation
            in_source_text = True
        elif in_translation:
            if not line.strip():
                in_source_text = False
            elif in_source_text:
                original += line + "\n"
            else:
                translation += line + "\n"
