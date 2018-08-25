from peewee import SqliteDatabase, CharField

pragmas = {
    'journal_mode': 'wal'
}
db = SqliteDatabase('urls.db', pragmas=pragmas)


class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        db.connect()

    def process_response(self, req, resp, resource):
        if not db.is_closed():
            db.close()
