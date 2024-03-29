class WordUtils:
    @staticmethod
    def get_words(category):
        words = ['account', 'login']

        bank_words = ['bankasi', 'kolaybasvuru', 'bayramkredisi', 'faizyok']
        shopping_words = ['hediye', 'gift', 'bedava', 'firsat']
        personal_words = ['official']

        if category == "Bank":
            words += bank_words
        elif category == "Shopping":
            words += shopping_words
        elif category == "Personal":
            words += personal_words

        return words
