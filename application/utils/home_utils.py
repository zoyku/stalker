
class HomeUtils:
    @staticmethod
    def create_user(keyword,register_name):

        user1 = User(insert_date='01.01.2000', update_date='01.01.2000', register_name=register_name, keyword=keyword)
        db.session.add(user1)
        db.session.commit()
        i = 0
        while i < 50:
            typo = typo_generator(keyword)
            keyword = KeywordTypo(keywordUser=User.query.filter_by(registerName=register_name), typo=typo)
            db.session.add(keyword)
            db.session.commit()
            i += 1

        return 0

    def typo_generator(phrase):
        ix = random.choice(range(len(phrase)))
        new_word = ''.join([phrase[w] if w != ix else random.choice(string.ascii_letters) for w in range(len(phrase))])

        return new_word