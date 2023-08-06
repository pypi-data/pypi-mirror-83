from ocrd_browser.model import Document


class Source:
    pass


class FileGroupSource(Source):
    def __init__(self, file_group: str, mimetype: str):
        self.file_group = file_group
        self.mimetype = mimetype

    def get(self, document: Document, page_id: str):
        return next(iter(document.files_for_page_id(page_id, self.file_group, self.mimetype)))
