from page import Page

class Category():
    def __init__(self, url, category, proxies={}, appendix=""):
        self.url = url
        self.category = category
        self.proxies = proxies
        self.next_page_appendix = appendix

        # pages hold Page instances
        self.pages = []
        # first_page is Page instance
        self.first_page = None
        self.last_page_no = None

    def _find_last_page(self):
        last_page = self.first_page.soup.find("a", {"class": "emos_invisible lastPage"})
        if last_page == None:
            return 2
        return int(last_page["href"].split("page=")[1])

    def fetch_first_page(self):
        self.first_page = Page(self.url, self.category, self.proxies)
        self.pages.append(self.first_page)
        self.first_page.fetch_page()

    def create_pages(self):
        self.fetch_first_page()
        self.last_page_no = self._find_last_page()
        for i in range(2, self.last_page_no+1):
            url = self.url + self.next_page_appendix + str(i)
            page = Page(url=url, category=self.category)
            self.pages.append(page)

    def parse_pages(self):
        print("Fetching category: " + self.category)
        for page in self.pages:
            page.fetch_page()
            page.fetch_items()
