class WordUtils:
    @staticmethod
    def get_words(category):
        words = []

        bank_words = ['bankasi', 'kolaybasvuru', 'bayramkredisi', 'faizyok']
        shopping_words = ['hediye', 'gift', 'bedava', 'firsat']
        personal_words = ['official']

        if category.name == "Bank":
            words += bank_words
        elif category.name == "Shopping":
            words += shopping_words
        elif category.name == "Personal":
            words += personal_words

        return words
