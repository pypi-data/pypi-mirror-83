from pathlib import PosixPath, Path


def flatten_seq(seq):
    """convert a sequence of embedded sequences into a plain list"""
    result = []
    vals = seq.values() if type(seq) == dict else seq
    for i in vals:
        if isinstance(i, (dict, list)):
            result.extend(flatten_seq(i))
        elif isinstance(i, str):
            result.append(i)
    return result


class ChapterNotFoundError(Exception):
    pass


class Chapters:
    """
    Helper class converting chapter list of complicated structure
    into a plain list of chapter names or path to actual md files
    in the src dir.
    """

    def __init__(self,
                 chapters: list,
                 working_dir: str or PosixPath or None = None,
                 src_dir: str or PosixPath or None = None,
                 ):
        self.working_dir = Path(working_dir).resolve() if working_dir else None
        self.src_dir = Path(src_dir).resolve() if src_dir else None
        self._chapters = chapters
        self._flat = flatten_seq(chapters)

    def __len__(self):
        return len(self._flat)

    def __getitem__(self, ind: int):
        return self._flat[ind]

    def __contains__(self, item: str):
        return item in self._flat

    def __iter__(self):
        return iter(self._flat)

    def __repr__(self):
        return f'Chapters({self._chapters})'

    @staticmethod
    def from_config(config: dict):
        '''
        Returns a Chapters instance, initiated with properties from config.
        '''
        return Chapters(
            config['chapters'],
            working_dir=config['tmp_dir'],
            src_dir=config['src_dir']
        )

    @property
    def chapters(self):
        """Original chapters list"""
        return self._chapters

    @chapters.setter
    def chapters(self, chapters):
        self._chapters = chapters
        self._flat = flatten_seq(chapters)

    @property
    def flat(self):
        """Flat list of chapter file names"""
        return self._flat

    def get_chapter_by_path(self, filepath: str or PosixPath):
        """
        Try and find filepath in working dir or src dir. If it is present in
        one of those — return relative path to file (as it is stated in chapters)
        """
        abs_path = Path(filepath).resolve()
        if self.working_dir and self.working_dir in abs_path.parents:
            chapter_path = str(abs_path.relative_to(self.working_dir))
        if self.src_dir and self.src_dir in abs_path.parents:
            chapter_path = str(abs_path.relative_to(self.src_dir))
        if chapter_path and chapter_path in self.chapters:
            return chapter_path
        else:
            raise ChapterNotFoundError(f'{filepath} is not in the chapter list')

    def paths(self, parent_dir: str or PosixPath):
        """
        Returns generator yielding PosixPath object with chapter path, relative
        to parent_dir.
        """

        return (Path(parent_dir) / chap for chap in self.flat)

    def get_chapter_title(self, chapter_path: str):
        """
        Returns the title for the chapter, defind in the chapters list.
        Returns empty string if chapter defined without title.
        Raises ChapterNotFoundError if chapter is not present in the list.

        Examples:

        ***
        chapters:
            - Chapter Title: info/index.md

        get_chapter_title('info/index.md') will return 'Chapter Title'

        ***
        chapters:
            - info/index.md

        get_chapter_title('info/index.md') will return ''

        ***
        chapters:
            - info.md

        get_chapter_title('info/index.md') will raise ChapterNotFoundError

        :param chapter_path: path to the chapter for which the title needs to be
                             found, _as it is stated in the chapters list_.

        :returns: chapter title or empty string.
        """
        def find_chapter(chapters: list or dict, to_find: str) -> str or dict or None:
            if isinstance(chapters, list):
                for i in chapters:
                    if isinstance(i, (list, dict)):
                        found = find_chapter(i, to_find)
                        if found:
                            return found
                    elif isinstance(i, str) and i == to_find:
                        return i
            elif isinstance(chapters, dict):
                val = next(iter(chapters.values()))
                if isinstance(val, str) and val == to_find:
                    return chapters
                else:
                    found = find_chapter(val, to_find)
                    if found:
                        return found
            elif isinstance(chapters, str):
                if chapters == to_find:
                    return chapters
            return None

        chapter = find_chapter(self.chapters, chapter_path)
        if chapter is None:
            raise ChapterNotFoundError(f'{chapter_path} is not in the chapter list')
        if isinstance(chapter, str):
            return ''
        elif isinstance(chapter, dict):
            return next(iter(chapter.keys()))
